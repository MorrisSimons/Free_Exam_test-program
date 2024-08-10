import json
import streamlit as st
import random

def load_data():
    with open("data.json", "r") as f:
        return json.load(f)

def reset_quiz():
    st.session_state.seen_questions = []
    st.session_state.remaining_questions = list(st.session_state.data.items())
    random.shuffle(st.session_state.remaining_questions)  # Randomize the order of questions
    st.session_state.current_question, st.session_state.current_answer = st.session_state.remaining_questions.pop()
    st.session_state.show_answer = False
    st.session_state.correct = False
    st.session_state.alternatives = get_question_with_alternatives(st.session_state.data, st.session_state.current_answer)

def get_question_with_alternatives(data, correct_answer):
    all_answers = list(data.values())
    alternatives = random.sample(all_answers, 3)  # Pick 3 random alternatives
    if correct_answer not in alternatives:
        alternatives[random.randint(0, 2)] = correct_answer  # Replace one alternative with the correct answer
    random.shuffle(alternatives)  # Shuffle the alternatives
    return alternatives

def main():
    st.title("Flashcard Question and Answer App")
    
    # Load data once into session state
    if 'data' not in st.session_state:
        st.session_state.data = load_data()
    
    total_questions = len(st.session_state.data)
    
    # Initialize session state
    if 'remaining_questions' not in st.session_state or len(st.session_state.remaining_questions) == 0:
        reset_quiz()
    
    # Display the counter
    solved_questions = total_questions - len(st.session_state.remaining_questions) - 1
    st.write(f"Questions solved: {solved_questions}/{total_questions}")
    
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
    
    # Handle the "Next Question" button
    if st.button("Next Question"):
        if st.session_state.remaining_questions:
            st.session_state.seen_questions.append((st.session_state.current_question, st.session_state.current_answer))
            st.session_state.current_question, st.session_state.current_answer = st.session_state.remaining_questions.pop()
            st.session_state.show_answer = False  # Reset answer visibility
            st.session_state.correct = False  # Reset correctness
            st.session_state.alternatives = get_question_with_alternatives(st.session_state.data, st.session_state.current_answer)  # Get new alternatives
        else:
            st.write("You have answered all the questions!")
    
    # Add the "Restart" button at the end
    if st.button("Restart"):
        reset_quiz()
    
    st.write("---")

if __name__ == "__main__":
    main()
