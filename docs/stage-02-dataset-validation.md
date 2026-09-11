# Stage 2: Dataset Validation and Preprocessing

## Objective

This stage prepares the dataset pipeline before training begins. It validates the folder structure, checks image integrity, and generates a dynamic class map that the ML model can use during training and inference.

## What this stage covers

- Detecting train/validation/test directories
- Listing class folders and counting valid images
- Detecting corrupted files and invalid file types
- Highlighting missing classes across splits
- Reporting class imbalance
- Generating a class configuration file
- Preventing obvious dataset leakage by separating classes and splits

## Dataset validation requirements

The validator supports common dataset layouts such as:

- dataset/train/apple
- dataset/validation/banana
- dataset/test/tomato

and freshness-specific structures such as:

- dataset/train/apple_fresh
- dataset/train/apple_rotten

## Script usage

```bash
python ml/dataset_validator.py --dataset-root dataset --output classes.json
```

## Expected output

The script prints a JSON report with:

- dataset structure
- available classes
- split-wise image counts
- corrupted image list
- missing class warnings
- class imbalance totals
- generated class mapping

## Preprocessing approach

The preprocessor resizes images to a standard input shape, converts them to RGB, and normalizes pixel values to the range 0-1. This keeps the pipeline compatible with transfer-learning backbones such as MobileNetV2 or EfficientNetB0.

## Notes

This stage is intentionally dataset-independent. It reads the actual structure and creates model configuration from discovered data instead of hard-coding a fixed list of produce types.
