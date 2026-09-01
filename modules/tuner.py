"""Keras Tuner module used by the TFX Tuner component."""
from keras_tuner import HyperParameters, RandomSearch
import tensorflow_transform as tft
from tfx.components.trainer.fn_args_utils import FnArgs
from tfx.components.tuner.component import TunerFnResult
from modules.trainer import _build_model, _input_fn

def tuner_fn(fn_args: FnArgs):
    tf_transform_output = tft.TFTransformOutput(fn_args.transform_graph_path)
    train_ds = _input_fn(fn_args.train_files, tf_transform_output)
    eval_ds = _input_fn(fn_args.eval_files, tf_transform_output)
    def build_model(hp: HyperParameters):
        return _build_model(
            learning_rate=hp.Choice("learning_rate", [1e-2, 1e-3, 1e-4]),
            hidden_units=hp.Choice("hidden_units", [32, 64, 128]),
            dropout=hp.Float("dropout", 0.1, 0.4, step=0.1))
    tuner = RandomSearch(build_model, objective="val_auc", max_trials=5, overwrite=True,
                         directory=fn_args.working_dir, project_name="breast_cancer_tuning")
    return TunerFnResult(tuner=tuner, fit_kwargs={"x": train_ds, "validation_data": eval_ds,
        "steps_per_epoch": fn_args.train_steps, "validation_steps": fn_args.eval_steps, "epochs": 5})
