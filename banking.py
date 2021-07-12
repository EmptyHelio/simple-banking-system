import sqlite3
import random

import luhn

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


class Banking:
    user_card_number = None
    user_card_pin = None
    check_sum = None
    banking_data = None
    id_in_system = 0

    def __init__(self):
        self.user_balance = 0

    def create_user(self):
        print("Your card has been created")
        print("Your card number")
        random.seed()
        Banking.user_card_number = "400000" + str(random.randint(100000000, 999999999))
        Banking.check_sum = str(luhn.luhn_checksum(Banking.user_card_number))
        Banking.user_card_number += Banking.check_sum
        print(Banking.user_card_number)
        print("Your card PIN:")
        Banking.user_card_pin = str(random.randint(1000, 9999))
        print(Banking.user_card_pin)

        data_entry(Banking.user_card_number, Banking.user_card_pin)

        print()
        main_screen()
        print()

    def login_usr(self):
        data_read()
        Banking.banking_data = cur.fetchall()
        print("Enter your card number")
        card = input(">")
        print("Enter your pin")
        pin = input(">")
        # cur.execute("UPDATE card SET balance=5;")
        # conn.commit()
        if (any(card in i for i in Banking.banking_data)) and (any(pin in i for i in Banking.banking_data)):
            print()
            cur.execute("SELECT id FROM card WHERE number =(?)", (card,))
            Banking.id_in_system = cur.fetchone()

            print("You have successfully logged in!")
            user_menu()
        else:
            print()
            print("Wrong card or PIN!")
            print()
            main_screen()

    def get_balance(self):
        cur.execute("SELECT balance FROM card WHERE id = (?)", (Banking.id_in_system))
        g = cur.fetchone()
        return g[0]

    def add_income(self):
        print("Enter income:")
        incom = int(input(">"))
        cur.execute("UPDATE card SET balance = balance + ? WHERE id=?", (incom, Banking.id_in_system[0]))
        conn.commit()
        user_menu()

    def do_transfer(self):
        cur.execute("SELECT number FROM card WHERE id = (?)", Banking.id_in_system)
        verification_numb = cur.fetchone()
        cur.execute("SELECT balance FROM card WHERE id = (?)", Banking.id_in_system)
        your_balance = cur.fetchone()

        print("Transfer \nEnter card number:")
        transf = input(">")

        # Verfication card
        if luhn.luhn_valid(transf):
            if any(transf in i for i in Banking.banking_data):
                if transf == verification_numb:
                    print("You can't transfer money to the same account!")
                else:
                    print("Enter how much money you want to transfer:")
                    money = int(input(">"))
                    if money > your_balance[0]:
                        print("Not enough money!")
                        user_menu()
                    else:
                        cur.execute("SELECT id FROM card WHERE number = (?)", (transf,))
                        id_transfer = cur.fetchone()
                        cur.execute("UPDATE card SET balance = balance + ? WHERE id = ?", (money, id_transfer[0]))
                        cur.execute("UPDATE card SET balance = balance - ? WHERE id = ?",
                                    (money, Banking.id_in_system[0]))
                        print("Success!")
                        conn.commit()
                        user_menu()
            else:
                print("Such a card does not exist.")
                user_menu()
        else:
            print("Probably you made a mistake in the card number. Please try again!")
            user_menu()

    def delete_account(self):
        cur.execute("DELETE FROM card WHERE id = ?", (Banking.id_in_system[0],))
        print("The account has been closed!")
        conn.commit()
        print()
        main_screen()


def user_menu():
    print("1. Balance")
    print("2. Add income")
    print("3. Do Transfer")
    print("4. Close account")
    print("5. Log Out")
    print("0. Exit")
    user_menu_select = int(input(">"))

    if user_menu_select == 1:
        print()
        user_money = Banking()
        print('Balance: {}'.format(user_money.get_balance()))
        print()
        user_menu()
    elif user_menu_select == 2:
        print()
        income = Banking()
        income.add_income()
        print()
    elif user_menu_select == 3:
        print()
        tranfer = Banking()
        tranfer.do_transfer()
    elif user_menu_select == 4:
        print()
        del_ac = Banking()
        del_ac.delete_account()
    elif user_menu_select == 5:
        print()
        print("You have successfully logged in!")
        print()
        main_screen()
    elif user_menu_select == 0:
        print("Bye!")
        conn.close()
        return 0


def main_screen():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    user_main_select = int(input(">"))

    if user_main_select == 1:
        print()
        create_us = Banking()
        create_us.create_user()
    elif user_main_select == 2:
        print()
        log_us = Banking()
        log_us.login_usr()
    elif user_main_select == 0:
        print()
        conn.close()
        print("Bye!")
        return 0


def create_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS card(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0);
    """)


def data_entry(bank_num, bank_pin):
    cur.execute("INSERT INTO card (number, pin) VALUES(?, ?)", (bank_num, bank_pin))
    conn.commit()


def data_read():
    cur.execute("SELECT number, pin FROM card;")


def get_balance():
    cur.execute("SELECT balance FROM card WHERE id = 1")
    g = cur.fetchone()
    return g[0]


create_table()
main_screen()
