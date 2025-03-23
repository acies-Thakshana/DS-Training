import streamlit as st
import random
import time

if 'target_number' not in st.session_state:
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0

def reset_game():
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.success("Game reset! Start guessing again.")

st.set_page_config(page_title="Number Guessing Game", layout="wide")
st.title("🔢 **The Ultimate Number Guessing Game** 🎯")
st.markdown("### 🤔 Can you guess the number between **1 and 100**? 🤔")

col1, col2 = st.columns([2, 1])

with col1:
    user_guess = st.number_input("🎯 Enter your guess:", min_value=1, max_value=100, step=1)

    if st.button("🚀 Submit Guess"):
        st.session_state.attempts += 1
        with st.spinner("Checking your guess..."):
            time.sleep(1)
        
        if user_guess < st.session_state.target_number:
            st.warning("📉 Too low! Try again.")
            st.image(random.choice([
                "https://media.giphy.com/media/l4FGI8GoTL7N4DsyI/giphy.gif",
                "https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif",
                "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif"
            ]), width=200)
        elif user_guess > st.session_state.target_number:
            st.warning("📈 Too high! Try again.")
            st.image(random.choice([
                "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif",
                "https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif",
                "https://media.giphy.com/media/l4KibK3JwaVo0CjDO/giphy.gif"
            ]), width=200)
        else:
            st.success(f"🎉 Correct! The number was {st.session_state.target_number}. You guessed it in {st.session_state.attempts} attempts!")
            st.balloons()
            st.image(random.choice([
                "https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif",
                "https://media.giphy.com/media/5GoVLqeAOo6PK/giphy.gif",
                "https://media.giphy.com/media/3o6UBpHgaXFDNAuttm/giphy.gif"
            ]), width=200)

with col2:
    if st.button("🔄 Restart Game"):
        reset_game()
