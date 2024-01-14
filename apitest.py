from flask import Flask, jsonify

app = Flask(__name__)

# Flask API values
API_HOST = '0.0.0.0'
API_PORT = 5000
API_SUCCES = 200
capacity = 69

@app.route('/capacity', methods=['GET'])
def get_integer():
    return jsonify({'capacity of the tank': capacity}), API_SUCCES


if __name__ == '__main__':
    app.run(host= API_HOST, port= API_PORT)
