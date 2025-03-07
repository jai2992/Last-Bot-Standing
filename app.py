import streamlit as st
import random
import os
from groq import Groq

st.set_page_config(
    page_title="Secret Word Quest",
    page_icon="🔍",
    layout="centered"
)

try:
    client = Groq(
        api_key=st.secrets["connections"]["groq_api_key"],
    )
except:
    client = None

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
if 'show_level_completed_popup' not in st.session_state:
    st.session_state.show_level_completed_popup = False
if 'completed_level' not in st.session_state:
    st.session_state.completed_level = 0
if 'llm_suggestion' not in st.session_state:
    st.session_state.llm_suggestion = ""

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

def get_llm_suggestion(question, answer, user_answer=None):
    """Get a simple hint from the LLM related to the question and answer, considering the user's previous attempt."""
    if client is None:
        if user_answer:
            return f"'{user_answer}' is close, but think about what performs tasks without life."
        return "Think carefully, the answer is closer than you think."
    
    try:
        # Add the user's answer to the prompt if available
        user_answer_text = f"The player's incorrect answer was: \"{user_answer}\"" if user_answer else "The player has not provided an answer yet."
        
        prompt = f"""
        You are a helpful assistant in a word puzzle game.

        The player is trying to answer a riddle, and you must provide a simple, helpful hint that subtly guides them toward the correct answer without giving it away directly.

        The riddle is: "{question}"
        The correct answer is: "{answer}"
        {user_answer_text}

        Give a SHORT and clear hint (maximum 15 words) that:
        1. Acknowledges their attempt if they made one (by briefly mentioning their answer)
        2. Nudges the player in the right direction toward the correct answer
        
        Your response must be ONLY the hint - no explanations, no prefixes, just the hint itself.
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            max_tokens=50
        )
        
        suggestion = chat_completion.choices[0].message.content.strip().strip('"')
        # Ensure it's not too long
        if len(suggestion.split()) > 15:
            suggestion = " ".join(suggestion.split()[:15]) + "..."
        return suggestion
    except Exception as e:
        if user_answer:
            return f"'{user_answer}' isn't quite right. Look for clues in the question itself."
        return "Look for clues in the question itself."


def skip_level():
    st.session_state.level += 1
    st.session_state.attempts = 0
    st.session_state.current_question_index = 0
    st.session_state.skipped_questions += 1
    st.session_state.show_empty_input_error = False
    st.session_state.llm_suggestion = ""
    st.rerun()

def skip_question():
    current_level = levels[st.session_state.level]
    num_questions = len(current_level["questions"])
    
    st.session_state.current_question_index = (st.session_state.current_question_index + 1) % num_questions
    st.session_state.show_empty_input_error = False
    st.session_state.llm_suggestion = ""
    st.rerun()

def close_level_popup():
    st.session_state.show_level_completed_popup = False
    st.rerun()

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    
    .main-title {
        font-family: 'Press Start 2P', cursive;
        color: #6a0dad;
        text-shadow: 3px 3px 0px #ffd700;
        padding: 10px;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 20px;
        letter-spacing: 2px;
    }
    
    .level-title {
        font-family: 'Orbitron', sans-serif;
        color: #1e88e5;
        text-shadow: 1px 1px 0px #4fc3f7;
        font-weight: 700;
        border-bottom: 2px solid #4fc3f7;
        padding-bottom: 10px;
    }
    
    .game-text {
        font-family: 'VT323', monospace;
        font-size: 1.3rem;
        line-height: 1.4;
    }
    
    .question-text {
        font-family: 'VT323', monospace;
        font-size: 1.5rem;
        border-left: 4px solid #ff9800;
        padding-left: 10px;
        margin: 15px 0;
        background-color: rgba(255, 152, 0, 0.1);
        padding: 10px;
        border-radius: 0 5px 5px 0;
    }
    
    .difficulty-badge {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.75rem;
        font-weight: 500;
        padding: 3px 8px;
        border-radius: 10px;
        color: white;
    }
    
    .difficulty-hard {
        background-color: #f44336;
    }
    
    .difficulty-medium {
        background-color: #ff9800;
    }
    
    .difficulty-easy {
        background-color: #4caf50;
    }
    
    .hint-box {
        font-family: 'VT323', monospace;
        font-size: 1.2rem;
        background-color: rgba(76, 175, 80, 0.1);
        border: 2px solid #4caf50;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    
    .game-container {
        background-color: #121212;
        color: #e0e0e0;
        padding: 20px;
        border-radius: 15px;
        border: 3px solid #ffd700;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
    }
    
    .sidebar-title {
        font-family: 'Orbitron', sans-serif;
        color: #6a0dad;
        text-align: center;
        border-bottom: 2px solid #6a0dad;
        padding-bottom: 5px;
        margin-bottom: 10px;
    }
    
    .sidebar-content {
        font-family: 'VT323', monospace;
        font-size: 1.2rem;
    }
    
    .stButton button {
        font-family: 'Orbitron', sans-serif;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        margin: 10px 0;
        border: 2px solid #2e7d32;
        box-shadow: 0 4px 0 #2e7d32;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        background-color: #45a049;
        transform: translateY(2px);
        box-shadow: 0 2px 0 #2e7d32;
    }
    
    .stButton button:active {
        transform: translateY(4px);
        box-shadow: none;
    }
    
    button[data-testid*="skip_level"] {
        background-color: #f44336;
        border: 2px solid #d32f2f;
        box-shadow: 0 4px 0 #d32f2f;
    }
    
    button[data-testid*="skip_level"]:hover {
        background-color: #e53935;
        box-shadow: 0 2px 0 #d32f2f;
    }
    
    button[data-testid*="next_question"] {
        background-color: #ff9800;
        border: 2px solid #f57c00;
        box-shadow: 0 4px 0 #f57c00;
    }
    
    button[data-testid*="next_question"]:hover {
        background-color: #fb8c00;
        box-shadow: 0 2px 0 #f57c00;
    }
    
    button[data-testid*="continue_button"] {
        background-color: #2196f3;
        border: 2px solid #1976d2;
        box-shadow: 0 4px 0 #1976d2;
    }
    
    button[data-testid*="continue_button"]:hover {
        background-color: #1e88e5;
        box-shadow: 0 2px 0 #1976d2;
    }
    
    div.stProgress > div > div {
        background-color: #ffd700;
    }
    
    .css-1aumxhk {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border: 2px solid #ffd700;
    }
    
    input[type="text"] {
        font-family: 'VT323', monospace;
        font-size: 1.3rem;
        background-color: #212121;
        color: #e0e0e0;
        border: 2px solid #4fc3f7;
        border-radius: 5px;
        padding: 10px;
    }
    
    .level-complete-popup {
        font-family: 'Press Start 2P', cursive;
        background: linear-gradient(135deg, #4a148c, #7b1fa2);
        color: white;
        padding: 25px;
        border-radius: 15px;
        border: 4px solid #ffd700;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .level-complete-popup::before {
        content: "";
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        background: linear-gradient(45deg, #ffd700, transparent, #ffd700, transparent);
        background-size: 400% 400%;
        animation: shimmer 3s infinite;
        z-index: -1;
        opacity: 0.3;
    }
    
    @keyframes shimmer {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    .hint-reveal {
        font-family: 'Orbitron', sans-serif;
        background-color: #212121;
        color: #ffd700;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #ffd700;
        text-align: center;
        font-size: 1.1rem;
        margin: 15px 0;
        letter-spacing: 1px;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.3) inset;
    }
    
    .completion-title {
        font-family: 'Press Start 2P', cursive;
        color: #ffd700;
        text-shadow: 2px 2px 0px #6a0dad;
        text-align: center;
        font-size: 2rem;
        margin-bottom: 20px;
        animation: pulse 2s infinite;
    }
    
    .suggestion-box {
        font-family: 'Orbitron', sans-serif;
        background-color: #673ab7;
        color: white;
        padding: 12px;
        border-radius: 8px;
        border: 2px solid #9c27b0;
        margin: 10px 0;
        font-size: 0.9rem;
        box-shadow: 0 0 10px rgba(156, 39, 176, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .suggestion-box::before {
        content: "✨ MYSTIC GUIDANCE";
        position: absolute;
        top: 5px;
        left: 10px;
        font-size: 0.7rem;
        opacity: 0.8;
    }
    
    .suggestion-text {
        margin-top: 15px;
        text-align: center;
        font-style: italic;
    }
    
    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            transform: scale(1);
        }
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-title"><h2>YOUR QUEST LOG</h2></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown(f'<h3>CURRENT MISSION: {st.session_state.level if st.session_state.level <= 3 else "FINAL CHALLENGE"}</h3>', unsafe_allow_html=True)
    
    total_levels = 4
    progress_percentage = (st.session_state.level - 1) / total_levels
    if st.session_state.level > total_levels:
        progress_percentage = 1.0
    
    st.markdown('<p>QUEST PROGRESS:</p>', unsafe_allow_html=True)
    st.progress(progress_percentage)
    st.markdown(f'<p>{int(progress_percentage * 100)}% COMPLETE</p>', unsafe_allow_html=True)
    
    st.markdown('<h3>COLLECTED ARTIFACTS:</h3>', unsafe_allow_html=True)
    if len(st.session_state.hints) == 0:
        st.markdown('<p>No artifacts discovered yet.</p>', unsafe_allow_html=True)
    else:
        for i, hint in enumerate(st.session_state.hints, 1):
            st.markdown(f'<div class="hint-box">🔍 ARTIFACT {i}: {hint}</div>', unsafe_allow_html=True)
    
    if st.session_state.skipped_questions > 0:
        st.markdown('<h3>ABANDONED QUESTS:</h3>', unsafe_allow_html=True)
        st.markdown(f'<p>You\'ve abandoned {st.session_state.skipped_questions} quest(s).</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("START NEW QUEST", key="reset_game"):
        st.session_state.level = 1
        st.session_state.hints = []
        st.session_state.attempts = 0
        st.session_state.game_completed = False
        st.session_state.final_attempt = False
        st.session_state.current_question_index = 0
        st.session_state.skipped_questions = 0
        st.session_state.show_empty_input_error = False
        st.session_state.show_level_completed_popup = False
        st.session_state.llm_suggestion = ""
        st.rerun()

st.markdown('<h1 class="main-title">🔍 SECRET WORD QUEST</h1>', unsafe_allow_html=True)
st.markdown('<div class="game-container">', unsafe_allow_html=True)

if st.session_state.show_level_completed_popup:
    completed_level = st.session_state.completed_level
    hint = levels[completed_level]["hint"]
    
    popup_container = st.container()
    with popup_container:
        popup_col1, popup_col2, popup_col3 = st.columns([1, 3, 1])
        with popup_col2:
            st.markdown("""
            <div class="level-complete-popup">
                <h2 style="text-align: center;">🎉 LEVEL COMPLETE! 🎉</h2>
                <p style="font-size: 14px; text-align: center; margin: 20px 0;">CONGRATULATIONS, ADVENTURER!</p>
                <p style="font-size: 14px; text-align: center;">YOU HAVE COMPLETED LEVEL {level}!</p>
                <p style="font-size: 12px; text-align: center; margin-top: 20px;"><strong>NEW ARTIFACT DISCOVERED:</strong></p>
                <div class="hint-reveal">{hint}</div>
            </div>
            """.format(level=completed_level, hint=hint), unsafe_allow_html=True)
            
            if st.button("CONTINUE YOUR QUEST", key="continue_button", use_container_width=True):
                close_level_popup()

if not st.session_state.game_completed and not st.session_state.show_level_completed_popup:
    if st.session_state.level <= 3:
        current_level = levels[st.session_state.level]
        
        st.markdown(f'<h2 class="level-title">{current_level["title"]}</h2>', unsafe_allow_html=True)
        st.markdown(f'<p class="game-text">{current_level["description"]}</p>', unsafe_allow_html=True)
        
        if st.button("ABANDON THIS QUEST", key=f"skip_level_{st.session_state.level}", type="secondary", use_container_width=True):
            st.warning(f"Abandoning quest for Level {st.session_state.level}. You won't receive the artifact for this level.")
            skip_level()
        
        current_question = current_level["questions"][st.session_state.current_question_index]
        difficulty_class = f"difficulty-badge difficulty-{current_question['difficulty'].lower()}"
        
        st.markdown(f'<div><span class="{difficulty_class}">{current_question["difficulty"]}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="question-text">{current_question["text"]}</div>', unsafe_allow_html=True)
        
        # Display suggestion if there is one (only after incorrect attempt)
        if st.session_state.llm_suggestion:
            st.markdown(f'''
            <div class="suggestion-box">
                <div class="suggestion-text">{st.session_state.llm_suggestion}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        user_answer = st.text_input("YOUR ANSWER:", key=f"level_{st.session_state.level}_attempt_{st.session_state.attempts}_q_{st.session_state.current_question_index}")
        
        if st.session_state.show_empty_input_error:
            st.error("You must provide an answer before proceeding!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("SUBMIT ANSWER", key=f"submit_{st.session_state.level}", use_container_width=True):
                if not user_answer.strip():
                    st.session_state.show_empty_input_error = True
                    st.rerun()
                else:
                    st.session_state.show_empty_input_error = False
                    if user_answer.lower() == current_question["answer"].lower():
                        st.session_state.hints.append(current_level["hint"])
                        st.session_state.completed_level = st.session_state.level
                        st.session_state.level += 1
                        st.session_state.attempts = 0
                        st.session_state.current_question_index = 0
                        st.session_state.llm_suggestion = ""
                        st.session_state.show_level_completed_popup = True
                        st.rerun()
                    else:
                        st.error("Incorrect! The ancient text remains unclear. Try again or seek another riddle.")
                        st.session_state.attempts += 1
                        # Get suggestion from LLM after incorrect answer
                        st.session_state.llm_suggestion = get_llm_suggestion(
                            current_question["text"], 
                            current_question["answer"],
                            user_answer
                        )
                        st.rerun()
        
        with col2:
            if st.button("TRY ANOTHER RIDDLE", key=f"next_question_{st.session_state.level}", use_container_width=True):
                skip_question()
    
    else:
        final_level = levels[4]
        
        st.markdown(f'<h2 class="level-title">{final_level["title"]}</h2>', unsafe_allow_html=True)
        st.markdown(f'<p class="game-text">{final_level["description"]}</p>', unsafe_allow_html=True)
        
        st.markdown('<h3>YOUR COLLECTED ARTIFACTS:</h3>', unsafe_allow_html=True)
        if len(st.session_state.hints) == 0:
            st.markdown('<p class="game-text">You haven\'t collected any artifacts! The challenge ahead will be formidable.</p>', unsafe_allow_html=True)
        else:
            for i, hint in enumerate(st.session_state.hints, 1):
                st.markdown(f'<div class="hint-box">🔍 ARTIFACT {i}: {hint}</div>', unsafe_allow_html=True)
        
        st.markdown('<h3>THE FINAL ENIGMA:</h3>', unsafe_allow_html=True)
        st.markdown(f'<div class="question-text">{final_level["question"]}</div>', unsafe_allow_html=True)
        
        # Display suggestion if there is one (only after incorrect attempt)
        if st.session_state.llm_suggestion:
            st.markdown(f'''
            <div class="suggestion-box">
                <div class="suggestion-text">{st.session_state.llm_suggestion}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        final_answer = st.text_input("YOUR FINAL ANSWER:", key="final_answer")
        
        if st.session_state.show_empty_input_error:
            st.error("You must provide an answer to complete your quest!")
        
        if st.button("REVEAL THE SECRET", key="submit_final", use_container_width=True):
            if not final_answer.strip():
                st.session_state.show_empty_input_error = True
                st.rerun()
            else:
                st.session_state.show_empty_input_error = False
                if final_answer.lower() == final_level["answer"].lower():
                    st.balloons()
                    st.success("CONGRATULATIONS! You've uncovered the ancient secret: ARTIFICIAL INTELLIGENCE!")
                    st.session_state.game_completed = True
                else:
                    st.error("The secret remains hidden. Review your artifacts and try again, brave adventurer.")
                    st.session_state.final_attempt = True
                    # Get suggestion from LLM after incorrect final answer
                    collected_hints_text = ", ".join([h.split(":")[0] for h in st.session_state.hints]) if st.session_state.hints else "No hints collected"
                    st.session_state.llm_suggestion = get_llm_suggestion(
                        f"Final challenge: {final_level['question']} (Player has collected hints about: {collected_hints_text})", 
                        final_level["answer"]
                    )
                    st.rerun()
else:
    if not st.session_state.show_level_completed_popup:
        st.markdown('<h2 class="completion-title">🎉 QUEST COMPLETED! 🎉</h2>', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; color: #ffd700;">You\'ve successfully uncovered the ancient secret:</h3>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; font-family: \'Press Start 2P\', cursive; color: #4caf50; text-shadow: 2px 2px 0px #1b5e20; margin: 20px 0;">ARTIFICIAL INTELLIGENCE</h2>', unsafe_allow_html=True)
        
        collected_hints = len(st.session_state.hints)
        total_hints = 3
        
        st.markdown(f'<p class="game-text" style="text-align: center;">You collected {collected_hints} out of {total_hints} artifacts.</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="game-text" style="text-align: center;">You abandoned {st.session_state.skipped_questions} quest(s).</p>', unsafe_allow_html=True)
        
        if collected_hints == 3:
            st.markdown('<div style="text-align: center; background-color: #4caf50; color: white; padding: 15px; border-radius: 10px; margin: 20px 0; font-family: \'Orbitron\', sans-serif;">PERFECT! You solved all challenges and collected every artifact. A true master of puzzles!</div>', unsafe_allow_html=True)
        elif collected_hints == 2:
            st.markdown('<div style="text-align: center; background-color: #2196f3; color: white; padding: 15px; border-radius: 10px; margin: 20px 0; font-family: \'Orbitron\', sans-serif;">WELL DONE! You collected most of the artifacts and still found the answer. Your wisdom is impressive!</div>', unsafe_allow_html=True)
        elif collected_hints == 1:
            st.markdown('<div style="text-align: center; background-color: #ff9800; color: white; padding: 15px; border-radius: 10px; margin: 20px 0; font-family: \'Orbitron\', sans-serif;">NOT BAD! You managed to find the answer with just one artifact. Your intuition is strong!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: center; background-color: #f44336; color: white; padding: 15px; border-radius: 10px; margin: 20px 0; font-family: \'Orbitron\', sans-serif;">IMPRESSIVE! You found the answer without any artifacts! You are truly a legendary puzzle solver!</div>', unsafe_allow_html=True)
        
        if st.button("EMBARK ON A NEW QUEST", use_container_width=True):
            st.session_state.level = 1
            st.session_state.hints = []
            st.session_state.attempts = 0
            st.session_state.game_completed = False
            st.session_state.final_attempt = False
            st.session_state.current_question_index = 0
            st.session_state.skipped_questions = 0
            st.session_state.show_empty_input_error = False
            st.session_state.show_level_completed_popup = False
            st.session_state.llm_suggestion = ""
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
            
