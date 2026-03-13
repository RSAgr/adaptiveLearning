# What is the project about

This project showcases a Minimal Viable Prototype (only the backend) of an AI-based adaptive learning system.

For this MVP, there is a set of 20 questions with varying difficulty levels. From this collection, a question is selected and presented to the student based on their current ability.

The system maintains an ability score for the student. Based on the correctness of the response, the difficulty of the question, and the student's current ability, the ability score is dynamically updated. This allows the system to gradually adjust the difficulty of upcoming questions to better match the student's knowledge level.

The adaptive mechanism follows a simplified **Item Response Theory (IRT)-inspired approach**, where the probability of answering a question correctly depends on the difference between the student’s ability and the question’s difficulty.

This process is repeated until either a predefined number of iterations is reached or the entire question set is exhausted.

For each questionnaire session, a performance summary is generated and passed to a GenAI model. Based on this summary, the model generates personalized suggestions for improvement and study strategy.

# How to start

- Install the required packages using  
  `pip install -r requirements.txt`

- Environment Variables
  * Create a `.env` file in the root directory and add your API key.
  * You can use either **Gemini** (used during development) or **OpenAI**.

### Note for Evaluators

Since the OpenAI API requires paid usage, Gemini was used during development and testing. However, the equivalent OpenAI implementation has also been included in the codebase as commented code in [evaluation.py](app/services/evaluation.py).

The current prototype uses a single implementation path for simplicity. Alternative designs—such as exposing separate endpoints for different LLM providers or allowing the user to select the model at runtime—were considered. However, these approaches were deemed unnecessary for the scope of this prototype and would introduce additional complexity without providing significant benefit for the assignment.

- Run the backend using  
  `uvicorn app.main:app --reload`

- Open a web browser and navigate to  
  `http://127.0.0.1:8000/docs`

- Test the backend using the following flow:

  **Start Session → Get Question → Submit Answer → Repeat Get Question → Generate AI Plan**

# AI Usage Log

This project was developed with assistance from AI tools for ideation, debugging, and documentation.

A detailed log of AI interactions, prompts, and how the outputs were used or modified can be found here:

[AI Usage Log](ai_log.md)

# Future Scope and Improvements

There are several opportunities to further enhance the adaptive diagnostic engine:

## 1. Conversational Adaptive Agent

The current system generates a study plan based solely on the performance summary derived from the test session. In future iterations, this can be extended using an agent-based framework such as **LangGraph** to create an interactive diagnostic agent.

Instead of relying only on test summaries, the agent could dynamically request additional information from the student (e.g., study habits, preparation timeline, prior knowledge, or target exam score). This additional context would allow the system to generate more personalized and actionable learning plans.

## 2. Topic-Aware Adaptive Difficulty

The current adaptive algorithm adjusts difficulty based on a **single global ability score**, without distinguishing between subject areas.

As a result, if a student performs well in one topic (e.g., Mathematics) but poorly in another (e.g., Vocabulary), the overall ability score may increase and cause the system to serve harder questions even in the weaker topic.

A more robust approach would involve maintaining **separate ability estimates per topic** (e.g., Algebra ability, Arithmetic ability, Vocabulary ability). The adaptive question selection algorithm could then choose questions based on the student's **topic-specific proficiency**, resulting in a more accurate assessment of strengths and weaknesses.

In a nutshell, moving from 1D IRT to multi-dimensional IRT

## 3. Scalable Question Retrieval

Currently, the system loads all questions from the database and selects the closest difficulty level in memory. While this works for a small dataset, it may not scale well for larger question banks.

A more scalable approach would involve querying the database for questions within a difficulty range (e.g., `ability ± ε`) and performing adaptive selection within that subset. This would significantly reduce memory usage and improve performance in production environments.
