import streamlit as st
import numpy as np

# Page Config
st.set_page_config(page_title="Tic-Tac-Toe Game", page_icon="🎮", layout="centered")

# Navigation Menu
page = st.sidebar.radio("📍 Navigate", ["🎮 Play Game", "🏆 Leaderboard"])

# Initialize session state variables if not already set
if "board" not in st.session_state:
    st.session_state.board = np.full((3, 3), "")
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.moves = 0
    st.session_state.scores = []  # Stores last 5 games

# **🏆 Leaderboard Page**
if page == "🏆 Leaderboard":
    st.title("🏆 Leaderboard - Last 5 Games")

    if len(st.session_state.scores) == 0:
        st.info("No games played yet! Play a game to see results.")
    else:
        for game in st.session_state.scores[::-1]:  # Show latest games first
            st.success(f"🎉 {game['winner']} won against {game['loser']}")

    # Back to game button
    if st.button("🔙 Back to Game"):
        st.rerun()

# **🎮 Game Page**
elif page == "🎮 Play Game":
    st.title("🎮 Tic-Tac-Toe ")

    # Two columns for Player names
    col1, col2 = st.columns(2)
    with col1:
        player1 = st.text_input("Player 1 Name", key="p1")
    with col2:
        player2 = st.text_input("Player 2 Name", key="p2")

    # **Prevent Play if Names are Empty**
    if not player1.strip() or not player2.strip():
        st.warning("⚠️ Both players must enter their names to start the game!")

        # **Show Error GIF**
        # st.image("https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif", width=200)
        # st.image("https://tenor.com/bVqit.gif", width=200)
        st.stop()

    # **Check for Winner**
    def check_winner(board):
        for i in range(3):
            if board[i, 0] == board[i, 1] == board[i, 2] and board[i, 0] != "":
                return board[i, 0]
            if board[0, i] == board[1, i] == board[2, i] and board[0, i] != "":
                return board[0, i]

        if board[0, 0] == board[1, 1] == board[2, 2] and board[0, 0] != "":
            return board[0, 0]
        if board[0, 2] == board[1, 1] == board[2, 0] and board[0, 2] != "":
            return board[0, 2]

        return None

    # Check if game is a draw
    def is_draw():
        return st.session_state.moves == 9 and st.session_state.winner is None

    # **Display Tic-Tac-Toe Grid**
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            with cols[j]:
                if st.button(st.session_state.board[i, j] or " ", key=f"{i}-{j}", disabled=st.session_state.winner is not None):
                    if st.session_state.board[i, j] == "" and st.session_state.winner is None:
                        st.session_state.board[i, j] = st.session_state.current_player
                        st.session_state.moves += 1  # Increment move count
                        
                        # Check for a winner
                        st.session_state.winner = check_winner(st.session_state.board)

                        if st.session_state.winner:
                            st.success(f"🎉 {player1 if st.session_state.winner == 'X' else player2} wins!")
                            
                            # **Winning & Losing GIFs Side-by-Side**
                            col_win, col_lose = st.columns(2)
                            with col_win:
                                # st.image("https://media.giphy.com/media/3o7abldj0b3rxrZUxW/giphy.gif", width=150)
                                # st.image("https://i.gifer.com/Be.gif", width=250)
                                st.write(f"🎉 {player1 if st.session_state.winner == 'X' else player2} Wins!")

                            with col_lose:
                                # st.image("https://media.giphy.com/media/1xVb3ZNsRJH6PnjMzU/giphy.gif", width=150)
                                # st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZG8yMHoyYjl2bGF6N3JvcHU2czAyZnc1NW5yeTJ1eXN0ZXZnb204ciZlcD12MV9zdGlja2Vyc19zZWFyY2gmY3Q9dHM/XEzOr6WMnC5O5gOGAI/giphy.gif",width=150)
                                st.write(f"😢 {player2 if st.session_state.winner == 'X' else player1} Loses!")

                            # Store in leaderboard
                            st.session_state.scores.append({
                                "winner": player1 if st.session_state.winner == "X" else player2,
                                "loser": player2 if st.session_state.winner == "X" else player1
                            })
                            st.session_state.scores = st.session_state.scores[-5:]  # Keep last 5 games

                        elif is_draw():
                            st.warning("🤝 It's a draw!")
                            # st.image("https://media.giphy.com/media/5xtDarlqG5OdDZrDb7W/giphy.gif", width=200)
                            # st.image("https://tenor.com/MgLe.gif", width=300)
                        else:
                            # Switch player
                            st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"

                        st.rerun()

    # **Show Game Result**
    if st.session_state.winner:
        st.success(f"🎉 {player1 if st.session_state.winner == 'X' else player2} wins!")
    elif is_draw():
        st.warning("🤝 It's a draw!")

    # **Reset Game Button**
    if st.button("🔄 Reset Game"):
        st.session_state.board = np.full((3, 3), "")
        st.session_state.current_player = "X"
        st.session_state.winner = None
        st.session_state.moves = 0
        st.rerun()
