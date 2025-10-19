from flask import Flask, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# A simple in-memory dictionary to store the latest sensor data.
# In a real application, you would use a database (like SQLite, PostgreSQL, or MongoDB).
latest_data = {
    "temperature": 0,
    "humidity": 0,
    "soil": 0,
    "rain": 0,
    "light": "N/A",
    "timestamp": "Never"
}

# --- API Endpoints ---

@app.route('/data', methods=['GET', 'POST'])
def handle_data():
    """
    This endpoint handles both receiving data from the IoT device (POST)
    and sending the latest data to the app (GET).
    """
    if request.method == 'POST':
        # This part receives data from your ESP32
        try:
            # Get the JSON data sent from the ESP32
            new_data = request.get_json()

            # Update our in-memory store with the new data
            # You can add validation here to ensure the data is correct
            global latest_data
            latest_data = new_data
            
            print(f"Received new data: {latest_data}")

            # Return a success response
            return jsonify({"status": "success", "message": "Data received"}), 201

        except Exception as e:
            # Handle potential errors, like badly formatted JSON
            return jsonify({"status": "error", "message": str(e)}), 400

    elif request.method == 'GET':
        # This part sends the latest data to your React Native app
        return jsonify(latest_data)

@app.route('/')
def index():
    """A simple welcome route to check if the server is running."""
    return "<h1>IoT Backend is running!</h1><p>Use /data to GET or POST sensor readings.</p>"


# --- Running the App ---
if __name__ == '__main__':
    # Use 0.0.0.0 to make the server accessible on your local network
    # Get port from environment variable for Render deployment
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
