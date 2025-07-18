# Pharmedic System – Technical Design Document

**Date:** July 2025  
**Authors:** Intern Team Raheel Sidiqui, Alagappan Alagappan, Fathima Arfa & Emna Arfaoui
**Version:** v0.1 (Draft)

---

##  1. Overview

This document outlines the technical design of the core module integration in the Pharmedic platform. It includes architecture choices, model explainability, and integration strategies for internal APIs.

---

##   2. System Architecture

### 2.1 Architecture Diagram

![System Architecture](./system-architecture.png)

### 2.2 Components

- **Model A – Model Name** (Raheel)
- **Model B – Model Name** (Fathima)
- **Model C – Model Name** (Alagappan)
- **Internal REST API Layer**
- **Mock Input/Output Interface**
- **Data Ingestion (CSV or API)**

---

##  3. Model Explainability

### 🟢 Model A – ADR Risk Classifier

- **Inputs:** SNPs (e.g., rs1799853), adverse drug history  
- **Outputs:** Risk level (e.g., “High”, “Moderate”, “Low”)  
- **Logic:**  
- **Use Case:** 
- **Test cases:** 
- **Model / Features we can add (based on week 2 audit):** 
 



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





