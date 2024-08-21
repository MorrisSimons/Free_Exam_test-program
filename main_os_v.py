import json
import streamlit as st
import random
import argparse, sys

def load_data(data):
    with open(f"{data}.json", "r") as f:
        return json.load(f)

def reset_quiz():
    st.session_state.seen_questions = []
    st.session_state.remaining_questions = st.session_state.data.copy()
    random.shuffle(st.session_state.remaining_questions)  # Randomize the order of questions
    current_q = st.session_state.remaining_questions.pop()
    st.session_state.current_question = current_q["question"]
    st.session_state.current_answer = current_q["answer"]
    st.session_state.incorrect_answers = 0  # Reset incorrect answers counter
    st.session_state.show_answer = False
    st.session_state.correct = False
    st.session_state.alternatives = get_question_with_alternatives(current_q["options"], st.session_state.current_answer)
    st.session_state.explanation = current_q["explanation"]  # Store the explanation

def get_question_with_alternatives(options, correct_answer):
    alternatives = random.sample(options, len(options))  # Shuffle the alternatives
    if correct_answer not in alternatives:
        alternatives[random.randint(0, len(alternatives) - 1)] = correct_answer  # Ensure correct answer is in alternatives
    random.shuffle(alternatives)  # Shuffle again to randomize the placement
    return alternatives

def load_next_question():
    if st.session_state.remaining_questions:
        st.session_state.seen_questions.append({
            "question": st.session_state.current_question,
            "answer": st.session_state.current_answer
        })
        current_q = st.session_state.remaining_questions.pop()
        st.session_state.current_question = current_q["question"]
        st.session_state.current_answer = current_q["answer"]
        st.session_state.show_answer = False  # Reset answer visibility
        st.session_state.correct = False  # Reset correctness
        st.session_state.alternatives = get_question_with_alternatives(current_q["options"], st.session_state.current_answer)  # Get new alternatives
        st.session_state.explanation = current_q["explanation"]  # Update explanation for new question
        

def main(data):
    st.title("Flashcard Question and Answer App")
    
    # Load data once into session state
    if 'data' not in st.session_state:
        st.session_state.data = load_data(data)
    
    total_questions = len(st.session_state.data)
    
    # Initialize session state
    if 'remaining_questions' not in st.session_state or len(st.session_state.remaining_questions) == 0:
        reset_quiz()
    
    # Handle the "Next Question" button
    next_question_clicked = st.button("Next Question")
    if next_question_clicked:
        load_next_question()

    # Display the counters
    solved_questions = total_questions - len(st.session_state.remaining_questions) - 1
    incorrect_answers = st.session_state.incorrect_answers
    st.write(f"Questions solved: {solved_questions}/{total_questions}")
    st.write(f"Incorrect answers: {incorrect_answers}")

    # Display the current question
    st.write(f"**Question:** {st.session_state.current_question}")
    
    # Show the multiple-choice options
    selected_option = st.radio("Choose the correct answer:", st.session_state.alternatives, index=0)
    
    # Show the correct answer when the user selects an option
    if st.button("Submit Answer"):
        if selected_option == st.session_state.current_answer:
            st.write("Correct!")
            st.session_state.correct = True
        else:
            st.write(f"Incorrect! The correct answer is: {st.session_state.current_answer}")
            st.session_state.correct = False
            st.session_state.incorrect_answers += 1

        # Show explanation after the answer is revealed
        st.write(f"**Explanation:** {st.session_state.explanation}")

    # Add the "Restart" button at the end
    if st.button("Restart"):
        reset_quiz()
    
    st.write("---")

if __name__ == "__main__":
    data = "os/all"
    main(data)
