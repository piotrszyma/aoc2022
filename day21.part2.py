from dataclasses import dataclass
import operator
from typing import Callable, Literal, TypeAlias, Union


VarName: TypeAlias = str


@dataclass
class CalcExpr:
    op: Callable[[int, int], int]
    vars: tuple[VarName, VarName]  # Name of arguments.
    kind: Literal["calc"] = "calc"


@dataclass
class ValueExpr:
    value: int
    kind: Literal["value"] = "value"


ExprTable = dict[VarName, Union[CalcExpr, ValueExpr]]


def calc(expr_table: ExprTable, variable: VarName) -> int:
    expr = expr_table.get(variable)
    if expr is None:
        raise ValueError(f"Unexpected variable {variable}")

    if expr.kind == "value":
        return expr.value

    arg0, arg1 = (calc(expr_table, variable) for variable in expr.vars)

    return expr.op(arg0, arg1)


def main():
    expr_table: dict[str, Union[CalcExpr, ValueExpr]] = {}

    with open("day21.input.txt", "r") as f:
        for line in f:
            target_variable, raw_expr = line.strip().split(": ")
            if raw_expr.isdigit():
                expr_table[target_variable] = ValueExpr(value=int(raw_expr))
                continue

            left, raw_op, right = raw_expr.split(" ")

            match raw_op:
                case "+":
                    op = operator.add
                case "-":
                    op = operator.sub
                case "*":
                    op = operator.mul
                case "/":
                    op = operator.truediv
                case _:
                    raise ValueError(f"Unexpected operator symbol {raw_op}")

            expr_table[target_variable] = CalcExpr(op, (left, right))

    print(calc(expr_table, "root"))


if __name__ == "__main__":
    main()
