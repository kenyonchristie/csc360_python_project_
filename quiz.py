import csv
import random

class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.incorrect_answers = []
        self.score = 0

    def question_user(self, question):
        if quiz_type != 3:
            print(question['question'])
            user_answer = input("Your answer: ")
            if user_answer.lower() == question['answer'].lower():
                print("Correct!\n")
                self.score += 1
            else:
                self.incorrect_answers.append(question['question'])
                print(f"I'm sorry, but that is incorrect. The correct answer is {question['answer']}\n")
        else:
            print(question['question'])
            for option in question:
                option_list = []
                option_list.append(question['answer'])
                option_list.append(question['option1'])                
                option_list.append(question['option2'])                
                option_list.append(question['option3'])
                random.shuffle(option_list)
                answer_labels = [1, 2, 3, 4]
                answers = option_list
                option_dict = dict(zip(answer_labels, answers))
            for key, value in option_dict.items():
                print(key, ': ', value)
            user_answer = int(input("Your answer: "))
            final_answer = option_dict.get(user_answer)
            if final_answer == question['answer']:
                print("Correct!\n")
                self.score += 1
            else:
                self.incorrect_answers.append(question['question'])
                print(f"I'm sorry, but that is incorrect. The correct answer is {question['answer']}.\n")

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

def extract_questions(filename):
    questions = []

    with open(filename, 'r') as file:
        filename_string = str(filename)
        filename_tokens = filename_string.split('.')  
        file_type = filename_tokens[1]
        if file_type == 'csv' and quiz_type == 1:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                questions.append({
                    'question': row['QUESTION'],
                    'answer': row['ANSWER']
                })
        elif file_type == 'csv' and quiz_type == 2:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                questions.append({
                    'question': row['ANSWER'],
                    'answer': row['QUESTION']
                })
        elif file_type == 'csv' and quiz_type == 3:
            csv_reader = csv.DictReader(file)
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

if __name__ == "__main__":
    quiz_filename = input('Enter quiz file: ')
    print('Please select which type of quiz you would like to run?')
    quiz_type = int(input('Enter 1 for question and answer, 2 for Jeopardy-style, or 3 for multiple choice: '))
    quiz_questions = extract_questions(quiz_filename)
    quiz = Quiz(quiz_questions)
    quiz.execute_quiz()
