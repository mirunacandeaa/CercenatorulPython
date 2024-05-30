from flask import Flask, jsonify, request
from webscrapper import webscrapper

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def hello_world():


    # Preiați valorile din parametrii URL-ului cererii
    durata = request.args.get('Durata')
    dificultate = request.args.get('Dificultate')
    regiune = request.args.get('Regiune')


    print(durata, dificultate, regiune)
    # Afișați textul în consolă
    if durata!=None and dificultate!=None and regiune!=None:
        print('Sunt in if')
        filtered_hikes_durata = webscrapper(regiune, dificultate, durata)

    else:
        print("Sunt in else ")
        filtered_hikes_durata=[]
    # Inițializăm o listă pentru a stoca răspunsurile pentru fiecare traseu
    responses = []

    #recommendationEngine(filtered_hikes_durata)

    for hike in filtered_hikes_durata:
        response_data = {
            'Region': hike.region,
            'Place': hike.place,
            'Difficulty': hike.difficulty,
            'Kilometers': hike.km,
            'Hours': hike.hour
        }
        # Adăugăm răspunsul pentru traseul curent în listă
        responses.append(response_data)

    # Returnăm lista de răspunsuri ca un răspuns JSON
    response = jsonify(responses)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == '__main__':
    app.run()
