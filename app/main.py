from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from app.evaluation import generate_study_plan
from app.services.adaptiveTesting import (
    select_next_question,
    update_ability
)
from bson.errors import InvalidId

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["adaptive_test"]

questions_collection = db["questions"] # this contains the questions
sessions_collection = db["sessions"] # this contains data for each new test session
students_collection = db["students"] # this can be used to store student performances in each of his/her test sessions, and can be used to track progress over time

# Will replace topics_wrong with counter

@app.post("/students")
def create_student(name: str):

    student = {
        "name": name
    }

    result = students_collection.insert_one(student)

    return {"student_id": str(result.inserted_id)}

@app.post("/start-session")
def start_session(student_id: str):

    session = {
        "student_id": ObjectId(student_id),
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

    return {
            "session_id": str(result.inserted_id),
            "message": "Session started. Use this session_id for subsequent requests."
        }

@app.get("/next-question/{session_id}")
def next_question(session_id: str):
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
        "difficulty": question["difficulty"],
        "message": "Use this question_id to submit your answer for this question."
    }
    
    
# the way we are increasing the difficulty that is respective for each topic, is it?    
# Also, let us have a conncept of strong topics which would be for topic for which correct answers were given more than a threshold 
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
 
# Though not used in the current flow, this endpoint can be useful for users to check their performance summary after completing the test or at any point during the test. It provides insights into their strengths and weaknesses, which can help them manually divert focus on specific areas for improvement.   
@app.get("/summary/{session_id}")                      
def summary(session_id: str):

    try:
        session = sessions_collection.find_one({"_id": ObjectId(session_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid session_id")

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return session["performance"]

# Give examples of difficulty
# Use of langgraph for getting student's POV as well

from bson.errors import InvalidId

# I am manually passing the params, without frontend, to test the endpoint. In real implementation, these params will be passed from frontend. 

@app.get("/study-plan/{session_id}")
def study_plan(session_id: str):

    try:
        session = sessions_collection.find_one({"_id": ObjectId(session_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid session_id")

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    student_id = session["student_id"]

    # Fetch previous sessions of this student (excluding current session)
    previous_sessions = list(
        sessions_collection.find(
            {
                "student_id": student_id,
                "_id": {"$ne": session["_id"]}
            }
        ).sort("_id", -1).limit(1) # since this is prototype, limiting to last session for context, can be increased later (with different prompt engineering to ensure we don't exceed token limits and more weightage is given to recent sessions)
    )

    previous_context = ""

    for s in previous_sessions: # In case somebody decides to increase the number of prev sessions to be considered
        perf = s["performance"]
        rec = s.get("ai_recommendation", "No recommendation recorded")

        previous_context += f"""
            Previous Session:
            Correct: {perf['correct']}
            Incorrect: {perf['incorrect']}
            Weak Topics: {perf['topics_wrong']}
            Hardest Difficulty Solved: {perf['max_difficulty_correct']}

            Previous Recommendation:
            {rec}
        """

    # Current session summary
    perf = session["performance"]

    current_summary = f"""
        Current Session Performance:
        Correct: {perf['correct']}
        Incorrect: {perf['incorrect']}
        Weak Topics: {perf['topics_wrong']}
        Hardest Difficulty Solved: {perf['max_difficulty_correct']}
        """

    prompt = f"""
        You are an AI learning assistant.

        Below is the student's learning history.

        {previous_context}

        {current_summary}

        Based on the previous recommendations and current performance,
        generate a personalized study plan to improve the student's weak areas.
        
        Also, if the performance has improved compared to the last session, acknowledge the improvement and suggest how to further build on that progress. If there are areas of decline, provide encouragement and specific strategies to address those.
        """

    plan = generate_study_plan(prompt)

    # Save recommendation in session
    sessions_collection.update_one(
        {"_id": session["_id"]},
        {"$set": {"ai_recommendation": plan}}
    )

    return {"study_plan": plan}