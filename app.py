import streamlit as st
import random
import chess

# import time


def is_a_draw(board):
    message = ""
    isdraw = False
    if board.is_stalemate():
        message = "Stalemate"
        isdraw = True
    elif board.is_insufficient_material():
        message = "Insufficient Material"
        isdraw = True
    elif board.can_claim_fifty_moves():
        message = "Fifty Moves Rule"
        isdraw = True
    elif board.can_claim_threefold_repetition():
        message = "Threefold Repetition"
        isdraw = True

    return isdraw, message


def random_move(board):
    legal_moves = list(board.legal_moves)
    return random.choice(legal_moves)


def is_move_legal(board, move):
    return move in board.legal_moves


def initialize_board():
    board = chess.Board()
    board.set_fen(chess.STARTING_FEN)
    return board


st.title("Blind-chess chat-bot")

if "board" not in st.session_state:
    st.session_state.game_ended = False
    st.session_state.board = initialize_board()


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Start a new game"):
        st.session_state.board = initialize_board()
        st.session_state.messages = []
with col2:
    if st.button("Clear chat"):
        st.session_state.messages = []
with col3:
    st.session_state.show_chat = st.checkbox("Show chat history", value=True)

if st.checkbox("Show raw data"):
    st.write(st.session_state.board.fen())

if st.session_state.show_chat:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is your move?"):
    # TODO: get rid of this variable
    user_message = prompt
    st.chat_message("user").markdown(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})

    try:
        st.session_state.board.push_san(prompt)

        check_draw, draw_type = is_a_draw(st.session_state.board)
        if check_draw:
            response_message = f"Draw: {draw_type}"
            st.session_state.game_ended = True
        elif st.session_state.board.is_checkmate():
            response_message = "Game Over - You won!"
            st.session_state.egame_ended = True
        else:
            bot_move = random_move(st.session_state.board)
            response_message = st.session_state.board.san(bot_move)

            # board.push(bot_move)
            st.session_state.board.push_san(st.session_state.board.san(bot_move))

            check_draw, draw_type = is_a_draw(st.session_state.board)

            if check_draw:
                response_message += f"Draw: {draw_type}"
                st.session_state.game_ended = True
            elif st.session_state.board.is_checkmate():
                response_message += "Game Over - I won!"
                st.session_state.game_ended = True

        st.chat_message("assistant").markdown(response_message)
        st.session_state.messages.append(
            {"role": "assistant", "content": response_message}
        )

    except ValueError:
        error_response = "This is not a legal move."
        st.chat_message("assistant").markdown(error_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": error_response}
        )

    if st.session_state.game_ended:
        st.session_state.board.set_fen(chess.STARTING_FEN)
        st.session_state.game_ended = False
        new_game_message = "Lets start a new game :)"
        st.chat_message("assistant").markdown(new_game_message)
        st.session_state.messages.append(
            {"role": "assistant", "content": new_game_message}
        )
