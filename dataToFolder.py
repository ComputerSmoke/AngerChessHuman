f = open("./data.pgn", "r")
i = 0
while True:
    line = f.readline()
    if not line:
        break
    fo = open("./data/"+str(i)+".pgn", "w")
    fo.write(line)
    fo.close()
    i += 1
f.close()
    