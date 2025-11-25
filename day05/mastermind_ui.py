from mastermind_logic import MasterMindGame

EXACT_MATCH_SYMBOL = "+"
WRONG_POSITION_SYMBOL = "~"
NO_MATCH_SYMBOL = "-"


def print_welcome_message():
    print("=" * 50)
    print("Welcome to Master Mind!")
    print("=" * 50)
    print("\nI'm thinking of a 4-digit number.")
    print("\nRules:")
    print(f"- '{EXACT_MATCH_SYMBOL}' means correct digit in correct position")
    print(f"- '{WRONG_POSITION_SYMBOL}' means correct digit in wrong position")
    print("\nTry to guess the number!\n")


def create_feedback(exact: int, wrong_pos: int) -> str:
    feedback = EXACT_MATCH_SYMBOL * exact + WRONG_POSITION_SYMBOL * wrong_pos
    return feedback if feedback else NO_MATCH_SYMBOL


def print_history(history: list[tuple[str, str]]):
    print("-" * 30)
    for guess, feedback in history:
        print(f"{guess}    {feedback}")
    print("-" * 30)


def print_win_message(game: MasterMindGame):
    print(f"\n🎉 You won! The number was {game.secret}")
    print(f"You guessed it in {game.attempts} attempts!\n")


def play_game():
    """Play a single game of Master Mind."""
    game = MasterMindGame()
    history = []

    print_welcome_message()

    while True:
        print(f"Attempt #{game.attempts + 1}")
        guess = input("Enter your guess (4 digits): ").strip()

        if not game.validate_guess(guess):
            print("Invalid! Please enter exactly 4 digits.\n")
            continue

        exact, wrong_pos, won = game.make_guess(guess)
        feedback = create_feedback(exact, wrong_pos)
        history.append((guess, feedback))

        print_history(history)

        if won:
            print_win_message(game)
            break


def main():
    while True:
        play_game()

        response = input("Play again? (y/n): ").strip().lower()
        if response not in ["y", "yes"]:
            print("\nThanks for playing!")
            break

        print("\n" + "=" * 50)
        print("Starting new game...")
        print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
