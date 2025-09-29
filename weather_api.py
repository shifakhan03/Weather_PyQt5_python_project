#Importing necessary modules
import sys            #used for system-related stuff like closing the app
import requests       #to get data/make requests from openweather API
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout)   # for making GUI
from PyQt5.QtCore import Qt                                       #for alignment 

#main weatherapplication class
class WeatherApp(QWidget):
    def __init__(self):   
        super().__init__()         #calling parent constructor

        #creating widgets for my UI
        self.city_label = QLabel("Enter city name: ",self)           # label which is asking user for city input
        self.city_input = QLineEdit(self)                            #text box for entering city name
        self.get_weather_button = QPushButton("Get Weather",self)    #Button to trigger weather fetch
        self.temperature_label = QLabel(self)                        #label to display temperature
        self.emoji_label = QLabel(self)                              # Label to display weather emoji
        self.description_label = QLabel(self)                        # Label to display weather description
        self.initUI()         #call UI setup function

    def initUI(self):
        self.setWindowTitle("Shifa's Weather App")   # title of the window

        # vertical layout to arrange items top to bottom
        vbox=QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        
        self.setLayout(vbox)   # setting the layout to main window
        #center aligning all labels and input
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        #now i am setting object names for each widget(css styling)
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        
        #now im taking a style sheet
        self.setStyleSheet("""
            QLabel,QPushButton{
                font-family : calibri;
            }
            QLabel#city_label{
                font-size: 40px; 
                font-style: italic;                    
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 65px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: segeo UI emoji;
            }
            QLabel#description_label{
                font-size: 50px;
            }
        """) 

        #when button is clicked, call the get_weather function
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key="e6b3532558285310d76b3a2307350f76"  #my openweather API key
        city=self.city_input.text()     #getting city name from input
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"    #making url for API call


        try:
            response = requests.get(url)   #sending the request
            response.raise_for_status()    #raises error for bad status codes
            data=response.json()       #converting response to json
 
            if data["cod"]==200:    #checking if city is found
                self.display_weather(data)      #if ok, show weather


        #handles http errors with different error messages
        except requests.exceptions.HTTPError as http_error:
           match response.status_code:
               case 400:
                   self.display_error("Bad request:\npls check ur input")
               case 401:
                   self.display_error("Unauthorized:\nInvalid API key")
               case 403:
                   self.display_error("Forbidden:\n Ur Access is denied")
               case 404:
                   self.display_error("Not Found:\nCity Not Found")
               case 500:
                   self.display_error("Internal Server Error:\npls try again back")
               case 502:
                   self.display_error("Bad Gateway:\nServer's down")
               case 503:
                   self.display_error("Service Unavailable:\npls check ur country")
               case 504:
                   self.display_error("Gateway Timeout:\nNo response from server")
               case _: #im wrting this if incase no matching cases
                   self.display_error(f"http error occured:\n{http_error}")

        #handling internet connection errors           
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Eroor:\nCheck ur internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Eroor:\nThe request has been timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects:\nCheck ur URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")
        
    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size:30px;")   #setting temp label font size
        self.temperature_label.setText(message)    #showing the error message
        self.emoji_label.clear()                  #to clear emoji when error occurs
        self.description_label.clear()            #to clear description when error occurs
        
    def display_weather(self,data):
        temperature_k=data["main"]["temp"]     #temp in kelvin 
        temperature_c=temperature_k - 273.15   #converting  kelvin to celsius
        temperature_f=(temperature_k*9/5) - 459.67   #converts kelvin to fahrenheit butnot used now
        weather_id=data["weather"][0]["id"]           #getting weather condition id
        weather_description=data["weather"][0]["description"]     #getting description (like clear sky)
    
        self.temperature_label.setText(f"{temperature_c:.0f}°C")   #displaying celsius temp only
        self.emoji_label.setText(self.get_weather_emoji(weather_id))   #setting a emoji 
        self.description_label.setText(weather_description)     #showing description of type of weather


    @staticmethod
     #here im matching emoji for different weather conditions
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"  #thunderstorms
        elif 300 <= weather_id <= 321:
            return "🌦️" #partially cloudy
        elif 500 <= weather_id <= 531:
            return "🌧️" #rainy
        elif 600 <= weather_id <= 622:
            return "❄️" #snow
        elif 701 <= weather_id <= 741:
            return "💨" #mist,dust,smoke
        elif weather_id == 762:
            return "🌋" #volcano
        elif weather_id == 781:
            return "🌪️" #tornado
        elif weather_id <= 800:
            return "🌞" #clear sky
        elif 801 <= weather_id <= 804:
            return "☁️" #different clouds
        else: 
            return ""
        
#running the app from here
if __name__ == "__main__":
    app=QApplication(sys.argv)  #create an app instance
    weather_app=WeatherApp()  #creating  a main window
    weather_app.show()        #this shows the app window
    sys.exit(app.exec_())     #runs the app in loop ...until closed
 