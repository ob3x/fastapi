from fastapi import FastAPI, HTTPException
import requests as r

app = FastAPI()
API_KEY = "8d75801b383e7e0ede90b7c71ffe9c75"

@app.get("/weather/{city}")
def fetch_weather_data(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = r.get(url)

    if response.status_code == 200:
        data = response.json()

        city_name = data["name"]
        temp = data["main"]["temp"]
        feels_temp = data["main"]["feels_like"]
        description = data["weather"][0]["main"]
        return {f"Temperatura w mieście {city_name} wynosi {temp}°C, odczuwalna temperatura to {feels_temp}°C. OPIS {description}"}
    
    else:
        raise HTTPException(status_code=404, detail="City not found")
    