document.getElementById('healthForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    // --- 1. Gather & Compute Data ---

    // Body Metrics
    const weight = parseFloat(document.getElementById('weight').value);
    const heightCm = parseFloat(document.getElementById('height').value);
    const heightM = heightCm / 100;
    const bmi = +(weight / (heightM * heightM)).toFixed(1);

    // Inferences for ML (Mapping 20Q to required fields)
    const hasHighBP = document.getElementById('q1_bp_history').value === 'true';
    const estSystolicBP = hasHighBP ? 145 : 120; // 130 is elevated threshold

    const hasDiabetes = document.getElementById('q2_diabetes_history').value === 'true';
    const estHbA1c = hasDiabetes ? 7.2 : 5.4;

    const estCholesterol = 190; // Default

    // Logic for Q9 (Inactive) -> Vigorous (False if inactive)
    const isInactive = document.getElementById('q9_inactive').value === 'true';

    // Logic for Q10 (Low Sleep) -> Sleep (6.0 if low, 7.5 if normal)
    const isLowSleep = document.getElementById('q10_low_sleep').value === 'true';

    const formData = {
        // Vitals for ML
        age: parseInt(document.getElementById('age').value),
        gender: parseInt(document.getElementById('gender').value),
        bmi: bmi,
        systolic_bp: estSystolicBP,
        hba1c: estHbA1c,
        cholesterol: estCholesterol,
        vigorous_activity: !isInactive, // Inverted
        sleep_hours: isLowSleep ? 5.5 : 7.5,
        smoker_history: document.getElementById('smoker_history').value === 'true',

        // 20-Question Raw Data
        q1_bp_history: document.getElementById('q1_bp_history').value === 'true',
        q2_diabetes_history: document.getElementById('q2_diabetes_history').value === 'true',
        q3_family_heart: document.getElementById('q3_family_heart').value === 'true',
        q4_dry_eyes: document.getElementById('q4_dry_eyes').value === 'true',
        q5_headaches: document.getElementById('q5_headaches').value === 'true',
        q6_neck_pain: document.getElementById('q6_neck_pain').value === 'true',
        q7_back_pain: document.getElementById('q7_back_pain').value === 'true',
        q8_sedentary: document.getElementById('q8_sedentary').value === 'true',
        // Q9/Q10 are handled above
        q11_insomnia: document.getElementById('q11_insomnia').value === 'true',
        q12_overwhelmed: document.getElementById('q12_overwhelmed').value === 'true',
        q13_drained: document.getElementById('q13_drained').value === 'true',
        q14_anxious: document.getElementById('q14_anxious').value === 'true',
        q15_anhedonia: document.getElementById('q15_anhedonia').value === 'true',
        q16_phone_bedtime: document.getElementById('q16_phone_bedtime').value === 'true',
        q17_internet_anxiety: document.getElementById('q17_internet_anxiety').value === 'true',
        q18_breathlessness: document.getElementById('q18_breathlessness').value === 'true',
        q19_fatigue: document.getElementById('q19_fatigue').value === 'true',
        q20_diet: document.getElementById('q20_diet').value === 'true',

        // Legacy/Computed
        daily_digital_hours: 8.0 // default
    };

    // UI Feedback
    const submitBtn = document.querySelector('.cta-button');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span class="spinner"></span> Analyzing Bio-Data...';
    submitBtn.disabled = true;

    try {
        // --- 2. Call API ---
        const response = await fetch('/api/v1/assess', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const err = await response.json();
            // Handle Pydantic Validation Errors (Array)
            if (Array.isArray(err.detail)) {
                console.error("Validation Errors:", err.detail);
                const msg = err.detail.map(e => `Field '${e.loc[e.loc.length - 1]}': ${e.msg}`).join('\n');
                throw new Error("Missing/Invalid Fields:\n" + msg);
            }
            throw new Error(err.detail || 'Assessment failed');
        }

        const result = await response.json();

        // --- 3. Render Results ---
        renderResults(result);

    } catch (err) {
        alert("Error: " + err.message);
    } finally {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
});

function renderResults(data) {
    // Hide Form, Show Results
    document.getElementById('assessment-form').classList.add('hidden');
    const resultSection = document.getElementById('results-view');
    resultSection.classList.remove('hidden');
    resultSection.classList.add('fade-in');

    // SVG Circle Animation
    const circle = document.querySelector('.progress-value');
    const radius = circle.r.baseVal.value;
    const circumference = radius * 2 * Math.PI;

    circle.style.strokeDasharray = `${circumference} ${circumference}`;
    circle.style.strokeDashoffset = circumference;

    const offset = circumference - (avgProb * circumference); // avgProb is 0.0 to 1.0

    // Add small delay to animate
    setTimeout(() => {
        circle.style.strokeDashoffset = offset;
    }, 100);

    // Cards
    const grid = document.getElementById('risk-cards-container');
    grid.innerHTML = ''; // Clear previous

    data.risks.forEach(risk => {
        const card = document.createElement('div');
        card.className = `risk-item ${risk.risk_level}`;

        card.innerHTML = `
            <div class="risk-header">
                <h3>${risk.disease}</h3>
                <span class="risk-level">${risk.risk_level}</span>
            </div>
            <p class="explanation"><strong>Primary Drivers:</strong> ${risk.contributing_factors.join(', ')}</p>
            <ul class="rec-list">
                ${risk.prevention_steps.map(s => {
            // Make the detailed steps look nice by bolding the Action
            const parts = s.split(':');
            if (parts.length > 1) {
                // Wrap the first part (Action) in strong tag if not already markdown formatted
                // The LLM returns "**Action**: ...", so we just render it.
                // But we should clean potential double asterisks if we want purely custom styling
                return `<li>${s.replace(/\*\*/g, '<strong>').replace(/\*\*/g, '</strong>')}</li>`;
            }
            return `<li>${s}</li>`;
        }).join('')}
            </ul>
        `;
        grid.appendChild(card);
    });
} // End renderResults

document.getElementById('reset-btn').addEventListener('click', () => {
    document.getElementById('results-view').classList.add('hidden');
    document.getElementById('assessment-form').classList.remove('hidden');
    document.getElementById('assessment-form').classList.add('fade-in');
});
