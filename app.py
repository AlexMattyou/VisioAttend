from flask import Flask, render_template, request, jsonify
from threading import Thread
app = Flask(__name__) 
  
@app.route("/send_json") 
def index(): 
   return render_template("index.html") 

@app.route('/send_json', methods=['POST'])
def receive_json():
    data = request.json  # Get JSON data sent from the client
    print('Received JSON data:', data)
    # Process the data as needed
    print("yeay")
    response_data = {'message': 'Data received successfully'}
    return jsonify(response_data)
  
if __name__ == '__main__': 
   app.run(debug = True) 