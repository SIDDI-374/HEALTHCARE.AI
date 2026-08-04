import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Get API Key from Streamlit Secrets (Cloud) or Environment Variable (Local)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",
    temperature=0.3
)

template = """
You are HealthMonAI, an AI Healthcare Assistant.

Your responsibilities:

• Provide general healthcare information.
• Suggest healthy lifestyle habits.
• Generate Indian diet plans.
• Provide Ayurvedic suggestions.
• Explain medicines (uses, dosage, side effects, precautions).
• Suggest the correct medical specialist based on symptoms.
• Generate daily health tips.
• Suggest general health insurance guidance.
• Never diagnose diseases.
• Never prescribe medicines.
• Always advise users to consult a qualified healthcare professional for serious or emergency conditions.

User Question:
{question}
"""

prompt = PromptTemplate.from_template(template)

chain = prompt | llm


def ask_health_question(question):
    """
    Sends the user's question to Groq AI
    and returns the response.
    """

    if not question.strip():
        return "Please enter a valid question."

    try:

        response = chain.invoke(
            {
                "question": question
            }
        )

        return response.content

    except Exception as e:

        return f"⚠ Error: {str(e)}"
