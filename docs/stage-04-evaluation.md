# Stage 4: Model Evaluation and Metrics

## Objective

This stage loads the trained model, evaluates it on the test dataset, and records metrics from actual execution. No fabricated accuracy or fake results are used.

## What this stage covers

- Loading the saved model
- Evaluating predictions on the test split
- Calculating accuracy, precision, recall, and F1-score
- Generating a confusion matrix
- Producing a classification report per class
- Saving evaluation output to the results directory

## Script usage

```bash
python ml/evaluate.py --dataset-root dataset --model-path ml/models/freshness_model.keras --output-dir results --class-config classes.json
```

## Outputs generated

- results/evaluation_metrics.json
- results/confusion_matrix.png

## Metrics used

The evaluation script computes metrics using scikit-learn:

- accuracy_score
- precision_score
- recall_score
- f1_score
- confusion_matrix
- classification_report

## Notes

This stage is intentionally grounded in real model execution. Only the metrics produced by the trained model are included in the results.
