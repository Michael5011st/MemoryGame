import logging
from UploadAPI import *
from answersQuestion import *
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
round_counter = 0
win_counter = 0
User = "User"
currentQuestionList = questionList
currentAnswerList = answerList
@ask.launch
def new_game():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("NoIntent")
def quit_game():
    UploadAPI(User, win_counter, 12/12/12)
    return statement("You answered "
                     + str(win_counter) + "out of "
                     + str(round_counter)
                     + "questions correct. ")


@ask.intent("YesIntent")
def vocalizeQuestion():
    global round_counter
    return question(questionList[round_counter])

@ask.intent("AnswerIntent",convert={'Answer': str})
def second_answer(Answer):
    global round_counter
    global win_counter
    if round_counter > len(questionList):
        return statement("You answered "
                     + str(win_counter) + "out of "
                     + str(round_counter)
                     + "questions correct. ")
    if Answer == answerList[round_counter]:
        win_counter += 1
        round_counter += 1
        continueMessage = render_template('win')
        return question(continueMessage)
    else:
        round_counter += 1
        continueMessage = render_template('lose')
        return question(continueMessage)



@ask.intent("PassIntent")
def passQuestion():
    global round_counter
    round_counter += 1
    outputMessage = render_template('passMessage')
    return question(outputMessage)
if __name__ == '__main__':
    app.run(debug=True)
