from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    clima = None
    error = None

    if request.method == 'POST':
        ciudad = request.form.get('ciudad')
        apiKey = "29f12a2f492e3fc1d9064042e6866f47"  # Reemplaza con tu clave de API de OpenWeatherMap
        url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={apiKey}&units=metric&lang=es"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            main = data['main']
            wind = data['wind']
            weatherDescription = data['weather'][0]['description']

            clima = {
                'ciudad': ciudad,
                'temperatura': main['temp'],
                'presion': main['pressure'],
                'humedad': main['humidity'],
                'descripcion': weatherDescription,
                'viento': wind['speed']
            }

        except requests.exceptions.HTTPError as err:
            error = "Ciudad no encontrada o error en la solicitud."
        except Exception as e:
            error = "Ocurrió un error al obtener el clima."

    return render_template('index.html', clima=clima, error=error)

if __name__ == '__main__':
    app.run(debug=True)
