import streamlit as st
import random

# Set page configuration
st.set_page_config(
    page_title="Secret Word Quest",
    page_icon="🔍",
    layout="centered"
)

# Initialize session state variables if they don't exist
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'hints' not in st.session_state:
    st.session_state.hints = []
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'game_completed' not in st.session_state:
    st.session_state.game_completed = False
if 'final_attempt' not in st.session_state:
    st.session_state.final_attempt = False
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'skipped_questions' not in st.session_state:
    st.session_state.skipped_questions = 0
if 'show_empty_input_error' not in st.session_state:
    st.session_state.show_empty_input_error = False

# Game content
levels = {
    1: {
        "title": "Level 1: The Riddle",
        "description": "Answer the riddle correctly to earn your first hint. You can skip if needed, but you'll miss the hint.",
        "questions": [
            {
                "text": "I am the silent workhorse of the digital age, built of metal and code, devoid of life yet capable of mimicry. What am I in essence?",
                "answer": "machine",
                "difficulty": "Hard"
            },
            {
                "text": "I operate without a soul, a crafted construct that powers modern innovation. What am I?",
                "answer": "machine",
                "difficulty": "Medium"
            },
            {
                "text": "What do we commonly call a device that performs tasks mechanically or electronically?",
                "answer": "machine",
                "difficulty": "Easy"
            }
        ],
        "hint": "Machine: The non-living engine that drives digital processes."
    },
    2: {
        "title": "Level 2: The Puzzle",
        "description": "Solve the puzzle to earn your second hint. You can skip if needed, but you'll miss the hint.",
        "questions": [
            {
                "text": "I represent the journey from data to insight, an evolving process where experience refines performance. What abstract process am I hinting at?",
                "answer": "learning",
                "difficulty": "Hard"
            },
            {
                "text": "I am the gradual accumulation of knowledge that transforms raw input into expertise. What process do I describe?",
                "answer": "learning",
                "difficulty": "Medium"
            },
            {
                "text": "What is the act of acquiring knowledge or skills through experience?",
                "answer": "learning",
                "difficulty": "Easy"
            }
        ],
        "hint": "Learning: The transformative process of gaining knowledge from experience."
    },
    3: {
        "title": "Level 3: The Cryptic Clue",
        "description": "Decode the cryptic clue to earn your final hint. You can skip if needed, but you'll miss the hint.",
        "questions": [
            {
                "text": "I am the invisible blueprint, a coded pathway that underlies every digital decision, operating silently behind the scenes. What construct am I hinting at?",
                "answer": "algorithm",
                "difficulty": "Hard"
            },
            {
                "text": "I am the series of rules that guide actions within a digital mind, determining outcomes step by step. What am I?",
                "answer": "algorithm",
                "difficulty": "Medium"
            },
            {
                "text": "What term describes a set of instructions or rules used to solve problems?",
                "answer": "algorithm",
                "difficulty": "Easy"
            }
        ],
        "hint": "Algorithm: The logical blueprint that silently orchestrates digital processes."
    },
    4: {
        "title": "Final Challenge",
        "description": "Using the hints you've collected, can you determine the secret word?",
        "question": "With a non-living device at its core, a process of absorbing and refining knowledge, and a hidden set of instructions guiding its every move, what modern, complex phenomenon emerges?",
        "answer": "artificial intelligence"
    }
}

# Function to skip current level
def skip_level():
    st.session_state.level += 1
    st.session_state.attempts = 0
    st.session_state.current_question_index = 0
    st.session_state.skipped_questions += 1
    st.session_state.show_empty_input_error = False
    st.rerun()

# Function to skip to next question within the same level
def skip_question():
    current_level = levels[st.session_state.level]
    num_questions = len(current_level["questions"])
    
    # Move to the next question in a circular manner (wrap around to first question after last)
    st.session_state.current_question_index = (st.session_state.current_question_index + 1) % num_questions
    st.session_state.show_empty_input_error = False
    st.rerun()

# Sidebar content
with st.sidebar:
    st.title("Your Progress")
    st.write("---")
    
    # Display current level
    st.subheader(f"Current Level: {st.session_state.level if st.session_state.level <= 3 else 'Final Challenge'}")
    
    # Display progress bar - starts at 0% and increases as levels are completed
    total_levels = 4
    # Adjust the calculation to start at 0% and end at 100%
    progress_percentage = (st.session_state.level - 1) / total_levels
    if st.session_state.level > total_levels:  # For completed game
        progress_percentage = 1.0
    
    st.write("Game Progress:")
    st.progress(progress_percentage)
    st.write(f"{int(progress_percentage * 100)}% complete")
    
    # Display collected hints
    st.subheader("Collected Hints:")
    if len(st.session_state.hints) == 0:
        st.write("No hints collected yet.")
    else:
        for i, hint in enumerate(st.session_state.hints, 1):
            st.success(f"Hint {i}: {hint}")
    
    # Display skipped questions
    if st.session_state.skipped_questions > 0:
        st.subheader("Skipped Levels:")
        st.write(f"You've skipped {st.session_state.skipped_questions} level(s).")
    
    # Reset game button
    if st.button("Start New Game", key="reset_game"):
        st.session_state.level = 1
        st.session_state.hints = []
        st.session_state.attempts = 0
        st.session_state.game_completed = False
        st.session_state.final_attempt = False
        st.session_state.current_question_index = 0
        st.session_state.skipped_questions = 0
        st.session_state.show_empty_input_error = False
        st.rerun()

