from typing import Tuple

FILE_NAME = 'input11.in'
part1 = False  #change to True for part 1


class Monkey:
    def __init__(self, items, operation, test, true_res, false_res):
        self.items = items
        self.operand = operation[0]
        self.operand_value = operation[1]
        self.test = test
        self.true_res = true_res
        self.false_res = false_res
        self.inspections = 0
        self.DIVISOR = None
        self.operators = {"+": lambda x, y: x+y, "*": lambda x, y: x*y}

    def do_job(self, item: int) -> Tuple[int, int]:
        return self.send_to_monkey(self.add_worry(item))

    def add_worry(self, item: int) -> int:
        if self.operand_value != "old":
            operand_value = int(self.operand_value)
        else:
            operand_value = item
        return self.operate(self.operand, item, operand_value)

    def operate(self, operand: str, value: int, many: int) -> int:
        return self.operators[operand](value, many)

    def send_to_monkey(self, item: int) -> Tuple[int, int]:
        new_item = int(item / 3.0) if self.DIVISOR is None else item % self.DIVISOR
        correct = new_item % self.test == 0
        return (self.true_res, new_item) if correct else (self.false_res, new_item)

    def add_item(self, value: int) -> None:
        self.items.append(value)

    def delete_items(self) -> None:
        self.items = []

    def set_divisor(self, divisor: int) -> None:
        self.DIVISOR = divisor


monkeys = []
divisors = 1
items = []

with open(FILE_NAME, 'r') as file:
    for line in file:
        value = line.strip().split(" ")
        if "Starting" in value:
            items = [int(numo) if numo[-1] != ',' else int(numo[:-1]) for numo in value[2:]]
        elif "Operation:" in value:
            operand, operand_value = value[-2:]
        elif "Test:" in value:
            divisible_test = int(value[-1])
        elif "If" in value:
            if "true:" in value:
                true_monkey = int(value[-1])
            else:
                false_monkey = int(value[-1])
                monkeys.append(Monkey(items, [operand, operand_value], divisible_test, true_monkey, false_monkey))
                divisors *= divisible_test

if not part1:
    for monkey in monkeys:
        monkey.set_divisor(divisors)

rounds = 0
MAX_ROUND = 20 if part1 else 10000

while rounds != MAX_ROUND:
    rounds += 1
    for monkey in monkeys:
        items = monkey.items
        monkey.delete_items()
        for item in items:
            res, new_item = monkey.do_job(item)
            monkeys[res].add_item(new_item)
        monkey.inspections += len(items)

inspections = sorted([monkey.inspections for monkey in monkeys], reverse=True)
print(inspections[0]*inspections[1])

