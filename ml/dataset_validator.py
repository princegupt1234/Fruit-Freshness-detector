import argparse
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def is_valid_image_file(file_path: Path) -> bool:
    return file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS


def safe_open_image(file_path: Path) -> bool:
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False


def discover_split_dirs(dataset_root: Path) -> Dict[str, Path]:
    split_dirs = {}
    for split_name in ["train", "validation", "valid", "val", "test"]:
        split_path = dataset_root / split_name
        if split_path.exists() and split_path.is_dir():
            split_dirs[split_name] = split_path
    return split_dirs


def get_class_directories(split_path: Path) -> List[Path]:
    return sorted([p for p in split_path.iterdir() if p.is_dir()])


def detect_dataset_structure(dataset_root: Path) -> str:
    split_dirs = discover_split_dirs(dataset_root)
    if split_dirs:
        return "split_directories"
    if any(p.is_dir() for p in dataset_root.iterdir()):
        return "flat_class_directories"
    return "empty"


def analyze_dataset(dataset_root: Path) -> Dict:
    summary = {
        "root": str(dataset_root),
        "structure": detect_dataset_structure(dataset_root),
        "splits": {},
        "classes": {},
        "missing_classes": {},
        "corrupted_images": {},
        "class_imbalance": {},
        "total_images": 0,
        "total_valid_images": 0,
        "errors": []
    }

    if not dataset_root.exists():
        summary["errors"].append(f"Dataset root does not exist: {dataset_root}")
        return summary

    split_dirs = discover_split_dirs(dataset_root)
    if not split_dirs:
        summary["errors"].append("No train/validation/test directories found in the dataset root.")
        return summary

    all_classes: set[str] = set()
    split_class_map: Dict[str, set[str]] = defaultdict(set)

    for split_name, split_path in split_dirs.items():
        classes = get_class_directories(split_path)
        split_summary = {
            "class_count": len(classes),
            "image_count": 0,
            "valid_images": 0,
            "classes": {}
        }

        for class_dir in classes:
            class_name = class_dir.name
            all_classes.add(class_name)
            split_class_map[split_name].add(class_name)

            valid_files = []
            corrupted = []
            for child in sorted(class_dir.iterdir()):
                if child.is_file() and is_valid_image_file(child):
                    valid_files.append(child)
                    if not safe_open_image(child):
                        corrupted.append(str(child))
                elif child.is_file() and child.suffix.lower() not in SUPPORTED_EXTENSIONS:
                    continue
            split_summary["classes"][class_name] = {
                "file_count": len(valid_files),
                "corrupted_images": corrupted,
                "valid_image_count": len(valid_files) - len(corrupted)
            }
            split_summary["image_count"] += len(valid_files)
            split_summary["valid_images"] += len(valid_files) - len(corrupted)

            if corrupted:
                summary["corrupted_images"].setdefault(split_name, {})[class_name] = corrupted

        summary["splits"][split_name] = split_summary

    summary["classes"] = sorted(all_classes)
    for split_name in split_dirs:
        expected_classes = set(summary["classes"])
        missing = sorted(expected_classes - split_class_map.get(split_name, set()))
        if missing:
            summary["missing_classes"][split_name] = missing

    for class_name in sorted(all_classes):
        counts = []
        for split_name, split_data in summary["splits"].items():
            class_info = split_data.get("classes", {}).get(class_name)
            counts.append(class_info["valid_image_count"] if class_info else 0)
        total = sum(counts)
        summary["total_valid_images"] += total
        summary["class_imbalance"][class_name] = {
            "total": total,
            "per_split": dict(zip(summary["splits"].keys(), counts)),
            "ratio": round(total / max(1, summary["total_valid_images"]), 4) if summary["total_valid_images"] else 0.0
        }

    summary["total_images"] = summary["total_valid_images"]

    if summary["classes"]:
        counts = [summary["class_imbalance"][cls]["total"] for cls in summary["classes"]]
        imbalance_values = [count for count in counts if count > 0]
        summary["imbalance_report"] = {
            "min_class_count": min(imbalance_values) if imbalance_values else 0,
            "max_class_count": max(imbalance_values) if imbalance_values else 0,
            "ratio_gap": round((max(imbalance_values) - min(imbalance_values)) / max(1, max(imbalance_values)), 4) if imbalance_values else 0.0
        }

    return summary


def build_class_mapping(class_names: List[str]) -> Dict[str, int]:
    ordered_classes = sorted(class_names)
    return {str(index): class_name for index, class_name in enumerate(ordered_classes)}


def generate_class_config(classes: List[str], output_path: Path) -> Dict:
    mapping = build_class_mapping(classes)
    config = {
        "version": "v1.0",
        "labels": mapping,
        "supported_classes": classes,
        "class_count": len(classes),
        "unknown_label": "Unknown",
        "freshness_classes": ["Fresh", "Moderately Fresh", "Rotten"]
    }
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(config, fh, indent=2)
    return config


def validate_model_training_input(dataset_root: str, output_path: str = "classes.json") -> Dict:
    root = Path(dataset_root)
    analysis = analyze_dataset(root)
    if analysis.get("classes"):
        config = generate_class_config(analysis["classes"], Path(output_path))
        analysis["class_config"] = config
    return analysis


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate dataset structure and generate class configuration.")
    parser.add_argument("--dataset-root", type=str, default="dataset", help="Root folder of the training dataset.")
    parser.add_argument("--output", type=str, default="classes.json", help="Where to save the generated class config JSON.")
    args = parser.parse_args()

    report = validate_model_training_input(args.dataset_root, args.output)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
