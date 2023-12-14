from flask import Flask, request, jsonify

class SimpleApi:
    def __init__(self):
        self.app = Flask(__name__)
        self.value = 0

        self.app.route('/set_value', methods=['POST'])(self.set_value)
        self.app.route('/get_value', methods=['GET'])(self.get_value)

    def set_value(self):
        data = request.get_json()
        new_value = data.get('value')

        if new_value is not None and isinstance(new_value, int):
            self.value = new_value
            return jsonify({'message': 'Value set successfully'}), 200
        else:
            return jsonify({'error': 'Invalid value provided'}), 400

    def get_value(self):
        return jsonify({'value': self.value}), 200

    def run_api(self):
        self.app.run(host='0.0.0.0', port=5000)
