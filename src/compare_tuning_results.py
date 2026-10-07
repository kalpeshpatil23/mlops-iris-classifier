# src/compare_tuning_results.py

"""
Pulls all three tracked runs (baseline, grid search, random search)
from MLflow and prints a consolidated comparison table.
"""

from mlflow.tracking import MlflowClient
import mlflow


# Connect to the local MLflow database
mlflow.set_tracking_uri("sqlite:///mlflow.db")

client = MlflowClient()


# Find the Practical 7 experiment
experiment = client.get_experiment_by_name(
    "iris-hyperparameter-tuning"
)

if experiment is None:
    print("Experiment not found.")
    exit()


# Retrieve all runs
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id]
)


print(
    f"{'Run Name':<32}"
    f"{'CV f1_macro':<15}"
    f"{'Test Accuracy':<15}"
    f"{'Total Fits':<12}"
)

print("-" * 74)


for run in sorted(
    runs,
    key=lambda r: r.data.tags.get(
        "mlflow.runName",
        ""
    )
):

    name = run.data.tags.get(
        "mlflow.runName",
        "unknown"
    )

    # Baseline uses cv_f1_macro_mean.
    # Search runs use best_cv_f1_macro.
    cv_score = run.data.metrics.get(
        "cv_f1_macro_mean",
        run.data.metrics.get(
            "best_cv_f1_macro",
            0
        )
    )

    test_acc = run.data.metrics.get(
        "test_accuracy",
        0
    )

    # Grid Search has total_combinations.
    # Random Search has n_iter.
    # Baseline has neither, so it uses 5 fits.
    n_iter = (
        run.data.params.get("total_combinations")
        or run.data.params.get("n_iter")
        or "1"
    )

    if name == "baseline_decision_tree":
        total_fits = 5
    else:
        total_fits = int(n_iter) * 5

    print(
        f"{name:<32}"
        f"{cv_score:<15.4f}"
        f"{test_acc:<15.4f}"
        f"{total_fits:<12}"
    )