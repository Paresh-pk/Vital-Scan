# Privacy Impact Assessment (PIA) - Self Audit

**Project**: Santinel AI Disease Risk Tool
**Date**: 2026-02-02
**Version**: 1.0

## 1. Data Collection & Minimization
| Data Point | Necessity | PII Status | Handling |
| :--- | :--- | :--- | :--- |
| **Age** | Required for Risk Model (NHANES) | Quasi-Identifier | Processed ephemeral, stored encrypted. |
| **Gender** | Required for Risk Model | Quasi-Identifier | Processed ephemeral, stored encrypted. |
| **IP Address** | Server Logs | Metadata | **ACTION**: Disable access logs in production or anonymize. |
| **Name/Email** | Not Collected | Direct PII | **Strictly Prohibited**. |

## 2. Storage Security
*   **Mechanism**: Local File Storage (`data/assessments.enc`).
*   **Encryption**: AES-128 (Fernet Implementation).
*   **Key Management**: Key stored locally (`data/secret.key`). *Note: In production, use AWS KMS/Azure Key Vault.*

## 3. Algorithm Transparency
*   **Models**: XGBoost (Tree-based).
*   **Explainability**: Feature Importance is interpretable.
*   **"Black Box" Risk**: Low. We do not use Deep Learning for the core risk score. LLM is only used for *text generation*, not *decision making*.

## 4. Regulatory Compliance Checks
*   [x] **GDPR Art. 22 (Automated Decision Making)**: User explicitly requests the assessment. Result is "Guidance", not "Legal Effect".
*   [x] **HIPAA**: App is "Direct to Consumer" (Non-Covered Entity), but follows HIPAA Security Rule best practices (Encryption).
*   [x] **FDA (SaMD)**: Software as a Medical Device.
    *   *Exemption*: General Wellness Policy.
    *   *Constraint*: Must not "diagnose, cure, mitigate, treat, or prevent harm".
    *   *Mitigation*: Strict labeling "ESTIMATE ONLY".

## 5. Risk Mitigation Strategy
*   **Risk**: User panics due to "High Risk" label.
*   **Mitigation**: UI always displays "Consult a Physician" button on High Risk cards.
