# Hyperparameter Tuning Analysis

## 1. Baseline Model

### Model
DecisionTreeClassifier with default hyperparameters.

### Cross-Validation
5-fold cross-validation was used with F1 Macro as the scoring metric.

### Results

- CV F1 Macro: **0.9663**
- CV F1 Macro Standard Deviation: **0.0316**
- Test Accuracy: **0.9000**
- Total Fits: **5**

The baseline model provides a reference point for evaluating the benefit of hyperparameter tuning.

---

## 2. Grid Search

### Model
RandomForestClassifier.

### Search Method
GridSearchCV with 5-fold cross-validation.

### Hyperparameter Grid

- `n_estimators`: 50, 100, 200
- `max_depth`: 3, 5, 10, None
- `min_samples_split`: 2, 5, 10
- `max_features`: sqrt, log2

The grid contains:

**3 × 4 × 3 × 2 = 72 combinations**

With 5-fold cross-validation:

**72 × 5 = 360 total fits**

### Best Hyperparameters

- `n_estimators`: 50
- `max_depth`: 3
- `min_samples_split`: 2
- `max_features`: sqrt

### Results

- Best CV F1 Macro: **0.9663**
- Test Accuracy: **0.9667**
- Total Fits: **360**

Compared with the baseline, the Grid Search Random Forest achieved the same CV F1 Macro but improved test accuracy from **0.9000 to 0.9667**.

---

## 3. Random Search

### Model
RandomForestClassifier.

### Search Method
RandomizedSearchCV with 5-fold cross-validation.

### Search Budget

Random Search evaluated **30 randomly selected combinations**.

With 5-fold cross-validation:

**30 × 5 = 150 total fits**

### Best Hyperparameters

- `n_estimators`: 100
- `max_depth`: 3
- `min_samples_split`: 6
- `max_features`: sqrt

### Results

- Best CV F1 Macro: **0.9663**
- Test Accuracy: **0.9667**
- Total Fits: **150**

Random Search achieved exactly the same CV F1 Macro and test accuracy as Grid Search while requiring substantially fewer model fits.

---

## 4. Comparative Analysis

| Method | Model | CV F1 Macro | Test Accuracy | Total Fits |
|---|---|---:|---:|---:|
| Baseline | Decision Tree | 0.9663 | 0.9000 | 5 |
| Grid Search | Random Forest | 0.9663 | 0.9667 | 360 |
| Random Search | Random Forest | 0.9663 | 0.9667 | 150 |

The baseline Decision Tree achieved a CV F1 Macro of **0.9663** and a test accuracy of **0.9000**.

Grid Search exhaustively evaluated all **72 hyperparameter combinations**, resulting in **360 model fits**. Its best Random Forest achieved a CV F1 Macro of **0.9663** and test accuracy of **0.9667**.

Random Search evaluated only **30 combinations**, resulting in **150 model fits**. It achieved the same best CV F1 Macro of **0.9663** and the same test accuracy of **0.9667**.

Therefore, in this experiment, Random Search was more computationally efficient than Grid Search. It achieved identical observed performance using **150 fits instead of 360**, which is approximately **58.3% fewer model fits**.

The tuned Random Forest models also improved test accuracy over the baseline Decision Tree by **0.0667**, or **6.67 percentage points**.

---

## 5. Conclusion

Both Grid Search and Random Search successfully tuned the Random Forest model.

Grid Search provides exhaustive coverage of the specified hyperparameter grid, while Random Search explores a smaller number of randomly selected configurations.

For this experiment, Random Search was the more efficient approach because it achieved the same CV F1 Macro and test accuracy as Grid Search while using less than half the number of model fits.

The final comparison demonstrates the importance of MLflow tracking because all three experiments and their results can be reviewed and compared from a single experiment record.