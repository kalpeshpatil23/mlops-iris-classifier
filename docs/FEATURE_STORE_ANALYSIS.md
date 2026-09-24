# Feature Store Analysis

## 1. Introduction

This experiment introduced Feast as an open-source feature store for the Iris
machine learning project. The experiment demonstrated feature registration,
online and offline feature retrieval, point-in-time correctness, feature
reusability, and centralized feature management.

## 2. Feature Store Architecture

The feature store contains two logically consistent storage layers:

- Offline store: Used for historical feature retrieval and training dataset
  construction.
- Online store: Used for low-latency feature retrieval during inference.

In this experiment, Feast uses the local Parquet source for historical data
and SQLite as the online store.

## 3. Training-Serving Consistency

The same registered feature definitions were used for both offline and online
retrieval.

The engineered features included:

- sepal_area
- petal_area
- sepal_to_petal_length_ratio
- petal_length_bin

Because these features were registered once in `features.py`, the same feature
definitions were available through both the historical retrieval API and the
online retrieval API.

This reduces the risk of training-serving skew caused by implementing the
same feature transformation separately in different parts of an ML system.

## 4. Point-in-Time Correctness

Historical feature retrieval was demonstrated using Feast's
`get_historical_features()` API.

The entity DataFrame contained both `sample_id` and `event_timestamp`.
Feast used these timestamps to retrieve feature values corresponding to the
appropriate point in time.

This approach helps prevent future-data leakage when constructing training
datasets from historical data.

## 5. Feature Reusability

The `iris_feature_service` was created as a reusable collection of the
registered Iris features.

The feature service was accessed from a separate Python program without
reimplementing the feature calculations.

This demonstrates how multiple ML models or tasks can reuse the same validated
feature definitions.

## 6. Centralized Feature Governance

The `features.py` file acts as the central definition of:

- Entity
- Data source
- Feature views
- Feature schemas
- TTL
- Feature service

This provides a single source of truth for the features used by consuming
ML applications.

## 7. Observations

The following results were successfully observed:

1. Feast successfully registered the `sample_id` entity.
2. Two feature views were registered:
   - `iris_measurements`
   - `iris_engineered_features`
3. The `iris_feature_service` was successfully registered.
4. Features were materialized into the SQLite online store.
5. Online retrieval returned all requested features for `sample_id = 1`.
6. Historical retrieval returned five point-in-time-correct feature records.
7. The same registered features were reusable through the feature service.

## 8. Conclusion

The experiment demonstrated the main benefits of using a Feature Store in an
MLOps workflow: centralized feature definitions, reusable features,
consistent online and offline retrieval, and point-in-time-correct historical
feature access.

Feast provides a structured mechanism for separating feature management from
individual model implementations, making feature usage more consistent and
maintainable across ML workflows.
