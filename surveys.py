from models import Survey, Account
import json



def create_question_dict():
    questiondict = {
        "q1" : [2,"   ", ["option1","option2","option3"]],
        "q2" : [1, "   "],
        "q3" : [1, "   "],
        "q4" : [0, "    "],
        "q5" : [3, "    "]
    }
    return questiondict

def create_answer_dict():
    answerdict = {
        "q1" : [0,0,0],
        "q2" : [],
        "q3" : [],
        "q4" : [],
        "q5" : [0,0,0,0,0,0,0,0,0,0]
    }
    return answerdict

def dict_to_json(dict):
    return json.dumps(dict)

b = create_question_dict()
b['q1'][1] = "5+5"
b['q1'][2][0] = "5"
b['q1'][2][1] = "6"
b['q1'][2][2] = "8"
b['q2'][1] = "Why is sky blue"
b['q3'][1] = "Why is sun red"
b['q4'][1] = "prove 1+1 = 10 in base 2"
b['q5'][1] = "how good was this quiz?"


b = create_question_dict()
b['q1'][1] = "when you look at the grass what colour is it?"
b['q1'][2][0] = "red"
b['q1'][2][1] = "green"
b['q1'][2][2] = "blue"
b['q2'][1] = "do you think your colour blind"
b['q3'][1] = "have you ever taken a colour blind"
b['q4'][1] = "please provide examples on how you belive your colour blind"
b['q5'][1] = "how bad do you think your colour blindness is "

b = create_question_dict()
b['q1'][1] = "which diet do you consider your self to be in"
b['q1'][2][0] = "vegan"
b['q1'][2][1] = "vegiterian"
b['q1'][2][2] = "no diet"
b['q2'][1] = "do you belive your fit?"
b['q3'][1] = "do you go to the gym or something else"
b['q4'][1] = "how can you improvre?"
b['q5'][1] = "on the level of one to ten how fit do you think you are"

c = create_answer_dict()
c[0] = 0
c[1] = "because of reflection or something"
c[2] = "If not what would be the point of superman?"
c[3] = "1 in binary is 1 and 2 in binary is 10 so 1+1 = 10"
c[4] = 4

print(b)




# eg  Question(0,)
class Question:
    def __init__(self,type,text,options):
        self.type = type #type 0(long answer), 1(shortanswer), 2 (multiple choice), 3 (ratings)
        self.text = text
        self.options = options