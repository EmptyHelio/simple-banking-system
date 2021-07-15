import enquiries
import colorama
import random
import sys
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


class Bank:

    def __init__(self):
       self.user_balance = 0
       self.user_card_number = 0
       self.user_card_pin = 0
       self.user_luhn_checksum = 0

    def greeting(self):
        options = ['Create an account', 'Log into account', 'Exit']
        choice = enquiries.choose('', options)
        if choice == 'Create an account':
            self.create_user()
        elif choice == 'Log into account':
            print(colorama.Fore.GREEN + "You are successfully logged in")
        else:
            if enquiries.confirm('Do you really want to exit the program?'):
                self.exit_the_program()
            else:
                self.greeting()

    def create_user(self):
        random.seed()
        self.user_card_number = "400000" + str(random.randint(000000000, 999999999))
        self.user_luhn_checksum = self.luhn_create_chksum(self.user_card_number)
        self.user_card_number += str(self.user_luhn_checksum)
        self.user_card_pin = str(random.randint(0000, 9999))
        self.create_bank_table()
        self.data_entry()

        print(colorama.Fore.GREEN + "Account has been created!")
        print(colorama.Style.RESET_ALL + "Your card number : " + colorama.Fore.YELLOW + self.user_card_number)
        print(colorama.Style.RESET_ALL + "Your card pin    : " + colorama.Fore.YELLOW +self.user_card_pin + colorama.Style.RESET_ALL + '\n')


    def luhn_create_chksum(self, card_num):
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(card_num)
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


    def login_user(self):
        pass

    def create_bank_table(self):
        cur.execute("""CREATE TABLE IF NOT EXISTS card(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0);
        """)

    def data_entry(self):
        cur.execute("INSERT INTO card (number, pin) VALUES(?, ?)", (self.user_card_number, self.user_card_pin))
        conn.commit()

    def exit_the_program(self):
        print(colorama.Fore.RED + "Good Luck! Bye")
        cur.close()
        sys.exit()


if __name__ == "__main__":
    start_sys = Bank()
    print("Welcome to the banking system! Choose one of these options:")
    while True:
        start_sys.greeting()
