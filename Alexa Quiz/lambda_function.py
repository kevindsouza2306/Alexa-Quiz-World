"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
from botocore.vendored import requests
import json
import random


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome to Quiz World"
    
    speech_output = "Welcome to Quiz World. " 
    
    speech_output += "Please select a quiz category. "\
                    "for example General Knowledge Category. "
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please select a quiz category. " 
    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_level_upgraded(intent,session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "LevelUP"
    
    
    
    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    
    
    if session.get('attributes', {}) and ("level" in session.get('attributes', {})):
        level = session['attributes']['level']
        session_attributes = create_level_json(level)
        
        print("Inside if of session Check"+str(session))
        
    if level ==0:
        level_in_words = "amateur"
            
    elif level==1:
        level_in_words = "intermediate"
        
    else:
        level_in_words = "professional"      
    
    
    speech_output = "Asking Questions from "+level_in_words+" level. "\
                    "Please select your category. "
    
    
    
    reprompt_text = "Please select a quiz category. " 
    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))





def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Quiz World " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_question_json_attributes(question,questionNo, answer, score, answer_option,level):
    print("question = "+str(question) +" questionNo = "+str(questionNo) +" answer = "+str(answer) + " score = "+str(score)+" level = "+str(level))
    return {"questionJson": question, "questionNo":questionNo, "answer":answer, "score":score, "answer_option":answer_option, "level":level}

def create_answer_attributes(answer):
    return {"answer": answer}


def create_level_json(level):
    return {"level": level}

