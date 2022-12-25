# Day 25
from math import log
import math
import re

BASE = 5

def snafu_to_dec(snafu: str) -> int:
    value = 0
    for idx, digit in enumerate(snafu):
        pow = len(snafu) - idx - 1
        base = 5**pow
        if digit == '2':
            value += base * 2
        elif digit == '1':
            value += base * 1
        elif digit == '0':
            value += base * 0
        elif digit == '-':
            value += base * (-1)
        elif digit == '=':
            value += base * (-2)

    return value

def dec_to_snafu(dec: int) -> str:
    num = log(dec, BASE)
    top_power = math.ceil(num)

    snafu_digits = [2 for _ in range(top_power + 1)]

    res = -1

    for didx in reversed(range(len(snafu_digits))):
        for possible in [2, 1, 0, -1, -2]:
            new_digits = [*snafu_digits]
            new_digits[didx] = possible
            new_value = [(5 ** idx) * v for idx, v in enumerate(new_digits)]
            res = sum(new_value)
            if res == dec:
                snafu_digits = new_digits
                break

            if res < dec:
                break
            snafu_digits = new_digits


        if res == dec:
            break

    value = []

    for digit in reversed(snafu_digits):
        if digit == -1:
            value.append("-")
        elif digit == -2:
            value.append("=")
        else:
            value.append(str(digit))

    return "".join(value).lstrip('0')


def main():
    snafu_nums: list[str] = []
    with open("day25.input.txt", "r") as f:
        for line in f:
            num = line.strip()
            snafu_nums.append(num)

    nums_sum = 0
    for snafu_num in snafu_nums:
        dec_num = snafu_to_dec(snafu_num)
        nums_sum += dec_num

    nums_sum = sum(snafu_to_dec(s) for s in snafu_nums)

    assert snafu_to_dec(dec_to_snafu(nums_sum)) ==  nums_sum
    print(dec_to_snafu(nums_sum))


if __name__ == "__main__":
    asserts = (
        """
        1              1
        2              2
        3             1=
        4             1-
        5             10
        6             11
        7             12
        8             2=
        9             2-
       10             20
       15            1=0
       20            1-0
     2022         1=11-2
    12345        1-0---0
314159265  1121-1110-1=0
        """
    )

    assert dec_to_snafu(1) == "1"
    assert dec_to_snafu(314159265) == "1121-1110-1=0", dec_to_snafu(314159265)

    for line in asserts.split('\n'):
        stripped = line.strip()
        if not stripped:
            continue
        dec, snafu = re.split(r"[ ]+", stripped)
        dec = int(dec)
        assert snafu_to_dec(snafu) == dec
        assert dec_to_snafu(dec) == snafu, (dec, snafu)

    main()
