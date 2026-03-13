import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_study_plan(summary):

    prompt = f"""
    A student completed an adaptive GRE test.

    Performance summary:
    {summary}

    Generate a concise 3-step study plan to improve the student's weak areas.
    """

    response = model.generate_content(prompt)

    return response.text

# print(generate_study_plan("The student performed well in quantitative reasoning but struggled with verbal reasoning."))