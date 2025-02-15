import urllib.request
import json
from django.shortcuts import render
from django.contrib import messages
# Create your views here.


def index(request):
    data = {}
    
    if request.method == 'POST':
        city = request.POST['city']
        
        try:
            source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=625af5386ef1dc7478c0f57f57d0ca6b').read()
            list_of_data = json.loads(source)
            
            if list_of_data['cod'] != 200:
                messages.error(request, f"Error: {list_of_data['message']}")
            else:
                # Convert temperature from Kelvin to Celsius
                temp_celsius = round(float(list_of_data['main']['temp']) - 273.15, 2)
                
                data = {
                    "country_code": str(list_of_data['sys']['country']),
                    "coordinate": str(list_of_data['coord']['lon']) + ', ' 
                    + str(list_of_data['coord']['lat']),
                    "temp": str(temp_celsius) + ' °C',
                    "pressure": str(list_of_data['main']['pressure']),
                    "humidity": str(list_of_data['main']['humidity']),
                    'main': str(list_of_data['weather'][0]['main']),
                    'description': str(list_of_data['weather'][0]['description']),
                    'icon': list_of_data['weather'][0]['icon'],
                }
                print(data)
                
        except urllib.error.HTTPError as e:
            messages.error(request, f"HTTP Error: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            messages.error(request, f"URL Error: {e.reason}")
        except KeyError as e:
            messages.error(request, f"Invalid city name. Please try again.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, "main/index.html", data)
