"""
███████ ██████  ██████   ██████  ██████
██      ██   ██ ██   ██ ██    ██ ██   ██
█████   ██████  ██████  ██    ██ ██████
██      ██   ██ ██   ██ ██    ██ ██   ██
███████ ██   ██ ██   ██  ██████  ██   ██
"""

from copy import deepcopy
from pprint import pprint  # better looking print for JSON
import calendar
import requests  # used for requesting information with the API

import API  # imports local file used for storing base url/key

global base_url #so i can use these in functions without declaring them
global api_key
global country

country = 'AU' #incase i want to expand to global functionality
base_url = API.base_url
api_key = API.API_key

global x

def testing():
    return 8

def warning_checK(data):
    #checks for weather conditions requireing a warning
    warn = API.warn
    #they are all ifs as i want to warn for multiple things if there are multiple things
    issues = []

    if data['speed'] >= warn['wind_speed']:
        issues.append('high wind speed warning')
    if float((data['temp'].replace('°C',''))) >= warn['temp_max']:
        # ^ removes the '°C' and converts to float for comparaion
        issues.append('heat wave warning')
    if float((data['temp'].replace('°C',''))) <= warn['temp_min']:
        issues.append(' cold front ')
    if data['rain'] >= warn['rain']:
        issues.append('possible flood warning')

    if len(issues) > 2:
        return issues
    return None

def degrees_to_cardinal(deg):
    #gets compass direction from wind degrese
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    ix = int((deg + 11.25)/22.5 - 0.02)
    return dirs[ix % 16]

def get_wheather():
    #gets the wheather fow ehere the user wants
    while True:#repeats untill the return triggers, ending the loop
        #this is inplace incase there is a issue (user entered wrong place,
        User_city = input('please enter the city you would like wheather for \n')
        URL = base_url.format(city_name = User_city, country_code = country, APIkey = api_key)
    #^ adds needed items to the url to call
        data = requests.get(URL)
        code = data.status_code
        if code == 200: #if its a sucess returns the data and leaves loop
            data = data.json()
            return data
        else: #if location is invalid prints that, and if there is another error, says there is a error and prints code
            if code == 404:
                print('sorry that location is invalid please try again')
            else:
                print('sorry there was a erorr try again \n status code:',code)

def weather_get(User_city):
    #gets the wheather fow ehere the user wants
    #this is inplace incase there is a issue (user entered wrong place,
    URL = base_url.format(city_name = User_city, country_code = country, APIkey = api_key)
#^ adds needed items to the url to call
    data = requests.get(URL)
    code = data.status_code
    print(URL)
    if code == 200: #if its a sucess returns the data and leaves loop
        data = data.json()
        return data
    else: #if location is invalid prints that, and if there is another error, says there is a error and prints code
        return code

def data_trim(data):
    #trims data
    trimed_data = {
        'temp_whole': data['main'],
        'wind': data['wind'],
        'loc': data['name'],
    }
    try: # it only sends the rain data if there has been rain in the last hour so i need this incase there hasnt been rain
        trimed_data['rain'] = data['rain']
    except KeyError: #basically if it doesnt work it skips this
        trimed_data['rain'] = 0

    #^ gets the fields i actually and puts them in a dict

    return trimed_data #returns it for use out of this function


def k_to_c(temp): #converts kelvin to celsuis and returns value
    return (temp -273.15)

def temp_check(temp):
    #converts units and rounds
    temp = k_to_c(temp)#converts units
    temp = str(round(temp,1)) + '°C'  #rounds so not long and adds c symbol
    return temp

def fuck_off(data, remove):
    #manages alot of data to make it more usable
    revamp = {} # ill output this list
    for item in data:
        if type(data[item]) != dict:
            revamp[item] = data[item]
        else:
            for ite, i in data[item].items():
                #^ loops though all items in dict
                if ite not in remove:
                    if 'temp' in ite:#if its a temprature it runs the function to deal with it
                        i = temp_check(i)
                    elif ite == 'deg':# if its degrese turns it to compass direction
                            i = degrees_to_cardinal(i)
                    revamp.update({ite:i})
                    #writes all of the items in there updated form to dict
    return revamp


def get_display(User_city):
    """
    this combines functions together
    it gets data, trims it twice to whats needed
    converts units, rounds units and add °C
    """
    #data = get_wheather() outdated as getting user data from website

    data = weather_get(User_city)
    trim = data_trim(data)
    trim = fuck_off(trim, API.remove_list)


    trim['warnings'] = warning_checK(trim)
    return trim

def month_num(month):#from the month being a full name of abveration it gets coraspoinding month of the year as that is needed for the api
    month = month.lower()
    x = 1
    while calendar.month_abbr[x].lower() != month and calendar.month_name[x].lower() != month:
        x += 1
    return x

def stat_trim(data):
    #turns it from a 3d array to a dictionary (with most of the same data)
    revamp = {}
    for item in data:
        if type(data[item]) == dict:#im aware that cus i dont have a else at the end of this getting the data that not all data is collected but i dont need it
            for ite, i in data[item].items():
                if type(i) == dict:
                    for ii in i:
                        revamp[ii] = i[ii]
                else:
                    revamp[ite] = i
    return revamp

def remove(data):
    #removes all things from the dict that are not needed for display.
    revamp = {}
    for key in data:
        if key in API.want:
            revamp[API.want[key]] = data[key]#checks if the key is in a dict in API, if it is then it saves the value and changes key name in a enw list
    return revamp

def temp_status(new,old):
    #checks if the key is related to temp. if it is then it calls a function converting units, adding a 'c' and rounding and replaces the value to that
    for item in new:
        if item in old['temp']:
            new[item] = temp_check(new[item])
    return new

def stat_month(user_city, month):
    #calls all of the needed functions for getting past data
    month = month_num(month)
    url = API.stat_url.format(city=user_city,month=month,API_key=api_key)
    h = requests.get(url).json()
    data = stat_trim(h)
    data = temp_status(data,h['result'])
    final_data = remove(data)


    return final_data

#pprint(stat_month('sydney','june'))
#pprint(get_display('sydney'))
#test line^