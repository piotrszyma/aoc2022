import enum


class Player(enum.Enum):
    OWN = enum.auto()
    OPONENT = enum.auto()


class Symbol(enum.Enum):
    ROCK = enum.auto()
    PAPER = enum.auto()
    SCISSORS = enum.auto()


class Result(enum.Enum):
    WIN = enum.auto()
    LOSS = enum.auto()
    DRAW = enum.auto()


def parse_opponent(oponent_symbol: str):
    match oponent_symbol:
        case "A":
            return Symbol.ROCK
        case "B":
            return Symbol.PAPER
        case "C":
            return Symbol.SCISSORS

    raise ValueError(f"unexpected state {oponent_symbol=}")


def parse_own(own_symbol: str):
    match own_symbol:
        case "X":
            return Symbol.ROCK
        case "Y":
            return Symbol.PAPER
        case "Z":
            return Symbol.SCISSORS

    raise ValueError(f"unexpected state {own_symbol=}")


def result_points(result: Result) -> int:
    match result:
        case Result.WIN:
            return 6
        case Result.DRAW:
            return 3
        case Result.LOSS:
            return 0

    raise ValueError(f"unexpected state {result=}")


def symbol_points(symbol: Symbol) -> int:
    match symbol:
        case Symbol.ROCK:
            return 1
        case Symbol.PAPER:
            return 2
        case Symbol.SCISSORS:
            return 3

    raise ValueError(f"unexpected state {symbol=}")


def winner(own: Symbol, oponent: Symbol) -> Result:
    if own == oponent:
        return Result.DRAW

    if own == Symbol.PAPER:
        if oponent == Symbol.ROCK:
            return Result.WIN
        elif oponent == Symbol.SCISSORS:
            return Result.LOSS

    if own == Symbol.SCISSORS:
        if oponent == Symbol.ROCK:
            return Result.LOSS
        elif oponent == Symbol.PAPER:
            return Result.WIN

    if own == Symbol.ROCK:
        if oponent == Symbol.SCISSORS:
            return Result.WIN
        elif oponent == Symbol.PAPER:
            return Result.LOSS

    raise ValueError(f"unexpected state {own=}, {oponent=}")


def own_move(oponent: Symbol, expected_result: Result) -> Symbol:
    for possibly_own in Symbol:
        res = winner(possibly_own, oponent)
        if res == expected_result:
            return possibly_own
    raise ValueError(f"unexpected state {expected_result=}, {oponent=}")


def parse_expected_result(raw: str) -> Result:
    match raw:
        case "X":
            return Result.LOSS
        case "Y":
            return Result.DRAW
        case "Z":
            return Result.WIN

    raise ValueError(f"unexpected state {strategy=}, {oponent=}")


with open("day2.input.txt", "r") as f:
    total_score = 0

    for line in f:
        line = line.strip()
        oponent, strategy = line.split(" ")

        expected_result = parse_expected_result(strategy)
        oponent = parse_opponent(oponent)

        own = own_move(oponent, expected_result)

        result = expected_result

        total_score += symbol_points(own) + result_points(result)

print(total_score)
