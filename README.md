# VITALSCAN - Elite AI Health Risk Intelligence

![VITALSCAN](frontend/vitalscan_hero_banner.png)

**VITALSCAN** is a privacy-first, AI-powered health risk assessment platform that provides personalized preventive health insights using machine learning and large language models.

## 🌟 Features

- **20-Question Comprehensive Screening** - Covers 8 health domains including cardiovascular, metabolic, mental health, and lifestyle factors
- **AI-Powered Risk Assessment** - XGBoost models trained on NHANES data for accurate risk prediction
- **Personalized Recommendations** - LLM-generated, context-aware prevention strategies tailored to your profile
- **Beautiful Interactive UI** - Modern wizard-style interface with 3D effects and smooth animations
- **Privacy-First** - All data processed locally, no personal information stored

## 🎯 Health Domains Assessed

1. **Cardiometabolic** - Type 2 Diabetes, Hypertension
2. **Digital Health** - Eye Strain, Screen Time Impact
3. **Musculoskeletal** - Posture, Pain Management
4. **Sleep & Lifestyle** - Sleep Quality, Activity Levels
5. **Mental Wellbeing** - Stress, Anxiety, Burnout
6. **Habits & Symptoms** - Diet, Fatigue, Respiratory Health

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js (optional, for development)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/vitalscan.git
cd vitalscan
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Create .env file
cp .env.example .env

# Add your Hugging Face API token
# HF_TOKEN=your_token_here
```

4. **Run the application**
```bash
python -m uvicorn app.main:app --reload
```

5. **Open in browser**
```
http://localhost:8000
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **XGBoost** - Gradient boosting for risk prediction
- **Scikit-learn** - ML pipeline and preprocessing
- **Pydantic** - Data validation

### Frontend
- **Vanilla JavaScript** - Interactive wizard interface
- **CSS3** - Modern animations and 3D effects
- **HTML5** - Semantic markup

### AI/ML
- **Hugging Face Inference API** - LLM-powered explanations
- **NHANES Dataset** - Training data for risk models

## 📊 Model Performance

- **Type 2 Diabetes**: AUC > 0.80
- **Hypertension**: AUC > 0.78
- **Metabolic Syndrome**: AUC > 0.75

## 🔒 Privacy & Safety

- ✅ No personal identifiable information (PII) collected
- ✅ Anonymous session IDs only
- ✅ All processing done locally
- ✅ No diagnosis provided - risk estimates only
- ✅ Medical disclaimers included

## 📁 Project Structure

```
vitalscan/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   └── core/
│       ├── ml_service.py    # Risk assessment logic
│       └── llm_service.py   # LLM integration
├── frontend/
│   ├── index.html           # Main UI
│   ├── style.css            # Core styles
│   ├── wizard.css           # Interactive wizard styles
│   ├── effects-3d.css       # 3D animations
│   ├── script.js            # Main logic
│   └── wizard.js            # Wizard navigation
├── ml/
│   ├── nhanes_loader.py     # Data pipeline
│   └── models/              # Trained models
├── docs/                    # Documentation
└── requirements.txt         # Python dependencies
```

## 🎨 UI Features

- **Multi-step Wizard** - 6-step progress indicator
- **Interactive Question Cards** - Hover effects and animations
- **Custom Option Buttons** - Beautiful Yes/No selections
- **3D Visual Effects** - Medical scanner, floating elements
- **Responsive Design** - Mobile-friendly layout
- **Keyboard Navigation** - Arrow keys to navigate steps

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

**VITALSCAN is for educational and informational purposes only. It is NOT a medical device and does NOT provide medical diagnosis or treatment. Always consult with qualified healthcare professionals for medical advice.**

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- NHANES (National Health and Nutrition Examination Survey) for training data
- Hugging Face for LLM infrastructure
- Open-source ML community

---

**Built with ❤️ for preventive health awareness**
