import random as rd

res = list()
for _ in range(100):
    res.append(rd.choice([0,1]))

with open("buf.txt", "w") as fd:
    fd.write(str(res))
