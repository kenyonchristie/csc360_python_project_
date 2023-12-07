import csv
import random
import sys
import tkinter as tk
from tkinter import messagebox

# Base class for running quiz through command line
class Quiz: 
    def __init__(self, questions, quiz_type):
        self.questions = questions
        self.incorrect_answers = []
        self.score = 0
        self.quiz_type = quiz_type

# Present user with questions and corresponding answer prompts based on quiz type
    def question_user(self, questions, quiz_type):
        if quiz_type != 3:     
            print(questions['question'])
            user_answer = exit_input("\nYour answer: ")
            user_answer = user_answer
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
            try:
                user_answer = exit_input("\nYour answer: ")
                if int(user_answer) not in [1, 2, 3, 4]:
                    raise ValueError
            except ValueError:
                print('Must select number from 1 - 4')
                user_answer = exit_input("\nYour answer: ")
            user_answer = int(user_answer)
            final_answer = option_dict.get(user_answer)
            if final_answer == questions['answer']:
                print("\nCorrect!\n")
                self.score += 1
            else:
                self.incorrect_answers.append(questions['question'])
                print(f"\nI'm sorry, but that is incorrect. The correct answer is {questions['answer']}.\n")

# Function to execute the quiz program and generate a final grade plus summary of review items as applicable
    def execute_quiz(self, quiz_type):
        for question in self.questions:
            self.question_user(question, quiz_type)
            self.final_score = (self.score / len(self.questions) * 100) 
        print(f'You scored {int(self.final_score)}%.\n')
        if len(self.incorrect_answers) > 0:
            print(f'Based on your answers, you should review the following questions:\n')
            i = 0
            for item in self.incorrect_answers:
                print(f'\t\t{self.incorrect_answers[i]}')
                i+=1

# GUI Quiz Class inheriting from the Quiz Class (base class)
class QuizGui(Quiz):
    def __init__(self, master, quiz_questions, quiz_type):
        super().__init__(quiz_questions, quiz_type)   
        self.master = master
        self.master.title("Escape from Quizlet")
        self.master.geometry('850x850')
        self.master.configure(bg='#15232E')
        
        font_selection = ('Century Gothic', 14) 
        question_font_color = '#15232E'
        answer_font_color = '#FFFFFF'
        background_color = '#15232E'

        self.q_index = 0

        self.question_frame = tk.Frame(self.master, bg=background_color)
        self.question_frame.pack(pady=10)

        self.label = tk.Label(self.master, text="Question", font=font_selection, fg=question_font_color)
        self.label.pack()

        if self.quiz_type == 3:
            self.user_answer = tk.IntVar()
            self.option_buttons = []
            for i in range(4):
                option_button = tk.Radiobutton(
                    self.master,
                    text="",
                    variable=self.user_answer,
                    value=i + 1,
                    command=self.validation,
                    font=font_selection,
                    fg=answer_font_color,                    
                    bg=background_color
                )
                option_button.pack()
                self.option_buttons.append(option_button)
        else:
            self.answer_frame = tk.Frame(self.master, bg=background_color)
            self.answer_frame.pack(pady=10)
            self.user_answer = tk.Entry(self.master, width=50, font=font_selection)
            self.user_answer.pack()
            self.submit_button = tk.Button(self.master, text="Submit", command=self.validation, font=font_selection)
            self.submit_button.pack(padx=0, pady=15)

        self.output_question()

    def output_question(self):
        if self.q_index < len(self.questions):
            question = self.questions[self.q_index]['question']
            self.label.config(text=question)
            if self.quiz_type == 3:
                options = [
                    self.questions[self.q_index]['answer'],
                    self.questions[self.q_index]['option1'],
                    self.questions[self.q_index]['option2'],
                    self.questions[self.q_index]['option3']
                ]
                random.shuffle(options)
                self.shuffled_options = options.copy() 
                for i in range(4):
                    self.option_buttons[i].config(text=self.shuffled_options[i])
        else:
            self.display_result()

    def validation(self):
        if self.quiz_type == 3:     
            correct_answer = self.questions[self.q_index]['answer']
            user_choice = self.shuffled_options[self.user_answer.get() - 1]

            if user_choice == correct_answer:
                self.score += 1
            else:
                self.incorrect_answers.append(self.questions[self.q_index]['question'])
        else:
            user_answer = self.user_answer.get().strip().lower()
            correct_answer = self.questions[self.q_index]['answer'].lower()
            if user_answer == correct_answer:
                self.score += 1
            else:
                self.incorrect_answers.append(self.questions[self.q_index]['question'])
        self.q_index += 1

        if isinstance(self.user_answer, tk.Entry):
            self.user_answer.delete(0, tk.END)
        self.output_question()

    def display_result(self):
        final_score = int(self.score / len(self.questions) * 100)
        messagebox.showinfo("Quiz Result", f'You scored {final_score}%.')
        if self.quiz_type == 3 and len(self.incorrect_answers) > 0:
            messagebox.showinfo("Review", "Based on your answers, you should review the following questions:")
            review_text = ""
            for answer in self.incorrect_answers:
                review_text += f"\n- {answer}"
            messagebox.showinfo("Incorrect Answers", review_text)
        elif len(self.incorrect_answers) > 0:
            messagebox.showinfo("Review", "Based on your answers, you should review the following questions:\n\n" + "\n".join(self.incorrect_answers))
        self.master.destroy()
        sys.exit()

# Function to create questions, answers, and multiple choice options from csv file
def extract_questions(filename, quiz_type):
    questions = [] #for storing the extracted questions and answers
    try:
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
                return questions    

            elif file_type == 'csv' and quiz_type == 2:
                csv_reader = list(csv.DictReader(file))
                random.shuffle(csv_reader)
                for row in csv_reader:
                    questions.append({
                        'question': row['ANSWER'],
                        'answer': row['QUESTION']
                    })
                return questions    

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
                return questions    
            
            else:
                raise ValueError
    except FileNotFoundError:
        print('File Not Found')
        return None
    except ValueError:
        print('\nMake sure you\'re loading a CSV file')
        return None

def exit_input(text):
    user_input = input(text)
    if user_input.lower() == 'quit':
        exit()
    else:
        return user_input
    
# Main program: takes file name from user, prompts user selection of quiz type, 
# generates questions to send to the Quiz class for program execution
if __name__ == "__main__":
    quiz_questions = None
    while quiz_questions == None: # loop to get user input 
        quiz_filename = exit_input('Enter quiz file: ')
        print('\nPlease select which type of quiz you would like to run?')
        try:
            quiz_type = exit_input('\nEnter 1 for Question & Answer, 2 for Jeopardy-style, or 3 for Multiple Choice: ')
            if int(quiz_type) not in [1,2,3]:
                raise ValueError
        except ValueError:
            print('Enter 1, 2, 3 or quit')
        else:
            quiz_questions = extract_questions(quiz_filename, int(quiz_type))
    
    try:
        gui_check = exit_input('\nWould you like to run this quiz in a GUI? (Y/N): ')
        if(gui_check.lower() not in ['y', 'n']):
            raise ValueError
    except ValueError:
        exit_input('Invalid selection. Please enter Y for Yes or N for No: ')
    else:
        if gui_check.lower() == 'n':
            quiz = Quiz(quiz_questions, int(quiz_type))
        else:
            root = tk.Tk()
            quiz = QuizGui(root, quiz_questions, int(quiz_type))
            root.mainloop()  
    print()
    quiz.execute_quiz(int(quiz_type))     
