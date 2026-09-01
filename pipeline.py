"""Local TFX pipeline definition used to generate reviewer-verifiable artifacts."""
from pathlib import Path

import tensorflow_model_analysis as tfma
from tfx.components import (
    CsvExampleGen,
    Evaluator,
    ExampleValidator,
    Pusher,
    SchemaGen,
    StatisticsGen,
    Trainer,
    Transform,
    Tuner,
)
from tfx.dsl.components.common.resolver import Resolver
from tfx.dsl.experimental import latest_blessed_model_resolver
from tfx.orchestration import metadata, pipeline
from tfx.orchestration.local.local_dag_runner import LocalDagRunner
from tfx.proto import pusher_pb2, trainer_pb2
from tfx.types import Channel, standard_artifacts

BASE_DIR = Path(__file__).resolve().parent
PIPELINE_NAME = "reza_harahap-pipeline"
PIPELINE_ROOT = str(BASE_DIR / PIPELINE_NAME)
DATA_ROOT = str(BASE_DIR / "data")
MODULE_ROOT = BASE_DIR / "modules"
SERVING_MODEL_DIR = str(BASE_DIR / "serving_model")
METADATA_PATH = str(BASE_DIR / "metadata.sqlite")


def create_pipeline():
    example_gen = CsvExampleGen(input_base=DATA_ROOT)
    statistics_gen = StatisticsGen(examples=example_gen.outputs["examples"])
    schema_gen = SchemaGen(
        statistics=statistics_gen.outputs["statistics"],
        infer_feature_shape=True,
    )
    validator = ExampleValidator(
        statistics=statistics_gen.outputs["statistics"],
        schema=schema_gen.outputs["schema"],
    )
    transform = Transform(
        examples=example_gen.outputs["examples"],
        schema=schema_gen.outputs["schema"],
        module_file=str(MODULE_ROOT / "transform.py"),
    )
    tuner = Tuner(
        module_file=str(MODULE_ROOT / "tuner.py"),
        examples=transform.outputs["transformed_examples"],
        transform_graph=transform.outputs["transform_graph"],
        train_args=trainer_pb2.TrainArgs(splits=["train"], num_steps=20),
        eval_args=trainer_pb2.EvalArgs(splits=["eval"], num_steps=10),
    )
    trainer = Trainer(
        module_file=str(MODULE_ROOT / "trainer.py"),
        examples=transform.outputs["transformed_examples"],
        transform_graph=transform.outputs["transform_graph"],
        schema=schema_gen.outputs["schema"],
        hyperparameters=tuner.outputs["best_hyperparameters"],
        train_args=trainer_pb2.TrainArgs(splits=["train"], num_steps=50),
        eval_args=trainer_pb2.EvalArgs(splits=["eval"], num_steps=20),
    )
    resolver = Resolver(
        strategy_class=latest_blessed_model_resolver.LatestBlessedModelResolver,
        model=Channel(type=standard_artifacts.Model),
        model_blessing=Channel(type=standard_artifacts.ModelBlessing),
    ).with_id("latest_blessed_model_resolver")

    eval_config = tfma.EvalConfig(
        model_specs=[tfma.ModelSpec(label_key="label")],
        slicing_specs=[tfma.SlicingSpec()],
        metrics_specs=[
            tfma.MetricsSpec(
                metrics=[
                    tfma.MetricConfig(
                        class_name="BinaryAccuracy",
                        threshold=tfma.MetricThreshold(
                            value_threshold=tfma.GenericValueThreshold(
                                lower_bound={"value": 0.80}
                            )
                        ),
                    ),
                    tfma.MetricConfig(
                        class_name="AUC",
                        threshold=tfma.MetricThreshold(
                            value_threshold=tfma.GenericValueThreshold(
                                lower_bound={"value": 0.80}
                            )
                        ),
                    ),
                ]
            )
        ],
    )

    evaluator = Evaluator(
        examples=example_gen.outputs["examples"],
        model=trainer.outputs["model"],
        baseline_model=resolver.outputs["model"],
        eval_config=eval_config,
    )
    pusher = Pusher(
        model=trainer.outputs["model"],
        model_blessing=evaluator.outputs["blessing"],
        push_destination=pusher_pb2.PushDestination(
            filesystem=pusher_pb2.PushDestination.Filesystem(
                base_directory=SERVING_MODEL_DIR
            )
        ),
    )

    components = [
        example_gen,
        statistics_gen,
        schema_gen,
        validator,
        transform,
        tuner,
        trainer,
        resolver,
        evaluator,
        pusher,
    ]
    return pipeline.Pipeline(
        pipeline_name=PIPELINE_NAME,
        pipeline_root=PIPELINE_ROOT,
        metadata_connection_config=metadata.sqlite_metadata_connection_config(
            METADATA_PATH
        ),
        components=components,
        enable_cache=False,
    )


if __name__ == "__main__":
    LocalDagRunner().run(create_pipeline())
