🧬 LifeMode AI – Occupational Lifestyle Intelligence System

LifeMode AI is an AI-powered health and lifestyle analysis platform designed to help
students, professionals, gamers, and workers understand how their daily habits,
work stress, and occupational strain affect their overall health.

This project was built for hackathons, learning, and startup MVP experimentation.

--------------------------------------------------------------------

FEATURES

    - AI-based health risk prediction
    - Biological health scoring (sleep, hydration, nutrition, BMI)
    - Burnout & nervous system analysis
    - Occupational strain & posture risk detection
    - LifeMode Master Index (combined health score)
    - Weekly health tracking with charts
    - Personalized health improvement plans
    - Daily health log saving

--------------------------------------------------------------------

TECH STACK

    - Python
    - Streamlit        : UI & dashboard
    - Scikit-learn    : AI model
    - Pandas & NumPy  : Data processing
    - Joblib          : Model loading

--------------------------------------------------------------------

PROJECT STRUCTURE

    smart-health-helper/
    |
    ├── WorkWellAI.py
    |       Main Streamlit application
    |
    ├── health_risk_model.pkl
    |       Trained AI prediction model
    |
    ├── train_ai_model.py
    |       AI training script
    |
    ├── train_health_model.py
    |       Health scoring model training
    |
    ├── weekly_log.csv
    |       Weekly health logs (auto-created)
    |
    ├── requirements.txt
    |       Python dependencies
    |
    └── README.md / README.txt
            Project documentation

--------------------------------------------------------------------

INSTALLATION & SETUP

    Step 1: Clone the repository

        git clone https://github.com/cap-mehboob/smart-health-helper.git
        cd smart-health-helper

    Step 2: Install dependencies

        pip install -r requirements.txt

    Step 3: Run the application

        python -m streamlit run WorkWellAI.py

    Step 4: Open in browser

        http://localhost:8501

--------------------------------------------------------------------

LIFEMODE MASTER INDEX FORMULA

    LifeMode Index =

        (45%  × Biological Health)
      + (30%  × Nervous System Health)
      + (25%  × Occupational Health)

--------------------------------------------------------------------

USE CASES

    - Hackathons & college projects
    - Health-tech MVP demos
    - Lifestyle analytics experiments
    - AI + wellness startup prototypes

--------------------------------------------------------------------

DISCLAIMER

    This tool is NOT a medical diagnosis system.

    It is intended only for:
        - Educational purposes
        - Experimental learning
        - Wellness awareness

    Always consult a medical professional for health decisions.

--------------------------------------------------------------------

AUTHOR

    Built with ❤️ by Mehboob
