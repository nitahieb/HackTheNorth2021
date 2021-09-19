import os

from flask import Flask, flash, redirect, render_template, request, session
# from flask.scaffold import F
# from flask.templating import render_template_string
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash, safe_join
from hackathon import create_account, get_hash, get_user, user_exists, create_survey,submit_survey, get_account, get_answer_data,get_surveys, fill_in_survey_data
from helpers import login_required, apology
import json
import urllib.parse
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from surveys import create_answer_dict, create_question_dict


try:

    opt ='cockroachdb://nitahieb:@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/bank?sslmode=verify-full&sslrootcert=root.crt&options=--cluster%3Dquaint-cougar-3476'
    db_uri = urllib.parse.unquote(opt)
    engine = create_engine(db_uri)
    DBSession = sessionmaker(bind=engine)
    DBsession = DBSession()


    # Configure application
    app = Flask(__name__)

    # Ensure templates are auto-reloaded
    app.config["TEMPLATES_AUTO_RELOAD"] = True


    # Ensure responses aren't cached
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_FILE_DIR"] = mkdtemp()
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    @app.route("/")
    @login_required
    def home_page():
        return render_template("home_page.html")


    @app.route("/account_page")
    @login_required
    def account_page():
        return apology("TODO", 403)


    @app.route("/browsing_page")
    @login_required
    def browsing_page(): 
        if request.method == "POST":
            print("a")
        
        else:
            survey_list = get_surveys(DBsession)
            info_list = []
            for surveyind in range(6):
                info_list.append((survey_list[surveyind].title,survey_list[surveyind].description))
                #info_list.append(survey_list[surveyind].title)
            return render_template("browse.html", info_list=info_list)


    @app.route("/about_page")
    @login_required
    def about_page():
        return apology("TODO", 403)


    @app.route("/create_form", methods=["GET", "POST"])
    @login_required
    def create_form():
         
        if request.method == "POST":
            #title
            survey_title = request.form.get('enter_title')
            if not survey_title:
                return apology('enter title for survey', 400)

            #survey descripition
            survey_description = request.form.get('survey_description')
            if not survey_description:
                return apology('enter survey description', 400)
            #question for mutiple choice
            mutiple_choice_question = request.form.get("multiple_choice_question")
            if not mutiple_choice_question:
                return apology("enter a question for mutiple choice selection", 400)

            #naming raido buttons
            option1_name = request.form.get('radio_option_1')
            option2_name = request.form.get('radio_option_2')
            option3_name = request.form.get('radio_option_3')
            """ if not option1_name or not option2_name or not option3_name: 
                return apology('enter a value for mutiple choice options', 400) """
            #short answers
            short_question1 = request.form.get('short_answer_question_1')
            short_question2 = request.form.get('short_answer_question_2')
            if not short_question1 or not short_question2:
                return apology('enter question for short answers', 400)

            #long answers
            long_question = request.form.get('long_answer_question')
            if not long_question:
                return apology('enter question for long question', 400)

            #rating
            rating_question = request.form.get('rating_question')
            if not rating_question: 
                return apology('enter a rating question', 400)

            #tags = request.form.getlist('')
            tags = json.loads('{"tags": []}')
            if not tags:
                return apology('please provide tags for your survey', 400)

            #b['q1'][1] = "when you look at the grass what colour is it?"
            #b['q1'][2][0] = "red"
            #b['q1'][2][1] = "green"
            #b['q1'][2][2] = "blue"
            #b['q2'][1] = "do you think your colour blind"
            #b['q3'][1] = "have you ever taken a colour blind"
            #b['q4'][1] = "please provide examples on how you belive your colour blind"
            #b['q5'][1] = "how bad do you think your colour blindness is "
            question_data = create_question_dict()
            question_data['q1'][1] = mutiple_choice_question
            question_data['q1'][2][0] = option1_name
            question_data['q1'][2][1] = option2_name
            question_data['q1'][2][2] = option3_name
            question_data['q2'][1] = short_question1
            question_data['q3'][1] = short_question2
            question_data['q4'][1] = long_question
            question_data['q5'][1] = rating_question
            
            creator = get_account(DBsession,session["user_id"])
            #create_survey(session,title,creator,completed_people,tags,questions,responses):
            create_survey(DBsession,title = survey_title, creator = creator.username, completed_people= json.loads('{"completed_people": []}'),tags = tags, questions = question_data, responses = create_answer_dict(),description=survey_description)
            
            return redirect("/")
        else:
            return render_template("create_form.html")


    @app.route("/login", methods=["GET", "POST"])
    def login():
        # Forget any user_id
        session.clear()

        #POST Method
        if request.method == "POST":
            
            # Ensure username was submitted
            if not request.form.get("username"):
                return apology("must provide username", 400)
            
            # Ensure password was submitted
            if not request.form.get("password"):
                return apology("must provide password", 400)    
            
            # Check username
            check_user = user_exists(DBsession, request.form.get("username"))
            if check_user == False:
                return apology("invalid username", 400)
            
            # Check pasword
            gets_users = get_user(DBsession, request.form.get("username"))
            if not check_password_hash(gets_users.pass_hash, request.form.get("password")):
                return apology("invalid password", 400)
            
            # Remember user
            session["user_id"] = gets_users.id
            
            # Redirect user
            return redirect("/")

        else:
            return render_template("log_in.html")


    @app.route("/logout")
    def logout():
        # Forget any user_id
        session.clear()
        
        # Redirect user to login form
        return redirect("/")


    @app.route("/register", methods=["GET", "POST"])
    def register():
        # Forget any user_id
        session.clear()

        # POST Method
        if request.method == "POST":
            #username register
            username = request.form.get("username")
            if not request.form.get("username"):
                return apology('must provide a username', 400)
                
            #need more outputs here
            check = user_exists(DBsession, request.form.get("username"))
            if check:
                return apology("username already exists", 400)
            
            #email register
            email_address = request.form.get('email')
            if not request.form.get('email'):
                return apology("must provide E-mail address", 400)
            
            #password
            password = request.form.get('password')
            if not request.form.get('password'):
                return apology("must provide a password", 400)

            #password hashed
            pass_hash = generate_password_hash(password)
             
            # DOB
            month = request.form.get('month')
            day = request.form.get('day')
            year = request.form.get('year')
            if not request.form.get('month') or not request.form.get('day') or not request.form.get('year'):
                return apology("must provide a Date of birth", 400)
                
            #pronounce
            
            pronouns = request.form.getlist('pronouns')
            user_pronouns = ""
            for noun in pronouns:
                user_pronouns += noun+","

            if not request.form.getlist('pronouns'):
                return apology("must provide a pronoun", 400)
            #Ethnicity
            #American Indian, Asian, South Asian, Black or African American, Hispanic or Latino, Pacific Islander, White
            ethnicity = request.form.get('ethnicity')
            if not request.form.get('ethnicity'):
                return apology("must provide ethnicity", 400)
            #def create_account(session,email,username,completed_surveys,tags,birthdate,pass_hash):
            tags = json.loads('{"tags": []}')
            tags['tags'].extend(pronouns)
            tags['tags'].append(ethnicity)
            surveys = json.loads('{"surveys":[]}')


            create_account(DBsession, email = email_address, username = username,completed_surveys =  surveys, tags = tags,birthdate =  f'{day}-{month}-{year}', pass_hash = pass_hash)
            return redirect("/")
        else:
            return render_template("register.html")
           
    @app.route("/fill_form_1", methods=["GET", "POST"])
    @login_required
    def fill_form_1():

        if request.method == "POST":

            #raido options mutiple choice buttons
            options = request.form.getlist("radio_buttons")
            if not request.form.get("radio_buttons"):
                return apology('must select a option', 400)

            #short answes 1
            short_answers_1 = request.form.get('short_answer_1')
            if not request.form.get('short_answer_1'):
                return apology('must provide a answer for question 2', 400)

            #short answers 2
            short_answers_2 = request.form.get('short_answer_2')
            if not request.form.get('short_answer_2'):
                return apology('must provide a answer for question 3', 400)

            #long answes 1
            long_answers = request.form.get('long_answer_question')
            if not request.form.get('long_answer_question'):
                return apology('must provide a answer for question 4', 400)

            #rating answer
            rating_answer = request.form.getlist('rating_button')
            if not request.form.getlist('rating_button'):
                return apology('must provide a answer for question 5', 400)
            
            #connecting to database
            new_responses = [options, short_answers_1, short_answers_2, long_answers, rating_answer]
            
        else:
            return render_template("fill_form_1.html")
            
    def errorhandler(e):
        # Handle error 
        if not isinstance(e, HTTPException):
            e = InternalServerError()
        return apology(e.name, e.code)


    # Listen for errors
    for code in default_exceptions:
        app.errorhandler(code)(errorhandler)

except:
    session.rollback()
