"""TFX Trainer module for binary classification."""
import tensorflow as tf
import tensorflow_transform as tft
from tfx.components.trainer.fn_args_utils import FnArgs
from modules.transform import NUMERIC_FEATURES, transformed_name
from modules.constants import LABEL_KEY

_BATCH_SIZE = 32

def _input_fn(file_pattern, tf_transform_output, batch_size=_BATCH_SIZE):
    transformed_feature_spec = tf_transform_output.transformed_feature_spec().copy()
    return tf.data.experimental.make_batched_features_dataset(
        file_pattern=file_pattern, batch_size=batch_size, features=transformed_feature_spec,
        reader=tf.data.TFRecordDataset, label_key=transformed_name(LABEL_KEY), shuffle=True)

def _build_model(learning_rate=1e-3, hidden_units=64, dropout=0.2):
    inputs = {transformed_name(k): tf.keras.Input(shape=(1,), name=transformed_name(k)) for k in NUMERIC_FEATURES}
    x = tf.keras.layers.concatenate(list(inputs.values()))
    x = tf.keras.layers.Dense(hidden_units, activation="relu")(x)
    x = tf.keras.layers.Dropout(dropout)(x)
    x = tf.keras.layers.Dense(max(hidden_units // 2, 8), activation="relu")(x)
    output = tf.keras.layers.Dense(1, activation="sigmoid", name="output")(x)
    model = tf.keras.Model(inputs=inputs, outputs=output)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate), loss="binary_crossentropy",
                  metrics=[tf.keras.metrics.BinaryAccuracy(name="binary_accuracy"), tf.keras.metrics.AUC(name="auc")])
    return model

def _get_serve_tf_examples_fn(model, tf_transform_output):
    model.tft_layer = tf_transform_output.transform_features_layer()
    @tf.function
    def serve_tf_examples_fn(serialized_tf_examples):
        feature_spec = tf_transform_output.raw_feature_spec()
        feature_spec.pop(LABEL_KEY, None)
        parsed_features = tf.io.parse_example(serialized_tf_examples, feature_spec)
        transformed_features = model.tft_layer(parsed_features)
        return {"outputs": model(transformed_features)}
    return serve_tf_examples_fn

def run_fn(fn_args: FnArgs):
    tf_transform_output = tft.TFTransformOutput(fn_args.transform_output)
    train_ds = _input_fn(fn_args.train_files, tf_transform_output)
    eval_ds = _input_fn(fn_args.eval_files, tf_transform_output)
    hp = fn_args.hyperparameters or {}
    model = _build_model(float(hp.get("learning_rate", 1e-3)), int(hp.get("hidden_units", 64)), float(hp.get("dropout", 0.2)))
    model.fit(train_ds, steps_per_epoch=fn_args.train_steps, validation_data=eval_ds, validation_steps=fn_args.eval_steps, epochs=10)
    signatures = {"serving_default": _get_serve_tf_examples_fn(model, tf_transform_output).get_concrete_function(
        tf.TensorSpec(shape=[None], dtype=tf.string, name="examples"))}
    model.save(fn_args.serving_model_dir, save_format="tf", signatures=signatures)