def category_selected(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = "Category Selected"
    session_attributes = {}
    should_end_session = False
    
    

    if 'Category' in intent['slots']:
        """favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"""
        category_found = True
        favorite_category = ""
        try:
            favorite_category = intent['slots']['Category']['value'] 
        except Exception, e:
            category_found = False                
        
        speech_output = "Your category is "+favorite_category
        print("favorite_category"+favorite_category)
       
        noQues = 5
        
        
        print("Session is ::"+str(session))
        if session.get('attributes', {}) and ("level"  in session.get('attributes', {})):
            
            level = session['attributes']['level'] 
            print("in if of level session")
                
        else:
            print("in else of level session ")
            level = 0
        
        print('level is in question : '+str(level))
                
        if level ==0:
            fixed_URL="&difficulty=easy"
            
        elif level==1:
            fixed_URL="&difficulty=medium"
        else:
            fixed_URL="&difficulty=hard"
        
        
        
        #fixed_URL = ""
        if favorite_category is None:
            category_found = False
            
        elif favorite_category in ('any','Any',' any '):
           
            url = "https://opentdb.com/api.php?amount="+str(noQues)+fixed_URL
            
        elif favorite_category in ('General Knowledge','G K','general knowledge', 'general',' knowledge'):
            
            url = "https://opentdb.com/api.php?amount="+str(noQues)+"&category=9"+fixed_URL
            
            
        elif favorite_category in ('books','Books','entertainment books', 'novels',' story books'):
            
            url = "https://opentdb.com/api.php?amount="+str(noQues)+"&category=10"+fixed_URL
                
        elif favorite_category in ('films','film','movies', 'movie','entertainment movies'):
            
            url = "https://opentdb.com/api.php?amount="+str(noQues)+"&category=11"+fixed_URL
                
        elif favorite_category in ('music','songs','song', 'musics','entertainment music'):
            
            url = "https://opentdb.com/api.php?amount="+str(noQues)+"&category=12"+fixed_URL
                
        elif favorite_category in ('television','TV','enternment television', 'Television',' TV series'):
            
            url = "https://opentdb.com/api.php?amount="+str(noQues)+"&category=14"+fixed_URL
                
        elif favorite_category in ('science nature','nature','bio', 'wildlife','Natural'):
            
            url = "https://opentdb.com/api.php?amount="+str(noQues)+"&category=17"+fixed_URL
                
        elif favorite_category in ('computer','PC','servers', 'computers','science computers'):
            
            url = "https://opentdb.com/api.php?amount="+str(noQues)+"&category=18"+fixed_URL
                
        elif favorite_category in ('maths','mathematics','science mathematics', 'math','Maths'):
            
            url = "https://opentdb.com/api.php?amount="+str(noQues)+"&category=19"+fixed_URL
                
        elif favorite_category in ('sports','matches','sport', 'match','Sports'):
            
            url = "https://opentdb.com/api.php?amount="+str(noQues)+"&category=21"+fixed_URL
                
        elif favorite_category in ('geography','geo','Geography'):
            
            url = "https://opentdb.com/api.php?amount="+str(noQues)+"&category=22"+fixed_URL
            
        elif favorite_category in ('history','hist','History'):
            
            url = "https://opentdb.com/api.php?amount="+str(noQues)+"&category=23"+fixed_URL
         
        elif favorite_category in ('Art','art','arts','artist'):
            
            url = "https://opentdb.com/api.php?amount="+str(noQues)+"&category=25"+fixed_URL
          
        elif favorite_category in ('gadgets','science gadgets','Gadgetts'):
            
            url = "https://opentdb.com/api.php?amount="+str(noQues)+"&category=30"+fixed_URL
        
        elif favorite_category in ('vehicles','cars','super cars', 'transport', 'Vehicles'):
            
            url = "https://opentdb.com/api.php?amount="+str(noQues)+"&category=28"+fixed_URL
        
        else:
            category_found= False
            
        
            
        if category_found:
            print("url is  ::::"+url)    
            speech_output = "Asking Questions One By one; "\
                            "Please answer by saying ,"\
                            "Answer is option followed by option:  "
            req = requests.get(url)
            jsonResponce = json.loads(req.text)
            print("json Responce "+str(jsonResponce))
            questions = jsonResponce['results']
            questionNo = 0
                
                
            print("question"+str(questions))
            print("question[0]"+str(questions[questionNo]))
            #print("Question Session "+ session['attributes']['questionJson'])
                
            askquestion = ask_question(questions[questionNo])
            print(str(askquestion))
            speech_output += askquestion['speech_output']
            answer = askquestion['answer']
            answer_option = askquestion['answer_option']
                 
                    
            
            session_attributes = create_question_json_attributes(questions,questionNo, answer, 0, answer_option, level)
                  
            #session_attributes += create_answer_attributes(question['correct_answer'])
            # print("question = " +question['question'] )
            reprompt_text = "Please select your answer. " + askquestion['speech_output']    
            print("request"+req.text)
        else:
            speech_output = "Category not Found. "\
                            "Please select from below category. "\
                            "General Knowledge, Books, Computer, Movies, Songs, History, Television, Maths, Geography, History"
                            
        
            reprompt_text = "Please select a quiz category. "
        
    else:
        speech_output = "I'm not able to find your category. " \
                        "Please try again."
        reprompt_text = "I'm not able to find your category." \
                        "Please select a quiz category. "
                        
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



    
def ask_question(question):
    #question =questionJson[questionNo]
    print(question)
    print(question['incorrect_answers'])
    print("in ask questions"+str(question))
    answer = question['correct_answer']
    speech_output = question['question']  +". options are ;"
    options = []
    options.extend(question['incorrect_answers'])
    options.append(question['correct_answer'])
    alphabet = ['a','b','c','d','e','f','g']
    i = 0
    random.shuffle(options)

    for opt in options:
        speech_output += alphabet[i]+". "+opt + " , "
        if opt == question['correct_answer']:
            answer_option = alphabet[i]
        i+=1
        
    return {"speech_output": speech_output,"answer":answer, "answer_option":answer_option}

def get_answer_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None
    speech_output = ""
    print("Inside Answer intend ")
    
        
    if session.get('attributes', {}) and ("answer" and "questionJson" and "level" and "score" in session.get('attributes', {})):
        should_end_session = False
        level = session['attributes']['level'] 
        print("Inside If of answer Intend")
        questionNo = session['attributes']['questionNo'] +1
        questionJson = session['attributes']['questionJson']
        
        print("Start of code questionJson"+str(questionJson))
        
        print("Before Setting Score")
        score = session['attributes']['score']
        print("Score is : " +str(score))
        score = int(score)
        #print("Int Score"+score)
        answer = session['attributes']['answer']
        answerOption = session['attributes']['answer_option']
        if 'Answer' in intent['slots']:
            
            print("Inside if of getting slots")
            userAnswer = ""
            AnswerFlag = True
            try:
                userAnswer = intent['slots']['Answer']['value'] 
            except Exception, e:
                print("In exception of userAnswer")
                AnswerFlag = False
                #raise e
            
            
            n = 5
            
            ans_can_be = [answer.lower(), answerOption.lower(), answerOption.lower()+" "+answer.lower(), "option "+answerOption.lower(), "option "+answerOption.lower()+" "+answer.lower()]
            if AnswerFlag:
                if userAnswer.lower() in ans_can_be:
                    print("Before Adding 1 : "+ str(score))
                    score = score +1
                    print("After Adding 1 :" + str(score))
                    speech_output = "Congrats Your answer is correct.  "
                    #session_attributes = create_score_attributes(score+1)
                    
                    
                else:
                    speech_output = "Sorry You have selected wrong Answer. "
                
                
                
                level = session['attributes']['level'] 
                
                if questionNo <n:
                    speech_output += " Lets Move on to the Next Question. "  
                    askquestion = ask_question(questionJson[questionNo])
                    answer = askquestion['answer']
                    answer_option = askquestion['answer_option']
                    print(str(askquestion))
                    speech_output += askquestion['speech_output']
                    
                    reprompt_text = "Please select your answer, "+askquestion['speech_output']+". "
                    print('level is '+str(level))
                    session_attributes = create_question_json_attributes(questionJson,questionNo, answer, score,answer_option,level)
                 
                else:
                    askquestion = ask_question(questionJson[n-1])
                    answer = askquestion['answer']
                    answer_option = askquestion['answer_option']
                    if score > (0.75 * n):
                        speech_output += "Bravo your score is "+str(score)+ ". And your level has been upgraded.. Do you wish to continue?"
                        session_attributes = create_question_json_attributes(questionJson,questionNo, answer, score,answer_option, level+1)
                        should_end_session = False    
                        reprompt_text = "Please respond, Do you wish to continue?"
                    else:
                        speech_output += "Thank you. Your score is " +str(score)
                        session_attributes = create_question_json_attributes(questionJson,questionNo, answer, score,answer_option, level)
                        should_end_session = True
            
            else:
                print("in answer intend else : "+str(questionJson[questionNo-1]))
                print("full json"+ str(questionJson))
                questionNo = session['attributes']['questionNo']
                questionJson = session['attributes']['questionJson']
                askquestion = ask_question(questionJson[questionNo])
                answer = askquestion['answer']
                answer_option = askquestion['answer_option']
                speech_output = "Sorry Something Went wrong. " \
                                "Please select your answer, "+askquestion['speech_output']+". "
                #session_attributes = {"xyz":"123"}                
                session_attributes = create_question_json_attributes(questionJson,questionNo, answer, score,answer_option, level)
            
                reprompt_text = "Please select your answer, "+askquestion['speech_output']+". "
                should_end_session = False
                
        else:
            print("in answer intend else : "+ str(questionJson[questionNo-1]))
            print("full json"+str(questionJson))
            questionNo = session['attributes']['questionNo']
            questionJson = session['attributes']['questionJson']
            askquestion = ask_question(questionJson[questionNo])
            answer = askquestion['answer']
            answer_option = askquestion['answer_option']
                
            print("Inside else of getting slots")
            speech_output = "Sorry Something Went wrong. " \
                            "Please select your answer, "+askquestion['speech_output']+". "
            #session_attributes = {"xyz":"123"}
            session_attributes = create_question_json_attributes(questionJson,questionNo, answer, score,answer_option, level)
            reprompt_text = "Please select your answer, "+askquestion['speech_output']+". "
            should_end_session = False
            
            
    else:
        speech_output = "Sorry Something Went wrong, " \
                        "Please Try Again.."
        
        reprompt_text = "Please select your answer"
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        'you answered the question', speech_output, reprompt_text, should_end_session))



# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "CategorySelected":
        return category_selected(intent, session)
    elif intent_name == "AnswerIntent":
        return get_answer_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.YesIntent":
        return get_level_upgraded(intent,session)
        
    elif intent_name == "AMAZON.NoIntent":
        return handle_session_end_request()

    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
