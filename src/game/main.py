from game import run_game

def main():
    while True:
        result = run_game()
        if result != 'retry':
            break

if __name__ == "__main__":
    main()