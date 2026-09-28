# src/register_best_model.py

"""
Find the best MLflow run based on f1_macro
and register its trained model in the MLflow Model Registry.
"""

import os
import mlflow

from mlflow.tracking import MlflowClient


# =========================================================
# 1. Configure MLflow
# =========================================================

mlflow.set_tracking_uri(
    os.getenv(
        "MLFLOW_TRACKING_URI",
        "http://127.0.0.1:5000"
    )
)

client = MlflowClient()


# =========================================================
# 2. Find the Experiment
# =========================================================

experiment_name = "iris-classification-baseline"

experiment = client.get_experiment_by_name(
    experiment_name
)

if experiment is None:
    raise RuntimeError(
        f"Experiment '{experiment_name}' not found."
    )

experiment_id = experiment.experiment_id

print("=" * 60)
print("EXPERIMENT FOUND")
print("=" * 60)

print("Experiment Name:", experiment_name)
print("Experiment ID:", experiment_id)


# =========================================================
# 3. Find the Best Run
# =========================================================

runs = client.search_runs(
    experiment_ids=[experiment_id],
    order_by=["metrics.f1_macro DESC"]
)

if not runs:
    raise RuntimeError(
        "No runs found in the experiment."
    )

best_run = runs[0]

best_run_id = best_run.info.run_id

best_f1 = best_run.data.metrics["f1_macro"]

best_model_type = best_run.data.params["model_type"]


print("\n" + "=" * 60)
print("BEST RUN")
print("=" * 60)

print("Run ID:", best_run_id)
print("Model:", best_model_type)
print("F1 Score:", best_f1)


# =========================================================
# 4. Register the Best Model
# =========================================================

model_uri = f"runs:/{best_run_id}/model"

registered_model_name = "iris-classifier-prod"


print("\n" + "=" * 60)
print("REGISTERING MODEL")
print("=" * 60)

print("Model URI:", model_uri)
print("Registered Model Name:", registered_model_name)


model_version = mlflow.register_model(
    model_uri=model_uri,
    name=registered_model_name
)


print("\n" + "=" * 60)
print("MODEL REGISTERED SUCCESSFULLY")
print("=" * 60)

print("Model Name:", registered_model_name)
print("Version:", model_version.version)


# =========================================================
# 5. Move Model to Staging
# =========================================================

client.transition_model_version_stage(
    name=registered_model_name,
    version=model_version.version,
    stage="Staging"
)


print("\n" + "=" * 60)
print("MODEL MOVED TO STAGING")
print("=" * 60)

print(
    f"Model URI: models:/{registered_model_name}/Staging"
)
