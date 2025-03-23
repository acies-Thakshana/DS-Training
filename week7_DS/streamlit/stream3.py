import streamlit as st
import numpy as np

st.set_page_config(page_title="Tic-Tac-Toe", page_icon="🎮", layout="centered")

# Sidebar Navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["Game", "Leaderboard"])

# Initialize session state for game
if "board" not in st.session_state:
    st.session_state.board = np.full((3, 3), "")
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.loser = None
    st.session_state.moves = 0
    st.session_state.invalid_move = False
    st.session_state.game_over = False

# Keep leaderboard and scores persistent
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []  # Stores last 5 games
if "scores" not in st.session_state:
    st.session_state.scores = {}  # Stores player scores

if page == "Game":
    st.title("🎮 Tic-Tac-Toe")

    # Player name inputs
    col1, col2 = st.columns(2)
    with col1:
        player1 = st.text_input("Player 1 Name", value="Player 1")
    with col2:
        player2 = st.text_input("Player 2 Name", value="Player 2")

    if not player1.strip() or not player2.strip():
        st.warning("⚠️ Both players must enter their names to start the game!")
        st.stop()

    # Store player names only if not already stored
    if "player1" not in st.session_state:
        st.session_state.player1 = player1
    if "player2" not in st.session_state:
        st.session_state.player2 = player2

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

    def is_draw():
        return st.session_state.moves == 9 and st.session_state.winner is None

    def get_player_name(symbol):
        return st.session_state.player1 if symbol == "X" else st.session_state.player2

    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            with cols[j]:
                if st.button(st.session_state.board[i, j] or " ", key=f"{i}-{j}", disabled=st.session_state.game_over):
                    if st.session_state.board[i, j] == "" and not st.session_state.game_over:
                        st.session_state.board[i, j] = st.session_state.current_player
                        st.session_state.moves += 1

                        st.session_state.winner = check_winner(st.session_state.board)

                        if st.session_state.winner:
                            winner_name = get_player_name(st.session_state.winner)
                            loser_symbol = "O" if st.session_state.winner == "X" else "X"
                            st.session_state.loser = get_player_name(loser_symbol)
                            st.session_state.game_over = True

                            if winner_name not in st.session_state.scores:
                                st.session_state.scores[winner_name] = 0
                            st.session_state.scores[winner_name] += 1

                            st.session_state.leaderboard.insert(0, f"{winner_name} won against {st.session_state.loser}")
                            if len(st.session_state.leaderboard) > 5:
                                st.session_state.leaderboard.pop()

                            st.success(f"🎉 {winner_name} wins!")
                            

                        elif is_draw():
                            st.warning("🤝 It's a draw!")
                            st.session_state.game_over = True
                            st.session_state.leaderboard.insert(0, "Game ended in a draw")
                            if len(st.session_state.leaderboard) > 5:
                                st.session_state.leaderboard.pop()

                        else:
                            st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"

                        st.session_state.invalid_move = False
                        st.rerun()
                    
                    else:
                        st.session_state.invalid_move = True

    if st.session_state.invalid_move:
        st.warning("🚫 Invalid move! Block already selected.")

    elif st.session_state.winner:
        winner_name = get_player_name(st.session_state.winner)
        loser_name = st.session_state.loser
        st.success(f"🎉 {winner_name} wins!")

    elif is_draw():
        st.warning("🤝 It's a draw!")

    # Reset Button (Does NOT clear leaderboard)
    if st.button("🔄 Reset Game"):
        st.session_state.board = np.full((3, 3), "")
        st.session_state.current_player = "X"
        st.session_state.winner = None
        st.session_state.loser = None
        st.session_state.moves = 0
        st.session_state.invalid_move = False
        st.session_state.game_over = False
        st.rerun()

elif page == "Leaderboard":
    st.title("🏆 Leaderboard")

    st.subheader("📋 Last 5 Games")
    if st.session_state.leaderboard:
        for game in st.session_state.leaderboard:
            st.write(f"- {game}")
    else:
        st.write("No games played yet.")

    st.subheader("🎯 Player Scores")
    if st.session_state.scores:
        for player, score in st.session_state.scores.items():
            st.write(f"🎖️ {player}: {score} wins")
    else:
        st.write("No scores available yet.")
