"""
4x4 Chess
---------
White (UPPERCASE) starts at the bottom, Black (lowercase) at the top.

    4 r n b k
    3 p p p p
    2 P P P P
    1 R N B K
      a b c d

Pieces: K king, Q queen, R rook, B bishop, N knight, P pawn
Rules:  - Standard piece movement, no castling / en passant / double pawn step
        - A pawn reaching the far rank becomes a queen
        - No check or checkmate: capture the enemy king to win
Moves:  type the from-square and to-square, e.g.  b1a3   (or "b1 a3")
        type "quit" to leave
"""


def path_clear(board, fr, fc, tr, tc):
    """True if every square strictly between (fr,fc) and (tr,tc) is empty.
    Only used for straight/diagonal lines. On a 4x4 board that is at most 2 squares."""
    dr = tr - fr
    dc = tc - fc

    if dr > 0:
        sr = 1
    elif dr < 0:
        sr = -1
    else:
        sr = 0

    if dc > 0:
        sc = 1
    elif dc < 0:
        sc = -1
    else:
        sc = 0

    if abs(dr) > abs(dc):
        steps = abs(dr)
    else:
        steps = abs(dc)

    if steps == 1:
        return True

    # first square in between
    r1 = fr + sr
    c1 = fc + sc
    if board[r1][c1] != ".":
        return False
    if steps == 2:
        return True

    # second square in between (steps == 3)
    r2 = r1 + sr
    c2 = c1 + sc
    if board[r2][c2] != ".":
        return False
    return True


def is_legal(board, fr, fc, tr, tc, white_turn):
    piece = board[fr][fc]
    target = board[tr][tc]

    # must move one of your own pieces
    if piece == ".":
        return False
    if white_turn and not piece.isupper():
        return False
    if not white_turn and not piece.islower():
        return False

    # must actually move
    if fr == tr and fc == tc:
        return False

    # cannot capture your own piece
    if white_turn and target.isupper():
        return False
    if not white_turn and target.islower():
        return False

    dr = tr - fr
    dc = tc - fc
    adr = abs(dr)
    adc = abs(dc)
    kind = piece.lower()

    if kind == "k":
        if adr <= 1 and adc <= 1:
            return True
        return False

    if kind == "n":
        if adr == 2 and adc == 1:
            return True
        if adr == 1 and adc == 2:
            return True
        return False

    if kind == "r":
        if dr != 0 and dc != 0:
            return False
        return path_clear(board, fr, fc, tr, tc)

    if kind == "b":
        if adr != adc:
            return False
        return path_clear(board, fr, fc, tr, tc)

    if kind == "q":
        if dr != 0 and dc != 0 and adr != adc:
            return False
        return path_clear(board, fr, fc, tr, tc)

    if kind == "p":
        if white_turn:
            forward = -1  # white moves up the screen (toward row 0)
        else:
            forward = 1
        # straight step: only onto an empty square
        if dc == 0:
            if dr == forward and target == ".":
                return True
            return False
        # diagonal step: only when capturing
        if adc == 1 and dr == forward:
            if target != ".":
                return True
            return False
        return False

    return False


def show(board):
    print()
    print("4  " + " ".join(board[0]))
    print("3  " + " ".join(board[1]))
    print("2  " + " ".join(board[2]))
    print("1  " + " ".join(board[3]))
    print()
    print("   a b c d")
    print()


def main():
    board = [
        list("rnbk"),
        list("pppp"),
        list("PPPP"),
        list("RNBK"),
    ]
    white_turn = True

    print(__doc__)

    while True:
        show(board)

        if white_turn:
            name = "White"
        else:
            name = "Black"

        text = input(name + " to move: ").strip().lower().replace(" ", "")

        if text == "quit":
            print("Game ended.")
            break

        # --- parse the input -------------------------------------------------
        if len(text) != 4:
            print("Enter a move like b1a3.")
            continue
        if text[0] not in "abcd" or text[2] not in "abcd":
            print("Files must be a-d.")
            continue
        if text[1] not in "1234" or text[3] not in "1234":
            print("Ranks must be 1-4.")
            continue

        fc = ord(text[0]) - ord("a")
        fr = 4 - int(text[1])
        tc = ord(text[2]) - ord("a")
        tr = 4 - int(text[3])

        # --- validate --------------------------------------------------------
        if not is_legal(board, fr, fc, tr, tc, white_turn):
            print("Illegal move, try again.")
            continue

        # --- make the move ---------------------------------------------------
        piece = board[fr][fc]
        captured = board[tr][tc]
        board[tr][tc] = piece
        board[fr][fc] = "."

        # promotion
        if piece == "P" and tr == 0:
            board[tr][tc] = "Q"
            print("White pawn promotes to a queen!")
        if piece == "p" and tr == 3:
            board[tr][tc] = "q"
            print("Black pawn promotes to a queen!")

        # --- win check -------------------------------------------------------
        if captured.lower() == "k":
            show(board)
            print(name + " captured the king and wins!")
            break

        # --- next player -----------------------------------------------------
        if white_turn:
            white_turn = False
        else:
            white_turn = True


main()
