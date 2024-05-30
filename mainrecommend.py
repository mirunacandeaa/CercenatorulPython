from flask import Flask, jsonify, request
from recommendationAI import collaborative_filtering

app = Flask(__name__)

# Funcție pentru generarea recomandărilor
def generate_recommendations():
    # Aici apelăm funcția collaborative_filtering pentru a genera recomandările
    collaborative_filtering()  # Presupunând că aveți o funcție numită collaborative_filtering care generează recomandări

# Definim o rută pentru a primi cererile de recomandări
@app.route('/generate_recommendations', methods=['GET', 'POST'])
def handle_generate_recommendations():
    if request.method == 'POST':
        # Generăm recomandările doar dacă cererea este de tip POST
        generate_recommendations()

    # Nu returnăm nimic înapoi către aplicație
    return ''

# Setăm antetul pentru acces CORS pentru toate răspunsurile
@app.after_request
def set_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5001)
