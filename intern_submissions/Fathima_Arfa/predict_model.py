import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

# --- Part 1: Prediction on a Single Sample ---

# Load the trained model
# Adjust the path if the script is not run from the root directory
model_path = "intern_submissions/Fathima_Arfa/adr_model_xgboost.joblib"
model = joblib.load(model_path)

# The model was trained on 100 features (the top 100 most frequent side effects).
# We need to create a sample input with the same number of features.
# This sample represents a drug's side-effect profile (1 for presence, 0 for absence).
# For demonstration, we'll create a random binary vector.
np.random.seed(42)
sample_input = np.random.randint(2, size=(1, 100))

# Make a prediction
# The model predicts whether the "abdominal pain" ADR is present (1) or not (0).
prediction = model.predict(sample_input)
prediction_proba = model.predict_proba(sample_input)

# Map numeric prediction to a meaningful label
prediction_label = 'Abdominal Pain Present' if prediction[0] == 1 else 'Abdominal Pain Not Present'

print("--- ADR Prediction for Sample Drug Profile ---")
print(f"Sample Input Shape: {sample_input.shape}")
print("\nPrediction:")
print(f"  - Numeric Output: {prediction[0]}")
print(f"  - Predicted Label: {prediction_label}")
print("\nPrediction Probabilities:")
print(f"  - P(Not Present): {prediction_proba[0][0]:.4f}")
print(f"  - P(Present):     {prediction_proba[0][1]:.4f}")
print("\n" + "="*50 + "\n")


# --- Part 2: Optional Evaluation on a Test Set ---

print("--- Optional: Evaluating Model Accuracy on Test Set ---")

# To evaluate, we need to load and prepare the test data just as in the notebook.
# This assumes 'meddra_all_se.tsv' is in the same directory or accessible.
try:
    # 1. Load and pivot the original data
    df = pd.read_csv("meddra_all_se.tsv", sep="\t", header=None,
                     names=["drug_id", "umls_id", "side_effect_name",
                            "frequency", "placebo", "meddra_code"])
    binary_df = pd.crosstab(df.drug_id, df.side_effect_name).clip(0, 1)

    # 2. Recreate the exact 300-drug subset used for evaluation in the notebook
    subset = binary_df.sample(300, random_state=42)
    top100 = subset.sum(axis=0).nlargest(100).index.tolist()
    
    # This is our test set
    X_test = subset[top100].reset_index(drop=True)
    
    # Define the target ADR and get the true labels for the test set
    target = "C0000737"  # Abdominal pain
    y_test = subset[target].values
    
    print(f"Test set loaded successfully. Shape: {X_test.shape}")

    # 3. Make predictions on the entire test set
    y_pred = model.predict(X_test)

    # 4. Calculate and print the accuracy and a detailed classification report
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"\nAccuracy on the 300-drug test set: {accuracy:.4f}")
    print("\nFull Classification Report:")
    print(report)

except FileNotFoundError:
    print("\nCould not perform evaluation: 'meddra_all_se.tsv' not found.")
except Exception as e:
    print(f"\nAn error occurred during evaluation: {e}")