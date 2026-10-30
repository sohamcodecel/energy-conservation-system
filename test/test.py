"""
questions = ("How many elements are in the periodic table?: ",
             "Which animal lays the largest eggs?: ",
             "What is the most abundant gas in Earth's atmosphere?: ",
             "How many bones are in the human body?: ",
             "Which planet in the solar system is the hottest?: ")
 
options = (("A. 116", "B. 117", "C. 118", "D. 119"),
           ("A. Whale", "B. Crocodile", "C. Elephant", "D. Ostrich"),
           ("A. Nitrogen", "B. Oxygen", "C. Carbon-Dioxide", "D. Hydrogen"),
           ("A. 206", "B. 207", "C. 208", "D. 209"),
           ("A. Mercury", "B. Venus", "C. Earth", "D. Mars"))
 
answers = ("C", "D", "A", "A", "B")
guesses = []
score = 0
question_num = 0

for question in questions:
    print (question, end=" ")
    print ( )
    for option in options[question_num] :
        print (option)
    guesses.append ((input("Enter (A, B, C, or D): ")).upper())
    if guesses[question_num] == answers[question_num] :
        print ("CORRECT")
    else :
        print ("incorrect")
        print(f"correct answer is" ,answers[question_num])
        print ("--------------------------")
    question_num += 1
"""
import random
hangman_art = { 0 : "  a ", 
                1 : "  b ", 
                2 : "  c " , 
                3 : "  d " , 
                4 : "  e " , 
                5 : "  f "
}
words = ("xylophone", "giraffe", "computer", "python", "hangman")

def main():
    answer = random.choice(words)
    hint = ["_"]*len(answer)
    print(hint)

print (main())

if __name__ == "__main__":
    main()