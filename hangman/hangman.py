# hangman.py

from hangman_arts import display_hangman
from display_word import display_word
from word_list import choose_word

def hangman():
    secret_word = choose_word()
    guessed_letters = []
    attempts = 6

    print("Welcome to Hangman!")

    while True:
        print("\nCurrent word:", display_word(secret_word, guessed_letters))
        print(display_hangman(attempts))
        guess = input("Guess a letter: ").lower()

        if guess in guessed_letters:
            print("You already guessed that letter. Try again.")
            continue

        guessed_letters.append(guess)

        if guess not in secret_word:
            attempts -= 1
            print("Incorrect guess. Attempts left:", attempts)
            if attempts == 0:
                print("Sorry, you're out of attempts. The word was:", secret_word)
                break
        else:
            print("Good guess!")

        if set(guessed_letters) >= set(secret_word):
            print("Congratulations! You guessed the word:", secret_word)
            break

if __name__ == "__main__":
    hangman()
