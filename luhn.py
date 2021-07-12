from functools import reduce


def luhn_checksum(card_number):

    def digits_of(n):
        return [int(d) for d in str(n)]

    digits = digits_of(card_number)
    odd_digits = digits[0::2]
    even_digits = digits[1::2]

    odd_new_digits = [i * 2 for i in odd_digits]
    a = [i - 9 for i in odd_new_digits if i > 9]

    for i in odd_new_digits[:]:
        if i > 9:
            odd_new_digits.remove(i)
    sum_list = even_digits + odd_new_digits + a
    checksum = 0
    for i in sum_list:
        checksum += i
    for i in range(10):
        if (checksum + i) % 10 == 0:
            return i


def luhn_valid(code):
    LOOKUP = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)
    code = reduce(str.__add__, filter(str.isdigit, code))
    evens = sum(int(i) for i in code[-1::-2])
    odds = sum(LOOKUP[int(i)] for i in code[-2::-2])

    return (evens + odds) % 10 == 0
