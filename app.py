import streamlit as st
import random
import time
import chess

game_ended = False


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


print("start")
board = chess.Board()
board.set_fen(chess.STARTING_FEN)


st.title("Simple blind-chess chat-bot")

if st.checkbox("Show raw data"):
    st.write(board.fen())
    # for row in str(board).split("\n"):
    #     st.write(row)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is your move?"):
    print(prompt)
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    pass_count = 0
    print(f"passed: {pass_count}")
    pass_count += 1

    try:
        print("trying")

        print()
        print(board)
        print()

        board.push_san(prompt)

        print("new board:")

        print()
        print(board)
        print()

        print(f"passed: {pass_count}")
        pass_count += 1

        with st.chat_message("assistant"):
            init_react = f"{prompt} you say? insteresting..."
            init_response = st.markdown(init_react)
            st.session_state.messages.append(
                {"role": "assistant", "content": init_response}
            )

            print(f"passed: {pass_count}")
            pass_count += 1

            check_draw, draw_type = is_a_draw(board)
            if check_draw:
                response_message = f"Draw: {draw_type}"
                game_ended = True
            elif board.is_checkmate():
                response_message = "Game Over - You won!"
                game_ended = True
            else:
                print(f"passed: {pass_count}")
                pass_count += 1

                bot_move = random_move(board)
                response_message = board.san(bot_move)

                print(bot_move)
                print(board.san(bot_move))

                print()
                print(board)
                print()

                print(f"passed: {pass_count}")
                pass_count += 1

                # board.push(bot_move)
                board.push_san(board.san(bot_move))

                print()
                print(board)
                print()

                check_draw, draw_type = is_a_draw(board)
                print("draw checked")
                print(f"{check_draw}")

                if check_draw:
                    end_message = f"Draw: {draw_type}"
                    game_ended = True
                elif board.is_checkmate():
                    end_message = "Game Over - I won!"
                    game_ended = True

            print(response_message)
            response = st.markdown(response_message)

    except ValueError:
        print("oops")
        with st.chat_message("assistant"):
            response = st.markdown("This is not a legal move.")
    print("finish line")

    print()
    print(board)
    print()

    st.session_state.messages.append({"role": "assistant", "content": response})

    if game_ended:
        print("ended")
        board.set_fen(chess.STARTING_FEN)
        game_ended = False

        with st.chat_message("assistant"):
            response = st.markdown("Lets start a new game :)")
            st.session_state.messages.append({"role": "assistant", "content": response})
