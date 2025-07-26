# Pharmedic System – Technical Design Document

**Date:** July 2025  
**Authors:** Intern Team Raheel Sidiqui, Alagappan Alagappan, Fathima Arfa & Emna Arfaoui
**Version:** v0.1 (Draft)

---

## 1. Overview

This document outlines the technical design of the core module integration in the Pharmedic platform. It includes architecture choices, model explainability, and integration strategies for internal APIs.

---

## 2. System Architecture

### 2.1 Architecture Diagram

![System Architecture](./system-architecture.png)

### 2.2 Components

- **Model A – ADR Risk Classifier** (Raheel)
- **Model B – Model Name** (Fathima)
- **Model C – Model Name** (Alagappan)
- **Internal REST API Layer**
- **Mock Input/Output Interface**
- **Data Ingestion (CSV or API)**

---

## 3. Model Explainability

### 🟢 Model A (Raheel) – ADR Risk Classifier

- **Inputs:**
  `drug_name` (string) — preferred, human‑readable lookup key.  
  `stitch_id` (string) — alternative identifier if `drug_name` isn’t provided.

  Derived internal feature set:
  adr_vector[25] — 25‑element binary vector flagging the presence of the top‑25 ADRs (built from meddra_all_se.tsv).
  num_adrs — integer count of unique ADRs linked to the drug.

- **Outputs:**
  `risk_score` (float, 0 – 1) — XGBoost probability that “Insomnia” is an ADR for this drug.  
  `risk_level` (enum Low / Moderate / High) — buckets by score (≤ 0.33 Low; ≤ 0.66 Moderate; > 0.66 High).  
  `cluster_id` (int) — K‑means group label (k = 3).  
  `classifier` (string) — which model ran (“xgboost”).

- **Logic:**

  1. Receive `{ "drug_name": … }` or `{ "stitch_id": … }`.
  2. Look up drug in `drug_names.tsv`.
  3. Assemble the 25‑dim ADR vector + `num_adrs`.
  4. Predict `cluster_id` via pre‑fit KMeans.
  5. Pick `xgboost` model for that cluster.
  6. Compute `risk_score` = `model.predict_proba(...)[:,1]`.
  7. Map score → `risk_level`.
  8. Return `{ drug_name, cluster_id, classifier, risk_score, risk_level }`.

- **Use Case Scenario:**: A UAE community pharmacist scans a new prescription for Methylphenidate. The ADR‑Risk API returns risk_level "High" for insomnia, prompting the pharmacist to advise the patient on evening dosing and sleep monitoring.

- **Test cases:** (At Risk for Insomnia)
  | Test Case | Input | Expected Risk Level |
  |-----------|----------------------------------|----------------------|
  | TC‑01 | `{ "drug_name": "Paracetamol" }` | Low |
  | TC‑02 | `{ "drug_name": "Methylphenidate" }` | High |
  | TC‑03 | `{ "drug_name": "Clozapine" }` | Moderate |

- **REST API Specifications:**

  - #### Endpoint

  #### `POST /api/v1/adr-risk`

  - #### Headers

  #### `Content-Type: application/json`

  ***

  - #### Request Body

  ```json
  {
    "drug_name": "Ibuprofen" // or "stitch_id": "CID00133867"
  }
  ```

  - #### Successful Response

  ```json
  {
    "drug_name": "Ibuprofen",
    "cluster_id": 0,
    "classifier": "xgboost",
    "risk_score": 0.18,
    "risk_level": "Low",
    "timestamp": "2025-07-17T15:40:10Z"
  }
  ```

  - #### Error Response

  ```json
  {
    "error": "drug_not_found",
    "message": "Drug name 'Xyzalol' not present in database."
  }
  ```

- **Model / Features we can add (based on week 2 audit):**
- Integrate a SHAP-based interpretability layer:
  Deploy `shap.TreeExplainer` on the trained XGBoost booster so each API response includes a feature attribution vector.  
  Pharmacists will see the top 5 contributors (sorted by absolute SHAP value) that drove the risk score.

- Automated feature-pruning post-train hook:
  After fitting, run a `SelectFromModel` (threshold set via global SHAP importance) to filter out low signal columns.  
  This keeps the feature space breif, improves inference latency, and guards against overfitting.

- Upgrade to a multi-output side-effect predictor:
  Wrap XGBoost in `MultiOutputClassifier`so the pipeline emits a risk vector for several ADR labels eg: `[insomnia, nausea, headache]` rather than just one eg: `[insomnia]`.

=======

### 🟢 Model A (Raheel) – ADR Risk Classifier
### 🟢 Model A (Raheel) – ADR Risk Classifier

- **Inputs:**
  `drug_name` (string) — preferred, human‑readable lookup key.  
  `stitch_id` (string) — alternative identifier if `drug_name` isn’t provided.

  Derived internal feature set:
  adr_vector[25] — 25‑element binary vector flagging the presence of the top‑25 ADRs (built from meddra_all_se.tsv).
  num_adrs — integer count of unique ADRs linked to the drug.

