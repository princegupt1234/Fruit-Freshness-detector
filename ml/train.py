import json
import os
from pathlib import Path

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam


def load_or_generate_classes(dataset_root: str, class_config_path: str = "classes.json") -> dict:
    class_config = Path(class_config_path)
    if class_config.exists():
        with open(class_config, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if data.get("labels"):
            return data

    from ml.dataset_validator import validate_model_training_input

    result = validate_model_training_input(dataset_root, str(class_config))
    return result.get("class_config", {"labels": {}, "supported_classes": []})


def get_dataset_dirs(dataset_root: str):
    root = Path(dataset_root)
    train_dir = root / "train"
    val_dir = root / "validation"
    if not val_dir.exists():
        val_dir = root / "valid"
    if not val_dir.exists():
        val_dir = root / "val"

    if not train_dir.exists():
        raise FileNotFoundError(f"Training directory not found: {train_dir}")
    if not val_dir.exists():
        raise FileNotFoundError(f"Validation directory not found under {root}")

    return train_dir, val_dir


def build_model(num_classes: int, input_shape=(224, 224, 3), model_name="MobileNetV2"):
    base_model = MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights="imagenet",
        alpha=1.0,
    )
    base_model.trainable = False

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation="softmax", name="predictions")
    ])

    model.compile(
        optimizer=Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def train_model(dataset_root: str = "dataset", output_dir: str = "ml/models"):
    class_config = load_or_generate_classes(dataset_root)
    labels = class_config.get("labels") or {}
    num_classes = len(labels)

    if num_classes == 0:
        raise ValueError("No class labels were discovered in the dataset. Please validate the dataset first.")

    train_dir, val_dir = get_dataset_dirs(dataset_root)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    train_generator = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        labels="inferred",
        label_mode="int",
        class_names=list(labels.values()) if labels else None,
        image_size=(224, 224),
        batch_size=16,
        shuffle=True,
        validation_split=False,
    )

    val_generator = tf.keras.utils.image_dataset_from_directory(
        val_dir,
        labels="inferred",
        label_mode="int",
        class_names=list(labels.values()) if labels else None,
        image_size=(224, 224),
        batch_size=16,
        shuffle=False,
        validation_split=False,
    )

    AUTOTUNE = tf.data.AUTOTUNE
    train_generator = train_generator.prefetch(AUTOTUNE)
    val_generator = val_generator.prefetch(AUTOTUNE)

    model = build_model(num_classes=num_classes)

    checkpoint_path = output_path / "freshness_model.keras"
    callbacks = [
        EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=2, min_lr=1e-6),
        ModelCheckpoint(filepath=str(checkpoint_path), save_best_only=True, monitor="val_accuracy")
    ]

    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=1,
        callbacks=callbacks,
        verbose=1,
    )

    model.save(str(output_path / "freshness_model.keras"))
    return history, model


if __name__ == "__main__":
    train_model(dataset_root="dataset", output_dir="ml/models")
