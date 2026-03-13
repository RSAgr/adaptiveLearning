from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from app.evaluation import generate_study_plan
from app.services.adaptiveTesting import (
    select_next_question,
    update_ability
)

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["adaptive_test"]

questions_collection = db["questions"]
sessions_collection = db["sessions"]

# Will replace topics_wrong with counter

@app.post("/start-session")
def start_session():

    session = {
        "ability": 0.5,
        "asked_questions": [],
        "performance": {
            "correct": 0,
            "incorrect": 0,
            "topics_wrong": {},
            "max_difficulty_correct": 0
        },
        "questions_answered": 0
    }

    result = sessions_collection.insert_one(session)

    return {"session_id": str(result.inserted_id)}

@app.get("/next-question/{session_id}")
def next_question(session_id: str):

    # session = sessions_collection.find_one({"_id": ObjectId(session_id)})
    from bson.errors import InvalidId

    try:
        session = sessions_collection.find_one({"_id": ObjectId(session_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid session_id")

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    questions = list(questions_collection.find())

    question = select_next_question(
        questions,
        session["ability"],
        session["asked_questions"]
    )

    if not question:
        return {"message": "Test complete"}

    return {
        # "question_id": str(question["_id"]),
        "question_id": str(question["_id"]),
        "question": question["question"],
        "options": question["options"],
        "difficulty": question["difficulty"]
    }
    
# @app.post("/submit-answer")
# def submit_answer(session_id: str, question_id: str, answer: str):

#     session = sessions_collection.find_one({"_id": ObjectId(session_id)})

#     question = questions_collection.find_one({"_id": ObjectId(question_id)})

#     correct = answer.strip().lower() == question["correct_answer"].strip().lower() # ignore Case and whitespace

#     ability = update_ability(
#         session["ability"],
#         question["difficulty"],
#         correct
#     )

#     asked = session["asked_questions"]
#     asked.append(question["_id"])

#     sessions_collection.update_one(
#         {"_id": ObjectId(session_id)},
#         {
#             "$set": {"ability": ability},
#             "$push": {"asked_questions": question["_id"]},
#             "$inc": {"questions_answered": 1}
#         }
#     )

#     return {
#         "correct": correct,
#         "updated_ability": ability
#     }
    
@app.post("/submit-answer")
def submit_answer(session_id: str, question_id: str, answer: str):

    session = sessions_collection.find_one({"_id": ObjectId(session_id)})
    question = questions_collection.find_one({"_id": ObjectId(question_id)})

    correct = answer.strip().lower() == question["correct_answer"].strip().lower()

    ability = update_ability(
        session["ability"],
        question["difficulty"],
        correct
    )

    update_query = {
        "$set": {"ability": ability},
        "$push": {"asked_questions": question["_id"]},
        "$inc": {"questions_answered": 1}
    }

    if correct:
        update_query["$inc"]["performance.correct"] = 1
        update_query["$max"] = {
            "performance.max_difficulty_correct": question["difficulty"]
        }
    else:
        update_query["$inc"]["performance.incorrect"] = 1
        update_query["$inc"][f"performance.topics_wrong.{question['topic']}"] = 1

    sessions_collection.update_one(
        {"_id": ObjectId(session_id)},
        update_query
    )

    return {
        "correct": correct,
        "updated_ability": ability
    }
    
@app.get("/summary/{session_id}")
def summary(session_id: str):

    session = sessions_collection.find_one({"_id": ObjectId(session_id)})

    return session["performance"]

# Give examples of difficulty
# Use of langgraph for input

@app.get("/study-plan/{session_id}")
def study_plan(session_id: str):

    session = sessions_collection.find_one({"_id": ObjectId(session_id)})

    summary = str(session["performance"])

    plan = generate_study_plan(summary)

    return {"study_plan": plan}