# Master Mind Game

A simple implementation of the Master Mind board game in Python.

## How to Play

The computer thinks of a 4-digit number (duplicates allowed).
You try to guess it and receive feedback:

- `+` = correct digit in correct position
- `~` = correct digit in wrong position

Try to guess the number in as few attempts as possible!

## Example

```
Computer thinks: 5567 (hidden)

Your guess: 1234
Feedback: -        (Nothing match)

Your guess: 4589
Feedback: +        (5 is correct position)

Your guess: 5678
Feedback: +~~      (5 correct position, 6 and 7 wrong positions)
```

## Running the Game

```bash
python mastermind.py
```