import streamlit as st
import random
import time
import chess


def random_move(board):
    legal_moves = list(board.legal_moves)
    return [random.choice(legal_moves)]


def is_move_legal(board, move):
    return move in board.legal_moves


board = chess.Board()


st.title("Simple blind-chess chat-bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is your move?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    try:
        board.push_san(prompt)
        with st.chat_message("assistant"):
            bot_move = random_move(board)
            response = st.write_stream([board.san(m) for m in bot_move])
            board.push(bot_move[0])
    except ValueError:
        with st.chat_message("assistant"):
            response = st.write_stream("This is not a legal move.")
    st.session_state.messages.append({"role": "assistant", "content": response})
