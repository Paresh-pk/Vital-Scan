# 20-Question Health Risk Screening Tool

**Objective**: Comprehensive, non-diagnostic screening across physical, digital, and mental health domains.
**Format**: 20 Items, Yes/No Response.
**Total Score Range**: 0 - 20 (Higher = Higher Risk).

## I. Screening Questionnaire

### Domain: Cardiometabolic Health
1.  **Have you ever been treated for or diagnosed with high blood pressure?**
2.  **Have you ever been told you have high blood sugar or diabetes?**
3.  **Do you have a family history of heart disease or stroke?**

### Domain: Digital Eye Strain
4.  **Do you experience dry, tired, or burning eyes on a daily basis?**
5.  **Do you frequently experience headaches after using screens?**

### Domain: Musculoskeletal Health (Back/Neck)
6.  **Do you experience constant stiffness or pain in your neck or shoulders?**
7.  **Do you have lower back pain that worsens after sitting?**

### Domain: Sedentary Lifestyle
8.  **Do you sit for more than 6 hours total per day (work + commute + leisure)?**
9.  **Do you exercise vigorously (sweating/heavy breathing) less than 3 times a week?**

### Domain: Sleep Health
10. **Do you regularly get less than 7 hours of sleep per night?**
11. **Do you take more than 30 minutes to fall asleep, or wake up frequently?**

### Domain: Chronic Stress & Burnout
12. **Do you frequently feel overwhelmed or unable to cope with daily tasks?**
13. **Do you feel emotionally drained or exhausted by your work or studies?**

### Domain: Mental Wellbeing (Anxiety/Depression)
14. **Do you frequently feel nervous, anxious, or on edge?**
15. **Do you feel little interest or pleasure in doing things you used to enjoy?**

### Domain: Digital Habits
16. **Do you check your phone immediately upon waking up or right before sleep?**
17. **Do you feel anxious or restless when you cannot access the internet?**

### Domain: Symptom Signals
18. **Do you experience shortness of breath during mild physical activity?**
19. **Do you suffer from frequent fatigue or low energy, even after resting?**

### Domain: Lifestyle Factors
20. **Do you consume fast food, sugary drinks, or processed snacks >4 times a week?**

---

## II. Scoring Guidance & Interpretation

**Scoring**: Each "Yes" = 1 Point.

| Total Score | Risk Level | Interpretation |
| :--- | :--- | :--- |
| **0 - 4** | **Low Risk** | Healthy baseline. Maintain current habits. |
| **5 - 9** | **Moderate Risk** | Emerging issues. Specific lifestyle changes recommended. |
| **10 - 14** | **Elevated Risk** | Multiple distinct risk factors present. Proactive intervention suggested. |
| **15+** | **High Risk** | Significant burden across domains. Professional consultation advised. |

### Domain-Specific Thresholds
*   **Cardiometabolic**: If Q1 or Q2 is "Yes" → **Traffic Light: RED** (Immediate Medical Attention).
*   **Mental/Burnout**: If Q12-15 sum > 2 → **Traffic Light: YELLOW/RED** (Focus on Stress Management).
*   **Digital**: If Q4-7 sum > 2 → **Traffic Light: YELLOW** (Ergonomics/Vision Check).

## III. Implementation Notes

### Data Collection
*   **Input**: Simple boolean (True/False) array.
*   **Privacy**: No PII required. Data can be processed entirely locally (client-side or local server).
*   **Permissions**: If age/gender are provided beforehand, Q1/Q2/Q9 thresholds can be dynamically adjusted (e.g., higher sleep needs for younger users), but the standard 20 questions remain robust.

### Follow-Up Flow
If **Score > 10**:
1.  Display high-priority domain alerts (e.g., "Primary Concern: Cardiovascular").
2.  Unlock "Deep Dive" modules for specific areas (e.g., detailed sleep log).
3.  Generate a PDF summary for the user to take to a GP.
