f = open("./data_clean.pgn", "r")
fout = open("./data.pgn", "a")

while True:
    line = f.readline()
    if not line:
        break
    if line != "\n":
        fout.write(line)

