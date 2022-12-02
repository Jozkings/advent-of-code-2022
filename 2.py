FILE_NAME = 'input2.in'

WIN_REWARD = 6
DRAW_REWARD = 3
DEFEAT_REWARD = 0
ROCK_REWARD = 1
PAPER_REWARD = 2
SCISSORS_REWARD = 3

rules1 = {"AY": WIN_REWARD + PAPER_REWARD, "BZ": WIN_REWARD + SCISSORS_REWARD, "CX": WIN_REWARD + ROCK_REWARD,
          "AX": DRAW_REWARD + ROCK_REWARD, "BY": DRAW_REWARD + PAPER_REWARD, "CZ": DRAW_REWARD + SCISSORS_REWARD,
          "AZ": DEFEAT_REWARD + SCISSORS_REWARD, "BX": DEFEAT_REWARD + ROCK_REWARD, "CY": DEFEAT_REWARD + PAPER_REWARD}

rules2 = {"AY": DRAW_REWARD + ROCK_REWARD, "BZ": WIN_REWARD + SCISSORS_REWARD, "CX": DEFEAT_REWARD + PAPER_REWARD,
          "AX": DEFEAT_REWARD + SCISSORS_REWARD, "BY": DRAW_REWARD + PAPER_REWARD, "CZ": WIN_REWARD + ROCK_REWARD,
          "AZ": WIN_REWARD + PAPER_REWARD, "BX": DEFEAT_REWARD + ROCK_REWARD, "CY": DRAW_REWARD + SCISSORS_REWARD}

with open(FILE_NAME, 'r') as file:
    manual = [''.join(line.strip().split(" ")) for line in file]

res1 = sum(map(lambda instruction: rules1[instruction], manual))
res2 = sum(map(lambda instruction: rules2[instruction], manual))

print(res1, res2)
