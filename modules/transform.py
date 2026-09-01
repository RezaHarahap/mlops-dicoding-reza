"""TFX Transform preprocessing module."""
import tensorflow as tf
import tensorflow_transform as tft
from modules.constants import LABEL_KEY

NUMERIC_FEATURES = [
    "mean radius", "mean texture", "mean perimeter", "mean area", "mean smoothness",
    "mean compactness", "mean concavity", "mean concave points", "mean symmetry",
    "mean fractal dimension", "radius error", "texture error", "perimeter error",
    "area error", "smoothness error", "compactness error", "concavity error",
    "concave points error", "symmetry error", "fractal dimension error",
    "worst radius", "worst texture", "worst perimeter", "worst area", "worst smoothness",
    "worst compactness", "worst concavity", "worst concave points", "worst symmetry",
    "worst fractal dimension"
]

def transformed_name(key: str) -> str:
    return f"{key}_xf"

def preprocessing_fn(inputs):
    """Scale numeric features and preserve the binary label."""
    outputs = {transformed_name(k): tft.scale_to_z_score(inputs[k]) for k in NUMERIC_FEATURES}
    outputs[transformed_name(LABEL_KEY)] = tf.cast(inputs[LABEL_KEY], tf.int64)
    return outputs
