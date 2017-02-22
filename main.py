import logging
import datetime
from UploadAPI import *
from answersQuestion import *
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
currentQuestionList = questionList
currentAnswerList = answerList
counterDictionary = {'roundCounter': 0, 'winCounter': 0}
answerTag = ""
#need a python structure

def processState(userAnswer):
    global answerTag
    if round > len(questionList):
        message = quitQuiz()
        return message, 1
    if userAnswer[0] == 'Yes' and answerTag != 'continue':
        message = yesResponse()
        return message, 0
    if userAnswer[0] == 'No' and answerTag != 'continue':
        message = quitQuiz()
        return message, 1
    if userAnswer[0] == 'Pass' and answerTag != '':
        message = passResponse()
        return message,0
    else:
        message = answerResponse(userAnswer)
        return message, 0


def yesResponse():
    global answerTag
    answerTag = 'continue'
    message = nextQuestion()
    return message


def passResponse():
    global answerTag
    answerTag = ''
    message = passQuestion()
    return message

def answerResponse(userAnswer):
    global answerTag
    answerTag = ''
    message = checkAnswer(userAnswer)
    return message


def quitQuiz():
    user = "test_User_1"
    date = datetime.date
    UploadAPI(user, counterDictionary['winCounter'], date)
    return "The game is over. You answered "\
           + str(counterDictionary['roundCounter']) \
           + "out of "+ str(counterDictionary['winCounter'])\
           + "questions correct. "

def nextQuestion():
        round = counterDictionary['roundCounter']
        next_question = currentQuestionList[round]
        return next_question

def passQuestion():
    session.attributes["previous_question"]=""
    counterDictionary['roundCounter'] += 1
    output_message = render_template('passMessage')
    return output_message

def lose():
    counterDictionary['roundCounter'] += 1
    continue_message = render_template('lose')
    return continue_message

def win():
    counterDictionary['winCounter'] += 1
    counterDictionary['roundCounter'] += 1
    continue_message = render_template('win')
    return continue_message

def checkAnswerContent(userAnswer, correctAnswer):
    statusCode = 400
    for index in userAnswer:
        if(userAnswer[index] == correctAnswer[index]):
            statusCode = 200
        else:
            statusCode = 400
    return statusCode

def checkAnswer(userAnswer):
    round = counterDictionary['roundCounter']
    correctAnswer = currentAnswerList[round].split()
    if len(userAnswer) < len(correctAnswer) or len(userAnswer) < len(correctAnswer):
        message = lose()
        return message
    else:
        answerStatus = checkAnswerContent(userAnswer, correctAnswer)
        if answerStatus == 200:
            message = win()
            return message
        if answerStatus == 400:
            message = lose()
            return message


@ask.launch
def new_game():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("AnswerIntent", convert={'Answer': str})
def mainIntent(Answer):
    userAnswer = Answer.split()
    newMessage, end = processState(userAnswer)
    if end == 0:
        return question(newMessage)
    else:
        return statement(newMessage)

if __name__ == '__main__':
    app.run(debug=True)











def lose():
    counterDictionary['roundCounter'] += 1
    continue_message = render_template('lose')
    return continue_message

def win():
    counterDictionary['winCounter'] += 1
    counterDictionary['roundCounter'] += 1
    continue_message = render_template('win')
    return continue_message

def checkAnswerContent(userAnswer, correctAnswer):
    for index in userAnswer:
        if(userAnswer[index] == correctAnswer[index]):
            statusCode = 200
        else:
            statusCode = 400
    return statusCode

def checkAnswer(userAnswer):
    round = counterDictionary['roundCounter']
    correctAnswer = currentAnswerList[round].split()
    if len(userAnswer) < len(correctAnswer) or len(userAnswer) < len(correctAnswer):
        message = lose()
        return message
    else:
        answerStatus = checkAnswerContent(userAnswer, correctAnswer)
        if answerStatus == 200:
            message = win()
            return message
        if answerStatus == 400:
            message = lose()
            return message



