import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
import os
from PyQt5.QtCore import Qt
from dotenv import load_dotenv

class weatherapp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter the city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get weather", self)
        self.temp_label = QLabel(self)
        self.desc_label = QLabel(self)
        self.emoji_label = QLabel(self)

        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Weather app")

        vbox = QVBoxLayout()
        
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.desc_label)
        

        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temp_label.setObjectName("temp_label")
        self.desc_label.setObjectName("desc_label")
        self.emoji_label.setObjectName("emoji_label")

        self.setStyleSheet("""
    QLabel, QPushButton {
        font-family: Calibri;
    }
    QLabel#city_label {
        font-size: 24px;
        font-style: italic;
    }
    QLineEdit#city_input {
        font-size: 20px;
        padding: 5px;
    }
    QPushButton#get_weather_button {
        font-size: 20px;
        font-weight: bold;
        padding: 8px;
    }
    QLabel#temp_label {
        font-size: 36px;
    }
    QLabel#emoji_label {
        font-size: 48px;
        font-family: 'Segoe UI Emoji';
    }
    QLabel#desc_label {
        font-size: 24px;
    }
""")

    
        self.get_weather_button.clicked.connect(self.get_weather)
        self.setMinimumSize(400, 300)
        self.resize(500, 400)  # default size

    def get_weather(self):
        load_dotenv()
        api_key = os.getenv("API_KEY")
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized\nInvalid API key")
                case 402:
                    self.display_error("Forbidden\nAccess denied")
                case 403:
                   self.display_error("Not found\nCity not found")
                case 404:
                    self.display_error("Not found\nCity not found")
                case 405:
                    self.display_error("Bad request\nPlease check your input")
                case 406:
                    self.display_error("Bad request\nPlease check your input")
                case 407:
                    self.display_error("Bad request\nPlease check your input")
                case 408:
                    self.display_error("Bad request\nPlease check your input")
                case _:
                    self.display_error(http_error)
        
        except requests.exceptions.ConnectionError:
            self.display_error("Connection error\ncheck your internet")
        except requests.exceptions.Timeout:
            self.display_error("Connection timed out\nTry again later")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects")
        except requests.exceptions.RequestException as reqtexpterror:
            self.display_error(f"{reqtexpterror}")


    def display_error(self, message):
        
        self.temp_label.setText(message)

    def display_weather(self, data):
        temp = data["main"]["temp"]
        display_temp = temp - 273
        desc = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]

        self.emoji_label.setText(self.get_emoji(weather_id))
        self.temp_label.setText(f"{round(display_temp)}°C")
        self.desc_label.setText(f"{desc}")
        #print(f"{round(display_temp)}\n{desc}")

    @staticmethod
    def get_emoji(weather_id):
        if weather_id >= 200:
            return "⛈️"
        elif weather_id >= 300:
            return "🌧️"
        elif weather_id >= 500:
            return "🌧️"
        elif weather_id >= 600:
            return "❄️"
        elif weather_id >= 700:
            return "🌫️"
        elif weather_id == 800:
            return "☀️"
        elif weather_id > 800:
            return "☁️"
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = weatherapp()
    weather_app.show()
    sys.exit(app.exec_())