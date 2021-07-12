import enquiries
import colorama
class Bank:
    def greeting(self):
        options = ['Create an account', 'Log into account', 'Exit']
        choice = enquiries.choose('Welcome to the banking system! Choose one of these options:', options)
        if choice == 'Create an account':
            print(colorama.Fore.GREEN + "Account has been created!")

if __name__ == "__main__":
    start_sys = Bank()
    start_sys.greeting()
