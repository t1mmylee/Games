import subprocess
from colorama import init, Fore, Style

class color:
   BOLD = '\033[1m'
   END = '\033[0m'


def main():
    print(color.BOLD +"\nWelcome to the Game Launcher!" + color.END)
    print("\033[33mChoose a game to play:\033[0m")
    print("1. \033[36mTic Tac Toe\033[0m")
    print(color.BOLD + "2. \033[31mSpace Raid\033[0m" + color.END)

    choice = input("Enter the number of the game you want to play: ")

    if choice == '1':
        print("Launching Tic Tac Toe...")
        subprocess.run(['python', 'C:\\Users\\carlo\\OneDrive\\Desktop\\Carlo Games\\tictactoe\\tic.py'])
    elif choice == '2':
        print("Launching Space Raid...")
        subprocess.run(['python', 'C:\\Users\\carlo\\OneDrive\\Desktop\\\Carlo Games\\spaceship\\spaceship.py'])
    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()