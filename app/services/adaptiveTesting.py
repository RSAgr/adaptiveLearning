import math

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
