#all storeage

API_key = "removed for privacy reasons"
base_url = "https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={APIkey}"
remove_list = ['feels_like', 'pressure', 'humidity']

stat_url = 'https://history.openweathermap.org/data/2.5/aggregated/month?q={city},au&month={month}&appid={API_key}'

want = {'average_max': 'average max temp',
        'average_min': 'average min temp',
        'record_max': 'max temp ',
        'record_min': 'lowest temp',
        'sunshine_hours': 'hours of sun'}

warn = {
    'wind_speed': 40,
    'temp_max': 40,
    'temp_min': -5,
    'rain': 25

}#appologies if these values dont represent what would constatuite a warning, its close enough

place_holder = {

  '1h': 'n/a',
 'deg': 'n/a',
 'speed': 'n/a',
 'temp': 'n/a',
 'temp_max': 'n/a',
 'temp_min': 'n/a'
}

Radar_URL = 'https://tile.openweathermap.org/map/precipitation_new/{zoom}/{x_tiles}/{y_tiles}.png?appid={API}'