- **Outputs:**
  `risk_score` (float, 0 – 1) — XGBoost probability that “Insomnia” is an ADR for this drug.  
  `risk_level` (enum Low / Moderate / High) — buckets by score (≤ 0.33 Low; ≤ 0.66 Moderate; > 0.66 High).  
  `cluster_id` (int) — K‑means group label (k = 3).  
  `classifier` (string) — which model ran (“xgboost”).

- **Logic:**

  1. Receive `{ "drug_name": … }` or `{ "stitch_id": … }`.
  2. Look up drug in `drug_names.tsv`.
  3. Assemble the 25‑dim ADR vector + `num_adrs`.
  4. Predict `cluster_id` via pre‑fit KMeans.
  5. Pick `xgboost` model for that cluster.
  6. Compute `risk_score` = `model.predict_proba(...)[:,1]`.
  7. Map score → `risk_level`.
  8. Return `{ drug_name, cluster_id, classifier, risk_score, risk_level }`.

- **Use Case Scenario:**: A UAE community pharmacist scans a new prescription for Methylphenidate. The ADR‑Risk API returns risk_level "High" for insomnia, prompting the pharmacist to advise the patient on evening dosing and sleep monitoring.

- **Test cases:** (At Risk for Insomnia)
  | Test Case | Input | Expected Risk Level |
  |-----------|----------------------------------|----------------------|
  | TC‑01 | `{ "drug_name": "Paracetamol" }` | Low |
  | TC‑02 | `{ "drug_name": "Methylphenidate" }` | High |
  | TC‑03 | `{ "drug_name": "Clozapine" }` | Moderate |

- **REST API Specifications:**

  - #### Endpoint

  #### `POST /api/v1/adr-risk`

  - #### Headers

  #### `Content-Type: application/json`

  ***

  - #### Request Body

  ```json
  {
    "drug_name": "Ibuprofen" // or "stitch_id": "CID00133867"
  }
  ```

  - #### Successful Response

  ```json
  {
    "drug_name": "Ibuprofen",
    "cluster_id": 0,
    "classifier": "xgboost",
    "risk_score": 0.18,
    "risk_level": "Low",
    "timestamp": "2025-07-17T15:40:10Z"
  }
  ```

  - #### Error Response

  ```json
  {
    "error": "drug_not_found",
    "message": "Drug name 'Xyzalol' not present in database."
  }
  ```

- **Model / Features we can add (based on week 2 audit):**
- Integrate a SHAP-based interpretability layer:
  Deploy `shap.TreeExplainer` on the trained XGBoost booster so each API response includes a feature attribution vector.  
  Pharmacists will see the top 5 contributors (sorted by absolute SHAP value) that drove the risk score.

- Automated feature-pruning post-train hook:
  After fitting, run a `SelectFromModel` (threshold set via global SHAP importance) to filter out low signal columns.  
  This keeps the feature space breif, improves inference latency, and guards against overfitting.

- Upgrade to a multi-output side-effect predictor:
  Wrap XGBoost in `MultiOutputClassifier`so the pipeline emits a risk vector for several ADR labels eg: `[insomnia, nausea, headache]` rather than just one eg: `[insomnia]`.



 ### 🟡 Model B – Abdominal Pain Risk Predictor

**Inputs:**  
- SNPs (e.g., rs1799853, rs4342461)  
- Clinical history (e.g., prior abdominal pain, drug exposure)  
- Age and sex (if available)  

**Outputs:**  
- Predicted risk level for abdominal pain: “High”, “Moderate”, “Low”  
- Confidence score  

**Logic:**  
1. Collect genetic and clinical input features  
2. Encode and normalize inputs  
3. Reference known ADR and pain-associated SNP mappings  
4. Predict abdominal pain risk using a trained classifier (e.g., XGBoost)  
5. Return risk level and optional confidence score  

**Use Case:**  
A 55-year-old patient with SNP rs4342461 and prior gastrointestinal issues is evaluated for Drug X.  
The model predicts “High risk of abdominal pain,” guiding the clinician to prescribe an alternative.

**Test Cases:**  

| SNPs             | History                 | Expected Risk |
|------------------|--------------------------|----------------|
| rs1799853        | No prior pain           | Moderate       |
| None             | Abdominal pain w/ Drug Y | High           |
| rs123, rs456     | Mild GI symptoms         | Low            |


**Model / Features We Can Add:**  
- Expand to predict other ADRs (e.g., nausea, rash)  
- Include SHAP-based explanations  
- Add comorbidity and demographic interactions

### 🔌 Sample API – Abdominal Pain Risk Predictor

```http
POST /api/abdominal-pain-risk

Body:
{
  "snp_data": ["rs4342461", "rs1799853"],
  "history": ["abdominal pain after Drug Y", "GI issues"],
  "age": 55,
  "sex": "female",
  "drug_label": "Drug X"
}

Response:
{
  "risk_level": "High",
  "confidence": 0.91,
  "explanation": {
    "rs4342461": 0.38,
    "GI issues": 0.29
  }
}
```

