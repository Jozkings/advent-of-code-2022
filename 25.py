FILE_NAME = 'input25.in'

TO_DECIMAL = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
TO_SNAFU = {0: '0', 1: '1', 2: '2', 4: '-', 3: '='}
sumo = 0


def to_decimal(snafu: str) -> int:
    res = 0
    for expo, charo in enumerate(snafu[::-1]):
        res += (5 ** expo) * TO_DECIMAL[charo]
    return res


def to_snafu(decimal: int) -> str:
    res = ""

    while decimal > 0:
        remain = (decimal + 5) % 5
        charo = TO_SNAFU[remain]
        res += charo
        if not charo.isdigit():
            decimal += 2
        decimal //= 5

    return res[::-1]


with open(FILE_NAME, 'r') as file:
    for line in file:
        value = line.strip()
        sumo += to_decimal(value)

print(to_snafu(sumo))
