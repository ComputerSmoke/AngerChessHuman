import chess
import chess.pgn
import numpy as np
import io

pieceIdx = {
    "r": 5,
    "p": 4,
    "b": 7,
    "q": 8,
    "n": 6,
    "k": 9
}

def pgn_to_fen(line):
    moves = line.split(" ")
    outcome = moves[-1].replace("\n","")
    if outcome == "0-1":
        outcome = 0
    elif outcome == "1-0":
        outcome = 1
    elif outcome == "1/2-1/2":
        outcome = -1
    else:
        return
    moves = moves[:-1]
    moveMod = []
    for move in moves:
        if not '.' in move:
            moveMod.append(move)
    moves = moveMod

    pgnstr = ""
    for k in range(len(moves)):
        if k%2 == 0:
            pgnstr += str(int(k/2)+1) + "." 
        pgnstr += moves[k] + " "
    pgnio = io.StringIO(pgnstr)
    game = chess.pgn.read_game(pgnio)
    board = game.board()
    fens = [board.fen()]
    for move in game.mainline_moves():
        board.push(move)
        fens.append(board.fen())


    outcomes = [outcome for i in range(len(fens))]
    return fens, outcomes

def fen_to_bitmap(fen):
    bitmap = np.array([np.array([np.array([0 for k in range(12)]) for j in range(8)]) for i in range(8)])
    fen = fen.split(" ")
    playChar = fen[1]
    if playChar == 'w':
        play = 1
    else:
        play = 0
    fen = fen[0].split("/")
    for i,row in enumerate(fen):
        idx = 0
        rIdx = 0
        while idx < 8:
            c = "" + row[rIdx]
            if c.isnumeric():
                for j in range(int(c)):
                    bitmap[i][idx+j][0] = 1
                idx += int(c)
                rIdx += 1
                continue
            if c.isupper():
                bitmap[i][idx][2] = 1
            else:
                bitmap[i][idx][1] = 1
            c = c.lower()
            bitmap[i][idx][pieceIdx[c]] = 1
            idx += 1
            rIdx += 1
    return bitmap, play

def pgn_to_data(pgn):
    bitmaps = []
    turns = []
    fens,outcomes = pgn_to_fen(pgn)
    for fen in fens:
        bitmap,turn = fen_to_bitmap(fen)
        bitmaps.append(bitmap)
        turns.append(turn)
    return bitmaps, turns, outcomes

def get_data(startIdx, amt):
    f = open("./data.pgn", "r")
    for i in range(startIdx):
        f.readline()
    bitmaps = []
    outcomes = []
    turns = []
    i = 0
    skips = 0
    while i < amt:
        try:
            pgn = f.readline()
            bitmap,turn,outcome = pgn_to_data(pgn)
            for j in bitmap:
                bitmaps.append(j)
            for j in turn:
                turns.append(j)
            for j in outcome:
                outcomes.append(j)
            if(i%10==0): print("Loaded pgn " + str(i) + " / " + str(amt) + "\t" + str(i*100/amt) + "% loaded")
            i += 1
        except:
            print("Failed to load a pgn, skipping.")
    labels = []
    for outcome in outcomes:
        if outcome == 1:
            labels.append([0, 1, 0])
        elif outcome == 0:
            labels.append([1, 0, 0])
        else:
            labels.append([0, 0, 1])

    return bitmaps, turns, labels, skips
    