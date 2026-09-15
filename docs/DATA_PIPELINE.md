# Data Pipeline Documentation

## 1. Overview

This document describes the end-to-end data pipeline implemented for the MLOps Iris Classifier project.

The pipeline consists of four stages:

```text
Collect
   |
   v
Preprocess
   |
   v
Feature Engineering
   |
   v
Validate
```

The pipeline is automated using DVC. Each stage has clearly defined dependencies and outputs in `dvc.yaml`.

---

## 2. Pipeline Stages

| Stage               | Purpose                                           | Input                                  | Output                                 |
| ------------------- | ------------------------------------------------- | -------------------------------------- | -------------------------------------- |
| Collect             | Obtain raw Iris data                              | scikit-learn Iris dataset              | `data/raw/iris_raw.csv`                |
| Preprocess          | Clean and prepare the data                        | `data/raw/iris_raw.csv`                | `data/processed/iris_preprocessed.csv` |
| Feature Engineering | Create additional model-useful features           | `data/processed/iris_preprocessed.csv` | `data/processed/iris_features.csv`     |
| Validate            | Check schema, nulls, categories, and value ranges | `data/processed/iris_features.csv`     | Validation result                      |

---

## 3. Stage 1: Data Collection

### Purpose

The collection stage obtains the Iris dataset using scikit-learn and saves it as a raw CSV file.

### Script

`src/pipeline/collect.py`

### Input

The Iris dataset provided by scikit-learn.

### Output

`data/raw/iris_raw.csv`

### Processing

The stage:

* Loads the Iris dataset.
* Converts it into a pandas DataFrame.
* Converts numeric target values into species names.
* Adds a collection timestamp.
* Saves the resulting data as a CSV file.

The collection stage produced 150 rows.

---

## 4. Stage 2: Data Preprocessing

### Purpose

The preprocessing stage cleans the raw data before feature engineering.

### Script

`src/pipeline/preprocess.py`

### Input

`data/raw/iris_raw.csv`

### Output

`data/processed/iris_preprocessed.csv`

### Processing

The stage:

* Removes exact duplicate records.
* Converts numeric columns to numeric data types.
* Handles missing numeric values using median imputation.
* Removes rows with missing target values.
* Removes the collection timestamp because it is not required for modeling.

During execution, one duplicate row was removed.

Final output:

* 149 rows
* Original Iris measurement columns
* Species target column

---

## 5. Stage 3: Feature Engineering

### Purpose

The feature engineering stage creates additional features that may provide useful information for machine learning.

### Script

`src/pipeline/features.py`

### Input

`data/processed/iris_preprocessed.csv`

### Output

`data/processed/iris_features.csv`

### Features Created

The pipeline creates:

1. `sepal_area`

   Calculated as:

   `sepal length × sepal width`

2. `petal_area`

   Calculated as:

   `petal length × petal width`

3. `sepal_to_petal_length_ratio`

   Calculated as:

   `sepal length / petal length`

4. `petal_length_bin`

   Petal length is divided into three categories:

   * short
   * medium
   * long

The final dataset contains 9 columns.

---

## 6. Stage 4: Data Validation

### Purpose

The validation stage ensures that the processed data satisfies predefined quality requirements before it can be used downstream.

### Script

`src/pipeline/validate.py`

### Input

`data/processed/iris_features.csv`

### Validation Rules

#### Schema Validation

The following columns are expected:

* `sepal length (cm)`
* `sepal width (cm)`
* `petal length (cm)`
* `petal width (cm)`
* `species`
* `sepal_area`
* `petal_area`
* `sepal_to_petal_length_ratio`
* `petal_length_bin`

#### Null Validation

The pipeline checks that there are no unexpected null values.

#### Species Validation

Only the following species values are accepted:

* `setosa`
* `versicolor`
* `virginica`

#### Range Validation

The following ranges are enforced:

| Column              | Minimum | Maximum |
| ------------------- | ------: | ------: |
| `sepal length (cm)` |     3.0 |     9.0 |
| `sepal width (cm)`  |     1.5 |     5.5 |
| `petal length (cm)` |     0.5 |     8.0 |
| `petal width (cm)`  |    0.05 |     3.0 |

If any validation rule fails, the pipeline raises a `DataValidationError` and exits with status code 1.

A successful validation exits with status code 0.

---

## 7. DVC Pipeline Dependency Graph

The DVC pipeline is defined in `dvc.yaml`.

```text
+---------+
| collect |
+---------+
     |
     v
+------------+
| preprocess |
+------------+
     |
     v
+----------+
| features |
+----------+
     |
     v
+----------+
| validate |
+----------+
```

The dependencies are:

```text
collect -> preprocess
preprocess -> features
features -> validate
```

DVC uses these dependencies to determine which stages need to be executed.

---

## 8. Pipeline Automation

The complete pipeline can be executed using:

```bash
dvc repro
```

DVC checks the dependencies and outputs of each stage.

If a dependency has changed, the affected stage and its downstream stages are re-executed.

If nothing has changed, DVC skips the stages.

For example, after the first successful execution, running:

```bash
dvc repro
```

again produced:

```text
Stage 'collect' didn't change, skipping
Stage 'preprocess' didn't change, skipping
Stage 'features' didn't change, skipping
Stage 'validate' didn't change, skipping

Data and pipelines are up to date.
```

This demonstrates DVC's dependency-based caching.

---

## 9. Validation Failure Test

To verify that validation correctly prevents invalid data from passing downstream, the value of `sepal length (cm)` was temporarily changed to `50`.

The allowed range is 3.0 to 9.0.

The validation stage detected the invalid value and produced:

```text
1 rows out of expected range for 'sepal length (cm)' (3.0-9.0)
Pipeline halted: Validation failed with 1 error(s)
```

The process exited with status code:

```text
1
```

After restoring the correct data, validation passed successfully with exit code:

```text
0
```

This demonstrates that the validation stage can detect invalid data and stop the pipeline.

---

## 10. Pipeline Outputs

The pipeline produces the following data artifacts:

```text
data/
├── raw/
│   └── iris_raw.csv
│
└── processed/
    ├── iris_preprocessed.csv
    └── iris_features.csv
```

The pipeline definition is stored in:

`dvc.yaml`

The exact pipeline state and dependency/output hashes are stored in:

`dvc.lock`

---

## 11. Conclusion

The Experiment 4 pipeline provides a reproducible and automated workflow for collecting, preprocessing, feature engineering, and validating Iris data.

The pipeline is modular because each processing stage is implemented as a separate Python script.

DVC provides dependency tracking, pipeline automation, caching, and reproducibility.

The validation stage provides a defensive quality check that prevents invalid data from silently flowing into downstream machine learning processes.
