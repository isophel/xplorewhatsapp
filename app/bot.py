from flask import Flask, request
import requests
import logging
import json
import tweepy
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
logging.basicConfig(filename='data.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route('/bot', methods=['GET','POST'])
def bot():
   
    # Get the message the user sent our Twilio number
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'tweets'in incoming_msg:
        #Retreive tweets from Twitter API
        consumer_key = 'GWA86Mzj6gVmGQVPR4V2tL8Qk'
        consumer_secret = '4sahREY1Lzp82R1Ap49nIxUnBHXAaZjFGd3kuekHgJUzHItk7n'
        access_token = '1041371062414528513-irZGuN4dPecJqFt1whbHeGyqdbavgH'
        access_token_secret = 'ehP1RRdjQGDlGF1d2MKIp22NrGdzRwba9uhrE5pHr8LP5'
        auth =tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        screen_name = 'TourismBoardUg'
        count = 3
        tweets = api.user_timeline(screen_name=screen_name, count=count)

        tweetsdata =  tweets[0].text + '\n' + tweets[1].text + '\n' + tweets[2].text
        msg.body(tweetsdata)
        responded = True
        app.logger.info('request for tweets')
        
    if 'destination' in incoming_msg:
        # return a destination
        r = requests.get('http://xplorebot.herokuapp.com/destinations/?format=json')
        if r.status_code == 200:
            
            data = r.json()
            #looping through data to get a single response
            for i in data:
                msg.body(f'{i["name"]}\n{i["about"]}\n{i["link"]}\n')  
                msg.media(i['image'])
                msg.body('\n-------------------------------\n')
                responded = True
            app.logger.info('request for destinations')
        else:
            msg.body('I could not retrieve any destination, sorry.')

    if 'car' in incoming_msg:
        #return cars 
        r = requests.get('http://xplorebot.herokuapp.com/carhire/?format=json')
        if r.status_code == 200:
            cars = r.json()
            for i in cars:
                msg.body(f'{i["type"]}\n {i["carlocation"]}\n{i["price"]}\n {i["contact"]}')  
                msg.media(i['carimage'])
                msg.body('\n-------------------------------\n')
                responded = True
            app.logger.info('request for car hire')
        else:
            msg.body('I couldn''t find any car, sorry.')
    if 'hotel' in incoming_msg:
        #return hotels
        r = requests.get('http://xplorebot.herokuapp.com/hotels/?format=json')
        if r.status_code == 200:
            hotels = r.json()
            for i in hotels:
                linkrates =  i['rates']
                msg.body(f'{i["Hname"]}\n{i["location"]}\n{i["Services"]}\n {i["Website"]}\n {i["email"]}' + 'Download the rates here\n' + linkrates)  
                msg.media(i['Image'])
                #msg.media(i['rates'])
                msg.body('\n-------------------------------\n')
                responded = True
            app.logger.info('request for hotels')
        else:
            msg.body('I couldn''t find any hotel, sorry.')
    if 'tour companies' in incoming_msg:
        #return tour companies
        r = requests.get('http://xplorebot.herokuapp.com/tourcompanies/?format=json')
        if r.status_code == 200:
            tourcompanies = r.json()
            for i in tourcompanies:
                msg.body(f'{i["Cname"]}\n {i["location"]}\n{i["Services"]}\n {i["website"]}\n {i["email"]}')  
                msg.media(i['Cimage'])
                msg.body('\n-------------------------------\n')
                responded = True
            app.logger.info('request for tour companies')
        else:
            msg.body('I couldn''t find any tour company, sorry.')
    if 'tour guides' in incoming_msg:
        #return tour guides
        r = requests.get('http://xplorebot.herokuapp.com/tourguides/?format=json')
        if r.status_code == 200:
            tourguides = r.json()
            for i in tourguides:
                msg.body(f'{i["Tname"]}\n {i["Bio"]}\n{i["phonenumber"]}\n {i["link"]}\n')  
                msg.media(i['profileimage'])
                msg.body('\n-------------------------------\n')
                responded = True
            app.logger.info('request for tour guides')
        else:
            msg.body('I couldn''t find any tour guide, sorry.')
       
        
    if 'trip' in incoming_msg:
        # return a trip
        r = requests.get('https://xplorebot.herokuapp.com/trips/?format=json')
        if r.status_code == 200:
            tripdata = r.json()
            poster = tripdata[1]['poster']
            desc = tripdata[1]['desc']
            duration =tripdata[1]['duration']
            inclusions = tripdata[1]['Inclusions']
            exclusions = tripdata[1]['Exclusions']
            date = tripdata[1]['Date']
            accmtype = tripdata[1]['accmtype']
            price = tripdata[1]['price']
            payments = tripdata[1]['paymentmthd']
            
            tripdataresponse = f'{desc}\n Duration:{duration}\n Inclusions:{inclusions}\n Date: {date}\n Accomodation Type:{accmtype}\n Price: {price}\n Payement Method:{payments}'
        else:
            tripdataresponse = 'I could not retrieve any Trips at the moment, sorry.'

        msg.body(tripdataresponse)  
        msg.media(poster)
        responded = True
        app.logger.info('request for trips')
    
    if 'fact' in incoming_msg:
        r = requests.get('https://xplorebot.herokuapp.com/facts/?format=json')  
        if r.status_code == 200: 
            factdata  = r.json()
            fact = factdata[0]['Fbody']  
            image = factdata[0]['Image']
            factresponse = f'{fact}\n'
        else:
            factresponse = 'Not facts available' 
        msg.body(factresponse)  
        msg.media(image)
        responded = True
        app.logger.info('request for facts')

    if 'thanks' in incoming_msg:
        msg.body('You are welcome!')
        responded = True
    if not responded:
        msg.body('Hello \U0001f600 , I am Xplorebot I give recommendations about various tourism aspects in Uganda which include.\n Destinations\nTrips\n Facts\nHotels and Accommodation\n Car hire\n Tour Companies \nYou can also ask me to send you tweets, \nThank you for using Xplorebot')
        app.logger.info('request for default response')
       
    return str(resp)

# @app.route('/print')
# def printMsg():
#     consumer_key = 'GWA86Mzj6gVmGQVPR4V2tL8Qk'
#     consumer_secret = '4sahREY1Lzp82R1Ap49nIxUnBHXAaZjFGd3kuekHgJUzHItk7n'
#     access_token = '1041371062414528513-irZGuN4dPecJqFt1whbHeGyqdbavgH'
#     access_token_secret = 'ehP1RRdjQGDlGF1d2MKIp22NrGdzRwba9uhrE5pHr8LP5'
#     auth =tweepy.OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_token_secret)
#     api = tweepy.API(auth)
#     screen_name = 'TourismBoardUg'
#     count = 3
#     tweets = api.user_timeline(screen_name=screen_name, count=count)
#     r2 = requests.get('http://xplorebot.herokuapp.com/destinations/?format=json')
#     data = r2.json()
#     name = data[0]['name']
#     description = data[0]['about']
#     image = data[0]['image']
#     link = data[0]['link']

#     # name = data2['name']
#     # image = data2['image']
#     # description = data2['about']
#     app.logger.warning('testing warning log')
#     app.logger.error('testing error log')
#     app.logger.info('some cool stuff')
#     return  tweets[0].text + '\n' + tweets[1].text + '\n' + tweets[2].text

if __name__ == '__main__':
    app.run()