
from argparse import ArgumentParser

import uuid
import urllib.parse
import json
from flask.globals import session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Account, Survey
from sqlalchemy.orm.attributes import flag_modified
from surveys import b,create_answer_dict,c
tags = json.loads('{"tags": ["lgbt","women","neurodivergent"]}')

surveys_completed = json.loads('{"surveys": []}')
# opt ='cockroachdb://nitahieb:@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/bank?sslmode=verify-full&sslrootcert=root.crt&options=--cluster%3Dquaint-cougar-3476'
# db_uri = urllib.parse.unquote(opt)
# engine = create_engine(db_uri)
# Session = sessionmaker(bind=engine)
# session = Session()

def create_account(session,email,username,completed_surveys,tags,birthdate,pass_hash):
    id = uuid.uuid4()
    id = str(id)
    account = Account(id=id,email=email,username=username,completed_surveys=completed_surveys,tags=tags,birthdate=birthdate,pass_hash=pass_hash)
    session.add(account)
    session.commit()


def create_survey(session,title,creator,completed_people,tags,questions,responses,description):
    id = uuid.uuid4()
    id = str(id)
    survey = Survey(id=id,title=title,creator=creator,completed_people=completed_people,tags=tags,questions=questions,responses=responses,description=description)
    session.add(survey)
    session.commit()

# def edit_tags_user(session,uuid,tags_add,tags_remove):
#     account = session.query(Account).filter(Account.id == uuid).first()
#     rest_tags = [i for i in account.tags if i not in tags_remove].extend(tags_add)
#     account.tags = rest_tags

def edit_tags_user(session,uuid,tags_add,tags_remove):
    account = session.query(Account).filter(Account.id == uuid).first()
    updated_tags = [i for i in account.tags['tags'] if i not in tags_remove]
    updated_tags.extend(tags_add)
    account.tags = updated_tags
    session.commit()

def edit_tags_survey(session,uuid,tags_add,tags_remove):
    survey = session.query(Survey).filter(Survey.id == uuid).first()
    updated_tags = [i for i in survey.tags['tags'] if i not in tags_remove]
    updated_tags.extend(tags_add)
    survey.tags = updated_tags
    session.commit()

def get_accounts(session):
    accounts = session.query(Account).all()
    return accounts

def get_surveys(session):
    Surveys = session.query(Survey).all()
    return Surveys

def get_survey(session, id):
    survey = session.query(Survey).filter(Survey.id == id).first()
    return survey

def get_account(session, id):
    survey = session.query(Account).filter(Account.id == id).first()
    return survey

def get_hash(session,username):
    account = session.query(Account).filter(Account.username == username).first()
    return account.pass_hash

def get_answer_data(session,survey_id):
    return session.query(Survey).filter(Survey.id == id).first().responses

def get_question_data(session,survey_id):
    return session.query(Survey).filter(Survey.id == id).first().questions

def get_survey_title(session,survey_id):
    return session.query(Survey).filter(Survey.id == id).first().title


def fill_in_survey_data(responses,new_responses):
    responses['q1'][new_responses[0]] +=1
    responses['q2'].append(new_responses[1])
    responses['q3'].append(new_responses[2])
    responses['q4'].append(new_responses[3])
    responses['q5'][new_responses[4]] +=1
    return responses

def submit_survey(session,user_uuid,survey_uuid,answers):
    survey = session.query(Survey).filter(Survey.id == survey_uuid).first()
    account = session.query(Account).filter(Account.id == user_uuid).first()
    account.completed_surveys["surveys"].append(survey_uuid)
    survey.completed_people.append(user_uuid)
    survey.responses = fill_in_survey_data(survey.responses,answers)
    flag_modified(account, "completed_surveys")
    flag_modified(survey, "completed_people")
    flag_modified(survey, "responses")
    session.commit()

def get_user(session,username):
    user = session.query(Account).filter(Account.username == username).first()
    return user

def get_title(session,title):
    return session.query(Survey).filter(Survey.title == title).first()


def user_exists(session,username):
    account = session.query(Account).filter(Account.username == username).first()
    if account:
        return True
    return False
