import streamlit as st
import numpy as np

# Set default theme
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Function to check winner
def check_winner(board):
    for i in range(3):
        if all(board[i, :] == 'X') or all(board[:, i] == 'X'):
            return 'X'
        if all(board[i, :] == 'O') or all(board[:, i] == 'O'):
            return 'O'
    
    if all(np.diag(board) == 'X') or all(np.diag(np.fliplr(board)) == 'X'):
        return 'X'
    if all(np.diag(board) == 'O') or all(np.diag(np.fliplr(board)) == 'O'):
        return 'O'
    
    return None

# Theme Colors
def apply_theme():
    if st.session_state.dark_mode:
        bg_color = "#121212"
        text_color = "#E0E0E0"
        button_color = "#333333"
    else:
        bg_color = "#FFFFFF"
        text_color = "#000000"
        button_color = "#DDDDDD"
    
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-color: {bg_color};
                color: {text_color};
            }}
            .stButton>button {{
                background-color: {button_color} !important;
                color: {text_color} !important;
                font-weight: bold;
                border-radius: 8px;
                width: 100px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    st.title("🎮 Tic-Tac-Toe")
    
    # Toggle Light/Dark Mode
    if st.button("🌞 Toggle Mode 🌙"):
        st.session_state.dark_mode = not st.session_state.dark_mode

    # Apply Theme
    apply_theme()

    # Player name inputs
    if 'player_x' not in st.session_state:
        st.session_state.player_x = ""
        st.session_state.player_o = ""

    st.session_state.player_x = st.text_input("Enter Player X Name:", st.session_state.player_x)
    st.session_state.player_o = st.text_input("Enter Player O Name:", st.session_state.player_o)

    if st.button("Start Game"):
        st.session_state.board = np.full((3, 3), '', dtype=str)
        st.session_state.current_player = 'X'
        st.session_state.winner = None

    # Initialize game state
    if 'board' not in st.session_state:
        st.session_state.board = np.full((3, 3), '', dtype=str)
        st.session_state.current_player = 'X'
        st.session_state.winner = None

    # Tic-Tac-Toe grid
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            button_label = st.session_state.board[i, j] if st.session_state.board[i, j] else " "
            if cols[j].button(button_label, key=f"btn_{i}_{j}"): 
                if not st.session_state.winner and st.session_state.board[i, j] == '':
                    st.session_state.board[i, j] = st.session_state.current_player
                    st.session_state.winner = check_winner(st.session_state.board)

                    if st.session_state.winner is None:
                        st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'

    # Display game result
    if st.session_state.winner:
        winner_name = st.session_state.player_x if st.session_state.winner == 'X' else st.session_state.player_o
        st.success(f"🎉 Congratulations, {winner_name}! You win! 🎊")
        st.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExcGtqdWhoZnl2M2FjeHd6ZWpmcWExNngyZ285b2RobWxoYmRza3hlbCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/t3sZxY5zS5B0z5zMIz/giphy.gif", use_container_width=True)

    elif '' not in st.session_state.board:
        st.warning("🤝 It's a draw!")
        st.image("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDY5b2l4bnFvejZrM24zZjZmeWZmM3UyeG1jbXZncWRqamJpeWhkbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/zj9phLUdgVJzwfJjf5/giphy.gif", use_container_width=True)

    st.markdown("---") 
    if st.button("🔄 Reset Game"):
        st.session_state.board = np.full((3, 3), '', dtype=str)
        st.session_state.current_player = 'X'
        st.session_state.winner = None

if __name__ == "__main__":
    main()
