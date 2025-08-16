# 🧪 Model B Evaluation Summary

**Model Name**:  
**Intern**: [Intern's Name]  
**Date**: [YYYY-MM-DD]  

---

## ✅ 1. Internal Accuracy (Using Training/Validation Data)

| Metric        | Value         |
|---------------|---------------|
| Accuracy      | [e.g. 84%]    |
| Precision     | [e.g. 0.76]   |
| Recall        | [e.g. 0.81]   |
| F1 Score      | [e.g. 0.79]   |
| Validation Method | [Cross-validation / held-out set / other] |

**Notes:**
- The model was evaluated on [#] training examples.
- [Mention if data imbalance or label noise was present.]

---

## 🧪 2. Manual Evaluation with Mock Patients

**File Reference**: `tests/mock-patients.json`  
**Test Count**: [5 / 10] manually crafted inputs

| Patient ID | Expected Drugs             | Model Output                | Match Score |
|------------|----------------------------|-----------------------------|-------------|
| 001        | azithromycin, clarithromycin | azithromycin, erythromycin | 1/2 (50%)   |
| 002        | amoxicillin, cephalexin     | amoxicillin, cephalexin     | 2/2 (100%)  |
| 003        | ...                        | ...                         | ...         |

**Manual Accuracy (Average)**: **[e.g. 70%]**  
**Test Highlights**:
- ✅ 3/5 cases had at least 1 correct recommendation
- ✅ 2/5 cases had full match
- ❌ 1/5 case returned a risky/inappropriate drug

---

## 🔍 3. Observations

- **Allergy Handling**: [e.g. Model sometimes recommends drugs the patient is allergic to]
- **Edge Cases**: [e.g. Fails for multi-condition patients]
- **Stability**: [e.g. Similar input gives different output]

---

## 🧠 4. Takeaways & Next Steps

- Accuracy is promising, but manual checks revealed:
  - [e.g. Drug ranking needs improvement]
  - [e.g. Allergy logic must be enforced before suggesting drugs]

- Next Step Suggestions:
  - ✅ Add rule-based pre-filter for allergic drugs
  - ✅ Improve interpretability (log drug scores)
  - ✅ Continue testing with more complex patients

---

