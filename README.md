# HEALTHCARE.AI
HealthMonAI is a full-stack AI-powered healthcare monitoring application that helps users manage fitness, medications, and general health guidance through an interactive interface.  The system provides an end-to-end healthcare workflow including chatbot assistance, health tracking, reporting, and Indian healthcare features.
__________________________________________________________________________________
Live Application
🔗 Deployed App: https://healthmonai-3qnhcdqnm4g3eux2r4f96h.streamlit.app
🔗 GitHub Repository: https://github.com/SIDDI-374/HEALTHCARE.AI
__________________________________________________________________________________
Features

AI Health Chatbot
Provides general health advice using AI
Handles errors safely
Uses Groq API for fast responses
__________________________________________________________________________________
Health Dashboard
Displays BMI and goal tracking
Gives quick health summary
__________________________________________________________________________________
BMI Calculator
Calculates BMI based on weight & height
Displays graphical visualization
Includes input validation
__________________________________________________________________________________
Medication Tracker
Add and store medications
View medication list
Check drug interactions
Get medicine information
_________________________________________________________________________________
📄 Health Report
Shows medication data
Provides health tips
Export report as CSV
_________________________________________________________________________________
Data Handling
Upload and view JSON health data
_________________________________________________________________________________
Health Goal Tracking
Set and monitor personal health goals
_________________________________________________________________________________
🇮🇳 Indian Healthcare Features

Diet recommendations (weight loss/gain/maintain)
Ayurvedic suggestions
Doctor finder (city-based local database)
Medical history input
Insurance awareness
Regional health preferences
_________________________________________________________________________________
Technologies Used
Python
Streamlit
LangChain
Groq API
SQLite
Matplotlib
Pandas
_________________________________________________________________________________
Project structure

HealthMonAI/
│
├── app.py
├── chatbot.py
├── health_metrics.py
├── medication.py
├── database.py
├── requirements.txt
└── README.md
_________________________________________________________________________________
How to Run Locally
1.Clone the repository
{git clone https://github.com/SIDDI-374/HEALTHCAREAI.git}

2.Navigate to folder
{cd HealthMonAI}

3.Install dependencies
{pip install -r requirements.txt}

4.Add API key (Groq)
{set GROQ_API_KEY=your_api_key (Windows)}

5.Run app
{streamlit run app.py}
_______________________________________________________________________________
Deployment
The application is deployed using Streamlit Community Cloud.

Steps:
Code hosted on GitHub
requirements.txt added
API key stored securely using Streamlit Secrets
App deployed via Streamlit Cloud dashboard
______________________________________________________________________________
Development Timeline
Week 1–2
Project setup
Chatbot
BMI calculator
Medication tracker

Week 3–4
Health data visualization
Report generation
JSON handling
Goal tracking

Week 5–6
Indian healthcare features
Diet system
Ayurvedic suggestions
Doctor system
Medical history

Week 7–8
Dashboard UI
Input validation
Error handling
Export feature
Deployment
_____________________________________________________________________________
Demo Video
The demo video demonstrates:
_____________________________________________________________________________
Dashboard overview
Chatbot interaction
BMI calculation
Medication tracking
Report export
Indian healthcare features
_____________________________________________________________________________
Disclaimer
This project is for educational purposes only. It does not provide medical diagnosis. Always consult a qualified doctor for serious conditions.
_____________________________________________________________________________
Author
Satya Venkata B.tech Student
