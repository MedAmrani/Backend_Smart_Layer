from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
import requests
from bs4 import BeautifulSoup
from datetime import date
from django.core import serializers
import json
import jsonpickle
import GetOldTweets3 as got
import pandas as pd
import re
from textblob import TextBlob


import joblib
 
from tutorials.models import Covid
from tutorials.serializers import CovidSerializer
from rest_framework.decorators import api_view

@api_view(['GET', 'POST', 'DELETE'])
def scrapeTweets(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        since_date = body['since_date']
        until_date = body['until_date']
        text_query = body['text_query']
        countt = body['count']
        count = int(countt)
        print(since_date)
        data =[]
        
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(text_query)\
                                                .setLang('en')\
                                                .setSince(since_date)\
                                                .setUntil(until_date)\
                                                .setMaxTweets(count)
        # Creation of list that contains all tweets
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)

        # Creating list of chosen tweet data
        text_tweets = [[tweet.date, tweet.text] for tweet in tweets]

        # Creation of dataframe from tweets
        tweets_df = pd.DataFrame(text_tweets, columns = ['Datetime', 'Text'])
        
        listOfCases= [(Tweet(row.Datetime,row.Text)) for index, row in tweets_df.iterrows() ]  
        tweets = []
        for obj in listOfCases :
            data1 = {
                "Datetime":obj.Datetime,
                "Text":obj.Text
                
            }
            tweets.append(data1)

        df = pd.DataFrame(tweets_df, columns = ['Text'])
        
        df['Text'] = df['Text'].apply(cleanTxt)
        df['Subjectivity'] = df['Text'].apply(getSubjectivity)
        df['Polarity'] = df['Text'].apply(getPolarity)
        df['Analysis'] = df['Polarity'].apply(getAnalysis)
        sentiments = df['Analysis'].value_counts()
        print(sentiments)
        
        values = sentiments.to_json(orient='records', lines=True)
        sents = {
            "Positive": values[0],
            "Neutral" : values[2],
            "Negative" : values[4]
        }
        print(values)

        responseData = {
            'Sentiments': sents,
            'tweets': tweets
            
        }
        # Converting tweets dataframe to csv file
        # tweets_df.to_csv('{}-{}k-tweets1.csv'.format(text_query, int(count/1000)), sep=',')  
        
        return JsonResponse(responseData, safe=False)

# Calling function to query X amount of relevant tweets and create a CSV file
#   


@api_view(['GET', 'POST', 'DELETE'])
def scraping(request):
    if request.method == 'GET':
        page = requests.get(
            'https://covid.hespress.com/')
        page.encoding = "utf-8"

        # Create a BeautifulSoup object
        soup = BeautifulSoup(page.text, 'html.parser')
        rows = soup.findAll("div", {"class": "col-7 text-left"})
        rows2 = soup.findAll("div", {"class": "col-3 text-left"})
        rows3 = soup.findAll("div", {"class": "col-6 text-left"})
        rows4 = soup.findAll("div", {"class": "col-8 text-left"})
        table = soup.findAll('tr')
        general = []
        states = []
        names = ['Total_Cases','Eliminated_Cases','Total_Recovred','Total_Deaths',
                'Active_Cases','New_Cases','New_Eliminated_Cases','New_Recovred','New_Deaths']
        i=0
        for row in rows:
            data = {
                names[i] : row.h4.getText()
            }
            i=i+1
            general.append(data)
        try: 
            for row in rows2:
                data = {
                    names[5]: row.a.span.getText()
                }
                general.append(data)
        except:
            print("no new cases")
            data = {
                    names[5]: "0"
                }
            general.append(data)
        try:
            # j=6    
            # for row in rows3:
                data = {
            
                    names[7]: rows3[1].a.span.getText()
                }
                # j=j+1
                general.append(data)
        except:
            print("no new recovred")
            data = {
            
                    names[7]: "0"
                }
                # j=j+1
            general.append(data)
        try:
            for row in rows4:
                data = {
                    
                    names[8]: row.a.span.getText()
                }
                general.append(data)
        except:
            print("no new deaths")
            data = {
                    
                    names[8]: "0"
                }
            general.append(data)
            
        for tab in table:
            td = tab.findAll('td')
            print(td)
            data = {
            
                'state': transformLanguage(tab.th.a.getText()),
                'total': td[0].getText(),
            

            }
            states.append(data)
        responseData = {
            'general': general,
            'states': states
        }
        covids = Covid.objects.all().last()
        covids_serializer = CovidSerializer(covids, many=False)
        print(covids_serializer.data)

        lastObject = covids_serializer.data
        print(lastObject['Date'])
        print(date.today())
        today = date.today()
        today_date = today.strftime("%d/%m/%Y")

        if lastObject['Date'] != today_date:
            covid_serializer = CovidSerializer(data=transform(responseData))
            if covid_serializer.is_valid():
                covid_serializer.save()


        return JsonResponse(covids_serializer.data, safe=False)

    


def transformLanguage(name):
    new_name=''
    if name == 'مراكش أسفي' :
        new_name = 'Marrakech_Safi'
    elif name == 'الدار البيضاء سطات' :
        new_name = 'Casablanca_Settat'
    elif name == 'العيون الساقية الحمراء' :
        new_name = 'Laayoune_SaguiaalHamra'
    elif name == 'طنجة تطوان الحسيمة' :
        new_name = 'Tanger_Tetouan_AlHoceima'
    elif name == 'الرباط سلا القنيطرة' :
        new_name = 'Rabat_Sale_Kenitra'
    elif name == 'الشرق' :
        new_name = 'Oriental'
    elif name == 'فاس مكناس' :
        new_name = 'Fes_Meknes'
    elif name == 'بني ملال خنيفرة' :
        new_name = 'BeniMellal_Khenifra'
    elif name == 'درعة تافيلالت' :
        new_name = 'Draa_Tafilalet'
    elif name == 'سوس ماسة' :
        new_name = 'Sous_Massa'
    elif name == 'كلميم واد نون' :
        new_name = 'Guelmim_OuedNoun'
    elif name == 'الداخلة وادي الذهب' :
        new_name = 'EdDakhla_OuededDahab'
    
    return new_name
    
