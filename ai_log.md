# AI Usage Log

This document records how AI tools were used during the development of this project.

## Tools Used
- ChatGPT
- GitHub Copilot (used minimally, as its suggestions often did not align with the development flow I wanted to maintain)

## Purpose of AI Usage
AI tools were used for:
- debugging backend issues
- refining documentation
- validating and improving system design ideas
- improving readability and clarity of explanations

## Example Interactions  
(Outcomes mention both the usefulness and the limitations encountered.)

### 1. Backend Debugging
Prompt:  
"Why are my FastAPI endpoints not returning questions?"

Outcome:  
ChatGPT helped identify an issue related to database naming.  
GitHub Copilot generated multiple iterative suggestions, but most of them were trivial or not aligned with the intended design, so those changes were eventually reverted.

### 2. Help with the Syntax of Code Snippets
ChatGPT was used for assistance with the syntax of certain backend code snippets. Most of the generated code was correct and usable. However, the MongoDB schema initially contained a few unnecessary attributes. Additionally, the AI occasionally produced inconsistent naming conventions, which caused issues when retrieving questions from the database (related to the issue described in the previous point).

Though the gpt seemed to forget the context after a while. Suggesting unnecessary improvements in the code.

### 3. README Refinement
ChatGPT was used to refine the structure and readability of the README file. The initial content and explanation were written manually, after which the model was asked only to improve formatting and clarity without altering the intended meaning.

### 4. General Clarifications
ChatGPT was used for conceptual clarifications related to the assignment, such as understanding the role of Item Response Theory (IRT) in adaptive learning systems. It was also used to explore options for using generative AI in the feedback stage. Since some AI APIs incur costs, alternative solutions were explored for testing, and the Gemini API free tier was used for local experimentation. Finally, GPT suggested giving a commented code snippet, this ways the evaluator can easily switch to OpenAI if he/she wants to use it instead of Gemini API

### 5. Refining the AI Log
This AI usage log itself was refined with the assistance of an AI tool to improve grammar, clarity, and structure while preserving the original content and intent.

### 6. Generating the Question Set
AI assistance was used to generate the initial set of 20 GRE-style questions.  
The generated questions included additional attributes such as `explanation` and `question_id`. While the system currently relies on MongoDB’s automatically generated `_id` field instead of `question_id`, these attributes were retained as they may be useful for future extensions (e.g., providing explanations after answering a question or supporting external question identifiers).
