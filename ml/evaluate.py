import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score


def load_class_names(class_config_path: str = "classes.json") -> list[str]:
    config_path = Path(class_config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Class configuration file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as fh:
        config = json.load(fh)

    labels = config.get("labels") or {}
    if not labels:
        raise ValueError("No class labels were found in the model configuration.")

    ordered = [labels[str(i)] for i in sorted((int(k) for k in labels.keys()))]
    return ordered


def resolve_test_dir(dataset_root: str) -> Path:
    root = Path(dataset_root)
    for candidate in ["test", "validation", "valid", "val"]:
        path = root / candidate
        if path.exists() and path.is_dir():
            return path
    raise FileNotFoundError(f"No validation/test dataset directory found under: {root}")


def save_confusion_matrix(cm: np.ndarray, class_names: list[str], save_path: Path) -> None:
    save_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
    ax.figure.colorbar(im, ax=ax)
    ax.set(title="Confusion Matrix", xlabel="Predicted label", ylabel="True label")
    ax.set_xticks(np.arange(len(class_names)))
    ax.set_yticks(np.arange(len(class_names)))
    ax.set_xticklabels(class_names, rotation=45, ha="right")
    ax.set_yticklabels(class_names)

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], "d"), ha="center", va="center", color="white" if cm[i, j] > cm.max() / 2 else "black")

    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


def evaluate_model(
    dataset_root: str = "dataset",
    model_path: str = "ml/models/freshness_model.keras",
    output_dir: str = "results",
    class_config_path: str = "classes.json",
) -> dict:
    model_path_obj = Path(model_path)
    if not model_path_obj.exists():
        raise FileNotFoundError(f"Trained model not found at: {model_path_obj}")

    test_dir = resolve_test_dir(dataset_root)
    class_names = load_class_names(class_config_path)

    dataset = tf.keras.utils.image_dataset_from_directory(
        test_dir,
        labels="inferred",
        label_mode="int",
        class_names=class_names,
        image_size=(224, 224),
        batch_size=16,
        shuffle=False,
        validation_split=False,
    )

    model = tf.keras.models.load_model(str(model_path_obj))
    predictions = model.predict(dataset, verbose=1)
    y_pred = np.argmax(predictions, axis=1)
    y_true = np.concatenate([label for _, label in dataset], axis=0)

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average="weighted", zero_division=0)
    recall = recall_score(y_true, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=list(range(len(class_names))))
    report = classification_report(y_true, y_pred, target_names=class_names, output_dict=True, zero_division=0)

    result = {
        "dataset_root": dataset_root,
        "model_path": str(model_path_obj),
        "test_dir": str(test_dir),
        "class_names": class_names,
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "confusion_matrix": cm.tolist(),
        "classification_report": report,
    }

    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    metrics_path = output_dir_path / "evaluation_metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, ensure_ascii=False)

    save_confusion_matrix(cm, class_names, output_dir_path / "confusion_matrix.png")

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a trained freshness detection model.")
    parser.add_argument("--dataset-root", type=str, default="dataset", help="Root dataset directory.")
    parser.add_argument("--model-path", type=str, default="ml/models/freshness_model.keras", help="Path to the trained Keras model.")
    parser.add_argument("--output-dir", type=str, default="results", help="Directory to save metrics and charts.")
    parser.add_argument("--class-config", type=str, default="classes.json", help="Path to the class config JSON.")
    args = parser.parse_args()

    metrics = evaluate_model(
        dataset_root=args.dataset_root,
        model_path=args.model_path,
        output_dir=args.output_dir,
        class_config_path=args.class_config,
    )

    print(json.dumps({
        "accuracy": metrics["accuracy"],
        "precision": metrics["precision"],
        "recall": metrics["recall"],
        "f1_score": metrics["f1_score"],
        "class_names": metrics["class_names"],
        "confusion_matrix": metrics["confusion_matrix"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
