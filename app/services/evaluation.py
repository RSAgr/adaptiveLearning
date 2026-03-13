import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_study_plan(summary):

    prompt = f"""
    {summary}
    Generate a concise 3-step study plan to improve the student's weak areas.
    """

    response = model.generate_content(prompt)

    return response.text

# ---------------- OPENAI IMPLEMENTATION (COMMENTED FOR NOW) ----------------

# Uncomment this block when switching to OpenAI and instead comment the above lines

# from openai import OpenAI
# import os
#
# from dotenv import load_dotenv

# load_dotenv()
#
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#
# def generate_study_plan(summary):
#
#     prompt = f"""
#     A student completed an adaptive GRE test.
#
#     Performance summary:
#     {summary}
#
#     Generate a concise 3-step study plan to improve the student's weak areas.
#     """
#
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are an expert GRE tutor."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#
#     return response.choices[0].message.content