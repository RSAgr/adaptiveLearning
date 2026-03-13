import math
from typing import Counter
from pymongo import MongoClient

# from app.evaluation import generate_study_plan

# IRT probability
def probability_correct(ability, difficulty):
    return 1 / (1 + math.exp(-(ability - difficulty)))

# ability update
def update_ability(ability, difficulty, correct):
    prob = probability_correct(ability, difficulty)
    result = 1 if correct else 0
    learning_rate = 0.1
    return ability + learning_rate * (result - prob)

# choose next question
def select_next_question(questions, ability, asked_ids):
    remaining = [q for q in questions if q["_id"] not in asked_ids]

    if not remaining:
        return None

    remaining.sort(key=lambda q: abs(q["difficulty"] - ability))
    return remaining[0]


# client = MongoClient("mongodb://localhost:27017/")

# db = client["questions"]
# questions_collection = db["questions"]

# questions = list(questions_collection.find())

# ability = 0.5
# asked_questions = set()

# NUM_QUESTIONS = 20

# performance = {
#     "correct": 0,
#     "incorrect": 0,
#     "topics_wrong": Counter(),
#     "max_difficulty_correct": 0
# }

# for _ in range(NUM_QUESTIONS):

#     question = select_next_question(questions, ability, asked_questions)

#     if not question:
#         print("No more questions available")
#         break

#     print(f"\nQuestion: {question['question']}")
#     print("Options:", ", ".join(question["options"]))

#     user_answer = input("Your answer: ")

#     correct = user_answer.strip() == question["correct_answer"]
    
#     # update stats
#     if correct:
#         performance["correct"] += 1
#         performance["max_difficulty_correct"] = max(
#             performance["max_difficulty_correct"],
#             question["difficulty"]
#         )
#     else:
#         performance["incorrect"] += 1
#         performance["topics_wrong"][question["topic"]] += 1

#     ability = update_ability(ability, question["difficulty"], correct)

#     asked_questions.add(question["_id"])

#     print(f"Correct: {correct}")
#     print(f"Updated ability: {ability:.2f}")
    
    
# summary = f"""
# Student Ability Score: {ability:.2f}

# Total Questions: {NUM_QUESTIONS}
# Correct Answers: {performance['correct']}
# Incorrect Answers: {performance['incorrect']}

# Weak Topics:
# {set(performance['topics_wrong'].keys())}

# Number of Incorrect Answers per Topic:
# {dict(performance['topics_wrong'])}

# Highest Difficulty Solved:
# {performance['max_difficulty_correct']}
# """

# print("\nPerformance Summary:")
# print(summary)

# study_plan = generate_study_plan(summary)

# print("\nPersonalized Study Plan:")
# print(study_plan)

# # develop the backend points
# # save last summary and pass it to the model, now the summary is a summary using the last summary as well
# # Why does it show : Highest Difficulty Solved: 0.5
# # Add more questions with higher difficulty to the database and test again.
# # Give more context to AI
# # Also, can't we use cloud to compare with others
# # Maybe we can use summary using the difficulty of questions and the correctness to generate a summary of the student's performance, which can then be fed into a language model to generate a study plan.