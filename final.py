import pandas as pd
import matplotlib.pyplot as plt
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def get_nepse_data():
    
    data = {
        'Company': [
            'Nabil Bank', 'Nepal Investment Bank', 'NIC Asia Bank', 'Global IME Bank',
            'Himalayan Bank', 'Everest Bank', 'Prabhu Bank', 'Sanima Bank',
            'Machhapuchhre Bank', 'Kumari Bank'
        ],
        'Stock Price': [1050, 980, 970, 950, 930, 920, 910, 900, 890, 880]
    }
    
    
    df = pd.DataFrame(data)
    
    
    df.to_csv('nepse_data.csv', index=False)
    
    return df


def generate_stock_chart(df):
    top_10 = df.sort_values(by='Stock Price', ascending=False).head(10)
    
    plt.figure(figsize=(10, 5))
    plt.bar(top_10['Company'], top_10['Stock Price'], color='blue')
    plt.xlabel('Company')
    plt.ylabel('Stock Price (NPR)')
    plt.title('Top 10 Companies by Stock Price - Nepse')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    
    plt.savefig('nepse_chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Stock chart generated for top 10 companies.")


def get_kathmandu_weather():
    
    weather_info = {
        "city_name": "Kathmandu",
        "main": {
            "temp": 277.72,
            "temp_min": 275.632,
            "temp_max": 279.15,
            "feels_like": 273.99,
            "pressure": 1029,
            "humidity": 75,
            "dew_point": 280.33
        },
        "weather": [{
            "id": 500,
            "main": "Rain",
            "description": "light rain",
            "icon": "10n"
        }],
        "wind": {
            "speed": 2.6,
            "deg": 10,
            "gust": 5.8
        },
        "clouds": {
            "all": 75
        },
        "visibility": 10000
    }
    temperature = weather_info['main']['temp'] - 273.15 
    humidity = weather_info['main']['humidity']
    weather_conditions = weather_info['weather'][0]['description']
    
    weather_info_text = f"Temperature: {temperature:.2f}°C, Humidity: {humidity}%, Conditions: {weather_conditions}"
    
    print(weather_info_text)
    return weather_info_text


def save_quote_and_weather():
    
    quote = random.choice([
        "Believe you can and you're halfway there.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: It is the courage to continue that counts."
    ])
    
    
    weather_info = get_kathmandu_weather()
    
    
    data = {
        'Quote': [quote],
        'Weather in Kathmandu': [weather_info]
    }
    df = pd.DataFrame(data)
    
    
    df.to_csv('quote_weather_data.csv', index=False)
    print("Quote and weather data saved successfully.")


def send_email(df):
    sender_email = "ishanigiri7@gmail.com"
    receiver_email = "giriishy66@gmail.com"
    password = "bprv yrks wseb oskh"
    
    
    weather_info = get_kathmandu_weather()
    
    
    quote = random.choice([
        "The only limit is your mind",
        "Inhale courage, exhale fear.",
        "Stay hungry, stay foolish."
    ])
    
    
    top_10 = df.sort_values(by='Stock Price', ascending=False).head(10)
    
    
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Daily Inspiration & Nepse Report"
    
    body = f"Good Morning!\n\nToday's Quote: {quote}\n\nWeather in Kathmandu: {weather_info}\n\nTop 10 Companies by Stock Price:\n"
    for index, row in top_10.iterrows():
        body += f"{row['Company']}: NPR {row['Stock Price']}\n"
    body += "\nHave a great day!"
    
    message.attach(MIMEText(body, 'plain'))
    
    
    with open('nepse_chart.png', 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename=nepse_chart.png")
        message.attach(part)
    
    try:
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    
    nepse_data = get_nepse_data()

    
    generate_stock_chart(nepse_data)
    
    
    save_quote_and_weather()
    
    
    send_email(nepse_data)
