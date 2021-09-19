from matplotlib import pyplot  as plt
import numpy as np
from hackathon import get_survey, get_answer_data, get_survey_title, get_question_data
import urllib.parse
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker

opt ='cockroachdb://nitahieb:bm7byD6rhy8ib779@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/bank?sslmode=verify-full&sslrootcert=root.crt&options=--cluster%3Dquaint-cougar-3476'
db_uri = urllib.parse.unquote(opt)
engine = create_engine(db_uri)
DBSession = sessionmaker(bind=engine)
DBsession = DBSession()

#def get_answer_data(session,survey_id):
answers = get_answer_data(session= DBsession, )
#def get_survey_title(session,survey_id):
title = get_survey_title(session = DBsession, )
#def get_question_data(session,survey_id):
questions = get_question_data(session= DBSession, )
#answerdict = {
#        "q1" : [0,0,0],
#        "q2" : [],
#        "q3" : [],
#        "q4" : [],
#        "q5" : [0,0,0,0,0,0,0,0,0,0]
#    }

questions = [questions['q1'][2][0],questions['q1'][2][1],questions['q1'][2][2]]
options = [answers['q1'][1], answers['q1'][2], answers['q1'][3]]

#questions = [122,178,91]
#options = ['option1', 'option2', 'option3']
#title = 'sometitle'

fig = plt.figure()

ypos = np.arange(len(options))

plt.xticks(ypos, options)

plt.bar(ypos, questions)

plt.show()

plt.savefig('/static/plot.png', bbox_inches='tight')
