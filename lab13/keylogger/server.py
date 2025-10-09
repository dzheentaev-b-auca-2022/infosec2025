import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/getfile', methods=['POST'])
def receive_logs():
   data = request.json
   with open("win64logs.txt", "a") as file:
       file.write(data.get("logs","")+ "\n")
   return {"status": "success"}, 200

if __name__ == "__main__":
       if not os.path.exists("win64logs.txt"):
            open("win64logs.txt", "w").close()

       app.run(host="0.0.0.0", port=8080)