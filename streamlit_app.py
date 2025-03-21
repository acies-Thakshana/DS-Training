import streamlit as st
import random
import json
import time

LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            data = f.read().strip()
            return json.loads(data) if data else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=4)

# Initialize session state
if 'random_number' not in st.session_state:
    st.session_state.random_number = random.randint(1, 10)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.start_time = time.time()
    st.session_state.hints_used = False
    st.session_state.leaderboard = load_leaderboard()
    st.session_state.name = ""
    st.session_state.score_saved = False

st.title("Number Guessing Game 🎯")
st.image("https://media.tenor.com/dHyGpx4Q3NoAAAAM/guess-dog.gif", use_container_width=True)

if not st.session_state.game_over:
    guess = st.number_input("Enter your guess (1-10):", min_value=1, max_value=10, step=1, key="guess")
    submit = st.button("Go For It!")

    if submit:
        st.session_state.attempts += 1
        
        if guess < st.session_state.random_number:
            st.image("https://i.makeagif.com/media/4-25-2023/1gitjh.gif", use_container_width=True)
            st.warning("Too Low! Try Again")
        elif guess > st.session_state.random_number:
            st.image("https://media3.giphy.com/media/63JznOhHCJ9MdCHCw0/200w.gif", use_container_width=True)
            st.warning("Too High! Try Again")
        else:
            end_time = time.time()
            time_taken = round(end_time - st.session_state.start_time, 2)
            st.image("https://media.tenor.com/97ePZDIfWPQAAAAM/you%27re-goddamn-right-heisenberg-you%27re-goddamn-right.gif", use_container_width=True)
            st.success(f"Congratulations! You guessed the number in {st.session_state.attempts} attempts and {time_taken} seconds!!!")
            st.balloons()
            st.session_state.game_over = True
            st.session_state.time_taken = time_taken

    # Hint System
    if st.session_state.attempts >= 3 and not st.session_state.hints_used:
        if st.button("Get a Hint 🔍", key="hint_button"):
            hint = "even" if st.session_state.random_number % 2 == 0 else "odd"
            st.session_state.hint_text = f"Hint: The number is {hint}!"
            st.session_state.hints_used = True
    
    if st.session_state.hints_used:
        st.info(st.session_state.hint_text)

if st.session_state.game_over and not st.session_state.score_saved:
    st.session_state.name = st.text_input("Enter your name for the leaderboard:", key="name_input")
    if st.button("Save Score"):
        if st.session_state.name:
            st.session_state.leaderboard.append({"name": st.session_state.name, "attempts": st.session_state.attempts, "time": st.session_state.time_taken})
            st.session_state.leaderboard = sorted(st.session_state.leaderboard, key=lambda x: (x['attempts'], x['time']))[:5]  # Keep top 5
            save_leaderboard(st.session_state.leaderboard)
            st.session_state.score_saved = True
            st.success("Score saved!")
        else:
            st.warning("Please enter your name before saving!")

if st.session_state.game_over:
    if st.button("Play Again"):
        st.session_state.random_number = random.randint(1, 10)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.start_time = time.time()
        st.session_state.hints_used = False
        st.session_state.hint_text = ""
        st.session_state.score_saved = False
        st.session_state.name = ""
        st.rerun()

# Display Leaderboard
st.sidebar.title("🏆 Leaderboard")
if st.session_state.leaderboard:
    for idx, entry in enumerate(st.session_state.leaderboard, 1):
        st.sidebar.write(f"{idx}. {entry['name']} - {entry['attempts']} attempts in {entry['time']}s")
else:
    st.sidebar.write("No scores yet. Be the first!")
