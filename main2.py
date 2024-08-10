import json
import streamlit as st

def main():
    st.title("Question and Answer App")
    
    # Load data
    with open("data.json", "r") as f:
        data = json.load(f)
    
    # Loop through all questions and answers
    for question, answer in data.items():
        # Display question and add an show/hide answer button
        if st.button(question):
            st.
            st.session_state[question] = False
        if st.button("next question"):
            st.session_state[question] = True
				if st.session_state[question] == True:
					st.
				
if __name__ == "__main__":
    main()
