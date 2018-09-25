from flask import Flask,render_template,request
from elasticsearch import Elasticsearch

import json
import nltk                 # Analyzing Text with the Natural Language Toolkit
import pprint
import re

app = Flask(__name__)

# es = Elasticsearch('localhost:16200/') # for LTM server
es = Elasticsearch('localhost:9200/')                           # change the port


@app.route('/', methods=["GET", "POST"])
def index():
    tempQuery = request.args.get("q")                           # Using Get Method

    # Read the txt file and store into 2D array (questionSolution)
    '''
    with open("questionType.txt") as file:
        questionSolution = [line.rstrip("\n").split(";") for line in file]
    '''
    # Using loop to compare the question type, check tempQuery contain those word or not


    # Process the query from user input
    #print tempQuery

    #tempQuery = request.form.get("q")                           # Using POST Method
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

        '''
        print splitTextArray[1][0]
        print splitTextArray[1][1]
        print splitTextArray[1][2]
        '''

        # Check which platform
        platform = request.user_agent.platform

        return render_template("index.html",
                                q=tempQuery,
                                response=resp,
                                resultLength = len(resp['hits']['hits']),
                                scroll='scrollContent',
                                location=splitTextArray,
                                checkPlatform=platform
                                )
    return render_template('index.html')        # End of if statement


if __name__== "__main__":
    app.run(debug=True,port=16000)

'''
   Similarity module
   Google search: elasticsearch similarity
'''
