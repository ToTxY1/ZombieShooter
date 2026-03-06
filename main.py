class user_input:
    def get_guess(self):
        return input("Enter your guess: ")
    def guess_validation(self, guess):
        if len(guess) != 4:
            print("Invalid guess. Please enter a 4-digit number.")
            return False
        if not guess.isdigit():
            print("Invalid guess. Please enter only digits.")
            return False
        return True
    def guess_splitter(self, guess):
        return list(map(int, str(guess)))
class randomization:
    def generate_number(self):
        import random
        self.number = random.randint(1000, 9999)
        code = list(map(int, str(self.number)))
        return code
class guess_checker:
    def check_guess(self, guess, number):
        for i in range(len(guess)):
            if guess[i] == number[i]:
                print("Correct digit in the correct position.")
            elif guess[i] in number:
                print("Correct digit in the wrong position.")
            else:
                print("Incorrect digit.")
    
def main():
    number = randomization().generate_number()
    guess = user_input().get_guess()
    while not user_input().guess_validation(guess):
        guess = user_input().get_guess()
    print(f"Your guess is: {guess}")
    guess = user_input().guess_splitter(guess)
    guess_checker().check_guess(guess, number)

