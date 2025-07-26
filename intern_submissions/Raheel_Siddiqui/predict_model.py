from pathlib import Path
import joblib
import numpy as np

def get_risk_level(score: float) -> str:
    if score <= 0.33:
        return "Low"
    elif score <= 0.66:
        return "Moderate"
    else:
        return "High"

BASE = Path().resolve()
model_file = BASE / "intern_submissions" / "Raheel_Siddiqui" / "Raheel-ADRmodel.joblib"

model = joblib.load(model_file)

sample_input = np.array([[4], [54], [74], [164]])

predictions = model.predict(sample_input)
print("Prediction for sample input:", predictions)

if hasattr(model, "predict_proba"):
    probs = model.predict_proba(sample_input)[:, 1]
    risk_levels = [get_risk_level(score) for score in probs]
    for i, (inp, pred, prob, risk) in enumerate(zip(sample_input, predictions, probs, risk_levels)):
        print(f"Input: {inp[0]}, Prediction: {pred}, Probability: {prob:.3f}, Risk Level: {risk}")
else:
    print("Model does not support probability prediction.")
