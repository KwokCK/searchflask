from flask import Flask,render_template,request,session,redirect,url_for,escape
from elasticsearch import Elasticsearch

import json
import nltk                 # Analyzing Text with the Natural Language Toolkit
import pprint
import re
import time

app = Flask(__name__)

# es = Elasticsearch('localhost:16200/') # for LTM server
es = Elasticsearch('localhost:9200/')                           # change the port

@app.route('/', methods=["GET", "POST"])
def index():
    tempQuery = request.args.get("q")                           # Using Get Method
    tempButtonID = request.args.get("TestValue")
    # Read the txt file and store into 2D array (questionSolution)
    '''
    with open("questionType.txt") as file:
        questionSolution = [line.rstrip("\n").split(";") for line in file]
    '''
    # Using loop to compare the question type, check tempQuery contain those word or not


    # Process the query from user input
    #print tempQuery

    #tempQuery = request.form.get("q")                           # Using POST Method
    if 'userSession' in session:
        # Check if session existed, direct read session if  existed
        # return 'Logged in as %s' % escape(session['username'])
        if tempQuery is not None:
            resp = es.search\
                (index='csearch', doc_type='doc', body=
                    # For fuzzy query

                    { # start of Query
                        "query": {
                            "match": {
                                "content": {
                                    "query": tempQuery,
                                    "fuzziness": "AUTO",
                                    "operator" : "and"
                                }
                            }
                        }
                    } # End of Query
                 )
            # End of search
            #myString = resp['hits']['hits'][0]['_source']['content']    # Display the first answer

            #i = 0

            #print len(myString.split('\n'))

            #while i < len(myString):
            #    print myString.splitlines()[i]
            #    i += 1

            #print len(resp['hits']['hits'])                        # Count how many result

            # The q=tempQuery refers to the input value from table
            # The response=resp refers to the query answer


            # Testing: Printing the location of the file

            print '---'
            i = 0
            splitTextArray = []
            while i < len(resp['hits']['hits']):

                rowText = resp['hits']['hits'][i]['_source']['path']['virtual']
                splitText = filter(None, re.split("[/_P a r t . p d f]+", rowText))
                splitTextArray.append(splitText)

                #pprint.PrettyPrinter(depth=6).pprint(resp['hits']['hits'][i]['_source']['path']['virtual'])
                #print splitText
                i += 1
            print '---'
            print 'Button ID is: ' + tempButtonID;

            '''
            print splitTextArray[1][0]
            print splitTextArray[1][1]
            print splitTextArray[1][2]
            '''

            # Check which platform (IOS/ Android/ Windows)
            platform = request.user_agent.platform

            with open("log.txt", "a") as logFile:
                logFile.write(  "\n"+
                                time.strftime('%Y/%m/%d %H:%M:%S')+
                                ",2,"+
                                session['userSession']+
                                ","+
                                "Query: "+tempQuery
                                )

            return render_template("index.html",
                                    q=tempQuery,
                                    response=resp,
                                    resultLength = len(resp['hits']['hits']),
                                    scroll='scrollContent',
                                    location=splitTextArray,
                                    checkPlatform=platform,
                                    userID=session['userSession']
                                    )
        return render_template('index.html')        # End of if statement
    #return redirect(url_for('/login'))
    return render_template('login.html')

@app.route('/checkUserSession', methods=['GET', 'POST'])
# @app.route('/csearch/checkUserSession', methods=['GET', 'POST'])
def checkUserSession():

    # timeNow = time.strftime("%c")
    ## date and time representation
    # print "Current date & time " + time.strftime("%c")

    if request.method == 'POST':
        userName = request.form['user']
        session['userSession'] = userName
        # print session['userSession'] + 'has logged'
        with open("log.txt", "a") as logFile:
            logFile.write(  "\n"+
                            time.strftime('%Y/%m/%d %H:%M:%S')+
                            ",1,"+
                            session['userSession'] + " has logged")

        return render_template('index.html')
    elif request.method == 'GET':
        if 'user' in session:
            return render_template('index.html')
        else:
            return render_template('login.html')

app.secret_key = 'kwokchakkwan'

if __name__== "__main__":
    app.run(debug=True,port=16000)

'''
   Similarity module
   Google search: elasticsearch similarity
'''