def transform(responseData):
    
    today = date.today()
    data ={
    'Date': today.strftime("%d/%m/%Y"),
    'Total_Cases': responseData['general'][0]['Total_Cases'],
    'New_Cases': responseData['general'][5]['New_Cases'],
    'Total_Deaths': responseData['general'][3]['Total_Deaths'],
    'New_Deaths': responseData['general'][7]['New_Deaths'],
    'Total_Recovred': responseData['general'][2]['Total_Recovred'],
    'New_Recovred': responseData['general'][6]['New_Recovred'],
    'Eliminated_Cases': responseData['general'][1]['Eliminated_Cases'],
    'Active_Cases':	responseData['general'][4]['Active_Cases'],
    responseData['states'][0]['state']: responseData['states'][0]['total'],
    responseData['states'][1]['state']: responseData['states'][1]['total'],
    responseData['states'][2]['state']: responseData['states'][2]['total'],
    responseData['states'][3]['state']: responseData['states'][3]['total'],
    responseData['states'][4]['state']: responseData['states'][4]['total'],
    responseData['states'][5]['state']: responseData['states'][5]['total'],
    responseData['states'][6]['state']: responseData['states'][6]['total'],
    responseData['states'][7]['state']: responseData['states'][7]['total'],
    responseData['states'][8]['state']: responseData['states'][8]['total'],
    responseData['states'][9]['state']: responseData['states'][9]['total'],
    responseData['states'][10]['state']: responseData['states'][10]['total'],
    responseData['states'][11]['state']: responseData['states'][11]['total']
    
    }
    return data

@api_view(['GET', 'POST', 'DELETE'])
def covid_list(request):
    if request.method == 'GET':
        covids = Covid.objects.all()
        
        covids_serializer = CovidSerializer(covids, many=True)
        return JsonResponse(covids_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        covid_data = JSONParser().parse(request)
        covid_serializer = CovidSerializer(data=covid_data)
        if covid_serializer.is_valid():
            covid_serializer.save()
            return JsonResponse(covid_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(covid_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Covid.objects.all().delete()
        return JsonResponse({'message': '{} covid19 data were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)



@api_view(["POST"])
def predict(request):
    if request.method == 'POST':
        cases_model = joblib.load('C:/Users/crona/myprophet_model.pkl')
        deaths_model = joblib.load('C:/Users/crona/prophet_deaths.pkl')
        recoverd_model = joblib.load('C:/Users/crona/prophet_recovery.pkl')
        # future_days = JSONParser.parse(request)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        future_days = body['future_days']

        cases_future_days = cases_model.make_future_dataframe(periods=int(future_days))
        cases_prediction = cases_model.predict(cases_future_days)

        deaths_future_days = deaths_model.make_future_dataframe(periods=int(future_days))
        deaths_prediction = deaths_model.predict(deaths_future_days)

        recoverd_future_days = recoverd_model.make_future_dataframe(periods=int(future_days))
        recoverd_prediction = recoverd_model.predict(recoverd_future_days)
        
        cases_data = cases_prediction[['ds', 'yhat']][-int(future_days):]
        deaths_data = deaths_prediction[['ds', 'yhat']][-int(future_days):]
        recoverd_data = recoverd_prediction[['ds', 'yhat']][-int(future_days):]
        new_data = cases_data.merge(deaths_data,on='ds').merge(recoverd_data,on='ds')

        # mergedDf = deaths_data.merge(deaths_data, left_index=True, right_index=True)
        # print(cases_data)
        # print(deaths_data)
        # print(recoverd_data)
        # print(new_data)



        listOfCases= [(Data(row.ds,row.yhat_x,row.yhat_y,row.yhat)) for index, row in new_data.iterrows() ]  
        json_data = []
        for obj in listOfCases :
            data1 = {
                "Date":obj.ds,
                "Total_Cases":obj.yhat_x,
                "Total_Deaths":obj.yhat_y,
                "Total_Recoverd":obj.yhat
            }
            json_data.append(data1)
            
        # print(listOfReading)
        # ret = data.to_json(orient='values', date_format='iso')
        # json_string = json.dumps([ob.__dict__ for ob in listOfReading])
        # for obj in listOfReading:
        #     print(transformmm(obj))
        # json_string = json.dumps(listOfReading, default=obj_dict)
        # print(ret)
        return JsonResponse(json_data,safe=False)

class Data:

   def __init__(self, h, p, a, b):
       self.ds = h 
       self.yhat_x = p
       self.yhat_y = a
       self.yhat = b
class Tweet:

    def __init__(self, Datetime, Text):
        self.Datetime = Datetime
        self.Text = Text

def obj_dict(obj):
    return obj.__dict__



def transformmm(myObject):
    return jsonpickle.encode(myObject, unpicklable=False)

def cleanTxt(text):
 text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
 text = re.sub('#', '', text) # Removing '#' hash tag
 text = re.sub('RT[\s]+', '', text) # Removing RT
 text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
 
 return text


# Create a function to get the subjectivity
def getSubjectivity(text):
   return TextBlob(text).sentiment.subjectivity

# Create a function to get the polarity
def getPolarity(text):
   return  TextBlob(text).sentiment.polarity

# Create a function to compute negative (-1), neutral (0) and positive (+1) analysis
def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'