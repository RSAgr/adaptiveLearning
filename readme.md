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
