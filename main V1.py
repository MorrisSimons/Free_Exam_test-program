import json
import streamlit as st
import random

def load_data():
    with open("data.json", "r") as f:
        return json.load(f)

def get_random_question(data, seen_questions):
    remaining_questions = [q for q in data.items() if q[0] not in seen_questions]
    if remaining_questions:
        question, answer = random.choice(remaining_questions)
        return question, answer
    else:
        return None, None

def reset_quiz():
    st.session_state.seen_questions = set()
    st.session_state.current_question, st.session_state.current_answer = get_random_question(st.session_state.data, st.session_state.seen_questions)
    st.session_state.show_answer = False

def main():
    st.title("Flashcard Question and Answer App")
    
    # Load data once into session state
    if 'data' not in st.session_state:
        st.session_state.data = load_data()
    
    total_questions = len(st.session_state.data)
    
    # Initialize session state
    if 'seen_questions' not in st.session_state:
        reset_quiz()
    
    # Display the counter
    solved_questions = len(st.session_state.seen_questions)
    st.write(f"Questions solved: {solved_questions}/{total_questions}")
    
    # Handle the "Next Question" button first
    if st.button("Next Question"):
        if st.session_state.current_question:
            st.session_state.seen_questions.add(st.session_state.current_question)
        st.session_state.current_question, st.session_state.current_answer = get_random_question(st.session_state.data, st.session_state.seen_questions)
        st.session_state.show_answer = False  # Reset answer visibility
    
    # Display the current question
    if st.session_state.current_question:
        st.write(f"**Question:** {st.session_state.current_question}")
    
        # Show the answer when the button is pressed
        if st.button("Show Answer"):
            st.session_state.show_answer = True
    
        if st.session_state.show_answer:
            st.write(f"**Answer:** {st.session_state.current_answer}")
    else:
        st.write("You have answered all the questions!")
    
    # Add the "Restart" button at the end
    if st.button("Restart"):
        reset_quiz()
    
    st.write("---")

if __name__ == "__main__":
    main()