# Main game area
st.title("🔍 Secret Word Quest")
st.write("---")

if not st.session_state.game_completed:
    # Current level content
    if st.session_state.level <= 3:
        current_level = levels[st.session_state.level]
        
        st.header(current_level["title"])
        st.write(current_level["description"])
        
        # Skip level button at the top
        if st.button("Skip This Level", key=f"skip_level_{st.session_state.level}", type="secondary", use_container_width=True):
            st.warning(f"Skipping Level {st.session_state.level}. You won't receive the hint for this level.")
            skip_level()
        
        # Display current question based on index
        current_question = current_level["questions"][st.session_state.current_question_index]
        
        st.subheader(f"Question ({current_question['difficulty']}):")
        st.write(current_question["text"])
        
        # User input
        user_answer = st.text_input("Your answer:", key=f"level_{st.session_state.level}_attempt_{st.session_state.attempts}_q_{st.session_state.current_question_index}")
        
        # Show error for empty input if needed
        if st.session_state.show_empty_input_error:
            st.error("Please enter an answer before submitting.")
        
        # Create two columns for buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Submit Answer", key=f"submit_{st.session_state.level}", use_container_width=True):
                if not user_answer.strip():
                    # Input is empty, show error
                    st.session_state.show_empty_input_error = True
                    st.rerun()
                else:
                    st.session_state.show_empty_input_error = False
                    # Check if answer is correct (case-insensitive)
                    if user_answer.lower() == current_question["answer"].lower():
                        st.success("Correct! You've earned a hint.")
                        st.session_state.hints.append(current_level["hint"])
                        st.session_state.level += 1
                        st.session_state.attempts = 0
                        st.session_state.current_question_index = 0
                        st.rerun()
                    else:
                        st.error("Incorrect answer. Try again or try another question.")
                        st.session_state.attempts += 1
        
        with col2:
            if st.button("Try Another Question", key=f"next_question_{st.session_state.level}", use_container_width=True):
                skip_question()
    
    # Final challenge
    else:
        final_level = levels[4]
        
        st.header(final_level["title"])
        st.write(final_level["description"])
        
        # Display collected hints summary
        st.subheader("Your Collected Hints:")
        if len(st.session_state.hints) == 0:
            st.write("You haven't collected any hints! This will be difficult.")
        else:
            for i, hint in enumerate(st.session_state.hints, 1):
                st.info(f"Hint {i}: {hint}")
        
        st.subheader("Final Question:")
        st.write(final_level["question"])
        
        # User input for final answer
        final_answer = st.text_input("Your final answer:", key="final_answer")
        
        # Show error for empty input if needed
        if st.session_state.show_empty_input_error:
            st.error("Please enter an answer before submitting.")
        
        if st.button("Submit Final Answer", key="submit_final", use_container_width=True):
            if not final_answer.strip():
                # Input is empty, show error
                st.session_state.show_empty_input_error = True
                st.rerun()
            else:
                st.session_state.show_empty_input_error = False
                if final_answer.lower() == final_level["answer"].lower():
                    st.balloons()
                    st.success("Congratulations! You've discovered the secret: Artificial Intelligence!")
                    st.session_state.game_completed = True
                else:
                    st.error("That's not correct. Review your hints and try again.")
                    st.session_state.final_attempt = True
else:
    # Game completed
    st.header("🎉 Quest Completed!")
    st.subheader("You've successfully discovered the secret: Artificial Intelligence!")
    
    collected_hints = len(st.session_state.hints)
    total_hints = 3
    
    st.write(f"You collected {collected_hints} out of {total_hints} hints.")
    st.write(f"You skipped {st.session_state.skipped_questions} level(s).")
    
    # Display performance message based on hints collected
    if collected_hints == 3:
        st.success("Perfect! You solved all the challenges and collected every hint.")
    elif collected_hints == 2:
        st.info("Well done! You collected most of the hints and still found the answer.")
    elif collected_hints == 1:
        st.warning("Not bad! You managed to find the answer with just one hint.")
    else:
        st.error("Impressive! You found the answer without any hints!")
    
    if st.button("Play Again", use_container_width=True):
        st.session_state.level = 1
        st.session_state.hints = []
        st.session_state.attempts = 0
        st.session_state.game_completed = False
        st.session_state.final_attempt = False
        st.session_state.current_question_index = 0
        st.session_state.skipped_questions = 0
        st.session_state.show_empty_input_error = False
        st.rerun()

# Add styling
st.markdown("""
<style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        margin: 10px 0;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stButton button[data-testid*="skip_level"] {
        background-color: #f44336;
    }
    .stButton button[data-testid*="skip_level"]:hover {
        background-color: #d32f2f;
    }
    .stButton button[data-testid*="next_question"] {
        background-color: #ff9800;
    }
    .stButton button[data-testid*="next_question"]:hover {
        background-color: #e68a00;
    }
    .css-1aumxhk {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    /* Add styling for the progress bar */
    div.stProgress > div > div {
        background-color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)