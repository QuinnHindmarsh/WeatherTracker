"""
███████ ██████  ██████   ██████  ██████
██      ██   ██ ██   ██ ██    ██ ██   ██
█████   ██████  ██████  ██    ██ ██████
██      ██   ██ ██   ██ ██    ██ ██   ██
███████ ██   ██ ██   ██  ██████  ██   ██
"""

from flask import Flask, render_template, request
import pprint
from main import get_display, stat_month
from API import place_holder
from copy import deepcopy
from ast import literal_eval
app = Flask(__name__)

if __name__ == "__main__":
    app.run()
    #auto runs app when this is run

global last, loc_data
loc_data = {}

def update(new):
    #sees how many locations the weather data has changed for, and if any (x tracks this)
    x = 0
    for item in new:
        if item != last[item]:
            x += 1
        return x


def contact(item):
    #calls a function in my other program to get the API data
    if item != '':
        h = get_display(item)
        return h
    #a function from other program to call the API, and trim data eg
    else:
        return place_holder
        #still needs a value for the HTML table




@app.route('/weather', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
#all possibe endings for the url to load this page
#the methods are how it can get data from the page
def data():

    try: #this runs if the button has been submited
        form_data = {}
        form_data['loc1'] = request.form.get('loc1')
        form_data['loc2'] = request.form.get('loc2')
        form_data['loc3'] = request.form.get('loc3')
        #gets info from the text boxes

        weather_data = contact(form_data['loc1'])
        weather_data2 = contact(form_data['loc2'])
        weather_data3 = contact(form_data['loc3'])
        #gets weather data for the location entered in the text boxes

        global last
        last = {
            'one': weather_data,
            'two': weather_data2,
            'three': weather_data3
        }#updates the last varialbe used to track if there are changed
        global loc_data
        loc_data = deepcopy(form_data)#the locs from the text boxes


        """
        i know i could have just had a 2 way array holding all of this insteed of 3 different dicts
        but working with 2 way arrays inside of this have me some issues 
        and it doesnt need to be scalalbe, and even to make it scalable  not much work is needed this this part of it
        """

          #^^ this is beacuse it still pings it if no location is suplied and just goes off IP location
        return render_template('weather.html', form_data=form_data, weather_data=weather_data,weather_data2=weather_data2, weather_data3=weather_data3)
    except:
        pass

    try: # this runs if a person reloads the page after submiting locations
        print(loc_data)
        weather_data = contact(loc_data['loc1'])
        weather_data2 = contact(loc_data['loc2'])
        weather_data3 = contact(loc_data['loc3'])

        new = {
            'one': weather_data,
            'two': weather_data2,
            'three': weather_data3
        }#used for comparing to past see alert if there are changed
        change = update(new)
        return render_template('weather.html', form_data=loc_data, weather_data=weather_data,weather_data2=weather_data2, weather_data3=weather_data3,change=change)
    #returns the template and data to use in html
    except:
        return render_template('weather.html')#the first time page is loaded/loaded before button is clicked there is no point having a empty table so it just returns nothing
#if its first time loading just returns webpage and no data

@app.route('/past', methods=['POST', 'GET'])
#this is the page for past weather statistics
def past():
    try:#this runs if data has been submited
        loc = request.form.get('loc')
        month = request.form.get('month')
        # gets data for API call
        data = stat_month(loc,month)
        #calls function in other program to call api and process data

        return render_template('past.html',w_data=data)
    #loads the past tempolate and gives it the needed data
    except:
        return render_template('past.html')
    #if its the first time loading it doent give data