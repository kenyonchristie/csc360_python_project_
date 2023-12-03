import csv
import random

class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.incorrect_answers = []
        self.score = 0

#Present user with questions and corresponding answer prompts based on quiz type
    def question_user(self, questions):
        if quiz_type != 3:     
            print(questions['question'])
            print()
            user_answer = input("\nYour answer: ")
            if user_answer.lower() == questions['answer'].lower():
                print("\nCorrect!\n")
                self.score += 1
            else:
                self.incorrect_answers.append(questions['question'])
                print(f"\nI'm sorry, but that is incorrect. The correct answer is {questions['answer']}\n")
        else:
            print(questions['question'])
            print()
            for option in questions:
                option_list = []
                option_list.append(questions['answer'])
                option_list.append(questions['option1'])                
                option_list.append(questions['option2'])                
                option_list.append(questions['option3'])
                random.shuffle(option_list)
                answer_labels = [1, 2, 3, 4]
                answers = option_list
                option_dict = dict(zip(answer_labels, answers))
            for key, value in option_dict.items():
                print(key, ': ', value)
            user_answer = int(input("\nYour answer: "))
            final_answer = option_dict.get(user_answer)
            if final_answer == questions['answer']:
                print("\nCorrect!\n")
                self.score += 1
            else:
                self.incorrect_answers.append(questions['question'])
                print(f"\nI'm sorry, but that is incorrect. The correct answer is {questions['answer']}.\n")

#Function to execute the quiz program and generate a final grade plus summary of review items as applicable
    def execute_quiz(self):
        for question in self.questions:
            self.question_user(question)
            self.final_score = (self.score / len(self.questions) * 100) 
        print(f'You scored {int(self.final_score)}%.\n')
        if len(self.incorrect_answers) > 0:
            print(f'Based on your answers, you should review the following questions:\n')
            i = 0
            for item in self.incorrect_answers:
                print(f'\t\t{self.incorrect_answers[i]}')
                i+=1

#Function to create questions, answers, and multiple choice options from csv file
def extract_questions(filename):
    questions = [] #for storing the extracted questions and answers
    with open(filename, 'r') as file:
        filename_string = str(filename) #convert to string so can do split and check file type
        filename_tokens = filename_string.split('.') #create token for file type extentions
        file_type = filename_tokens[1] #store filetype in variable for if comparison that follows
        if file_type == 'csv' and quiz_type == 1:
            csv_reader = list(csv.DictReader(file))
            random.shuffle(csv_reader)
            for row in csv_reader:
                questions.append({
                    'question': row['QUESTION'],
                    'answer': row['ANSWER']
                })
        elif file_type == 'csv' and quiz_type == 2:
            csv_reader = list(csv.DictReader(file))
            random.shuffle(csv_reader)
            for row in csv_reader:
                questions.append({
                    'question': row['ANSWER'],
                    'answer': row['QUESTION']
                })
        elif file_type == 'csv' and quiz_type == 3:
            csv_reader = list(csv.DictReader(file))
            random.shuffle(csv_reader)
            for row in csv_reader:
                questions.append({
                    'question': row['QUESTION'],
                    'answer': row['CORRECT_ANSWER'],
                    'option1': row['OPTION1'],
                    'option2': row['OPTION2'],
                    'option3': row['OPTION3']
                })
        else:
            print('File type not supported')            
    return questions

#Main program: takes file name from user, prompts user selection of quiz type, 
#generates questions to send to the Quiz class for program execution
if __name__ == "__main__":
    quiz_filename = input('Enter quiz file: ')
    print('\nPlease select which type of quiz you would like to run?')
    quiz_type = int(input('\nEnter 1 for Question & Answer, 2 for Jeopardy-style, or 3 for Multiple Choice: '))
    quiz_questions = extract_questions(quiz_filename)
    quiz = Quiz(quiz_questions)
    print()
    quiz.execute_quiz()
