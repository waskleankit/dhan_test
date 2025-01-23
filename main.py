from flask import Flask, request, render_template_string, Response
import json
import time

app = Flask(__name__)

# Variable to store the latest JSON data
latest_data = None
last_sent_data = None  # Variable to track the last sent data

# Route to handle POST requests and store JSON data
@app.route('/post', methods=['POST'])
def handle_post():
    global latest_data
    latest_data = request.get_json()
    print("Received data:", latest_data)
    return '', 200  # Return a 200 response with no content

# Route to display the latest JSON data
@app.route('/')
def display_data():
    def generate():
        global last_sent_data
        while True:
            if latest_data and latest_data != last_sent_data:
                # If data has changed, send the new data and update last_sent_data
                last_sent_data = latest_data
                yield f"data: {json.dumps(latest_data)}\n\n"
            time.sleep(1)  # Delay for the next update

    return Response(generate(), mimetype='text/event-stream')

# HTML template with JavaScript for displaying live JSON data
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSON Data Viewer</title>
</head>
<body>
    <h1>Latest JSON Data</h1>
    <pre id="json-data">Waiting for data...</pre>

    <script type="text/javascript">
        // Connect to the server-side event stream
        const eventSource = new EventSource("/");

        // Listen for new messages from the server
        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);
            document.getElementById('json-data').textContent = JSON.stringify(data, null, 4);
        };
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


# from flask import Flask, request, render_template_string, Response
# import json
# import time
#
# app = Flask(__name__)
#
# # Variable to store the latest JSON data
# latest_data = None
#
# # Route to handle POST requests and store JSON data
# @app.route('/post', methods=['POST'])
# def handle_post():
#     global latest_data
#     latest_data = request.get_json()
#     print("Received data:", latest_data)
#     return '', 200  # Return a 200 response with no content
#
# # Route to display the latest JSON data
# @app.route('/')
# def display_data():
#     def generate():
#         while True:
#             if latest_data:
#                 # Send the latest data as an event
#                 yield f"data: {json.dumps(latest_data)}\n\n"
#             time.sleep(1)  # Delay for the next update
#
#     return Response(generate(), mimetype='text/event-stream')
#
# # HTML template with JavaScript for displaying live JSON data
# html = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>JSON Data Viewer</title>
# </head>
# <body>
#     <h1>Latest JSON Data</h1>
#     <pre id="json-data">Waiting for data...</pre>
#
#     <script type="text/javascript">
#         // Connect to the server-side event stream
#         const eventSource = new EventSource("/");
#
#         // Listen for new messages from the server
#         eventSource.onmessage = function(event) {
#             const data = JSON.parse(event.data);
#             document.getElementById('json-data').textContent = JSON.stringify(data, null, 4);
#         };
#     </script>
# </body>
# </html>
# """
#
# @app.route('/')
# def home():
#     return render_template_string(html)
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)


# from flask import Flask, request, render_template_string
# import json
#
# app = Flask(__name__)
#
# # Variable to store the latest JSON data
# latest_data = None
#
# # Route to handle POST requests and store JSON data
# @app.route('/post', methods=['POST'])
# def handle_post():
#     global latest_data
#     # Parse incoming JSON data
#     latest_data = request.get_json()
#     print("Received data:", latest_data)
#     return '', 200  # Return a 200 response with no content
#
# # Route to display the latest JSON data
# @app.route('/')
# def display_data():
#     global latest_data
#     # Render the JSON data as a webpage
#     html = """
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>JSON Data Viewer</title>
#     </head>
#     <body>
#         <h1>Latest JSON Data</h1>
#         <pre>{{ data }}</pre>
#     </body>
#     </html>
#     """
#     return render_template_string(html, data=json.dumps(latest_data, indent=4) if latest_data else "No data received yet.")
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
#
#
#
# # from flask import Flask, render_template, request, jsonify, session
# # import asyncio
# # from dhanhq import marketfeed
# # from threading import Thread
# #
# # # Create Flask app
# # app = Flask(__name__)
# # app.secret_key = "your_secret_key"  # Required for Flask sessions
# #
# # # Initialize a variable to store the LTP data
# # ltp_data = {"message": "No data received yet."}
# #
# # # Define callback functions
# # async def on_connect(instance):
# #     print("Connection established")
# #
# # async def on_message(instance, message):
# #     if message["type"] == "Ticker Data":
# #         token = message["security_id"]
# #         ltp = f"{message['LTP']}"
# #         ltp_data["message"] = f"LTP for token {token}: {ltp}"
# #         print(ltp_data["message"])
# #
# # async def on_close(instance):
# #     print("WebSocket closed.")
# #
# # # Function to run Dhan feed
# # def run_dhan_feed():
# #     client_id = "1101864216"
# #     access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQwMDI3NDA2LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMTg2NDIxNiJ9.9Pr25SUPuI5pKPk2vJtZ30_FoEi8qQIttlHUKs_wXpGFa_9-wjufjSK-Oqh5hPX6j1Q8eviHXGTVOCeq5qw0Bw"
# #
# #     dhan_feed = marketfeed.DhanFeed(
# #         client_id=client_id,
# #         access_token=access_token,
# #         instruments=[(2, "54666")],
# #         subscription_code=15,
# #         on_connect=on_connect,
# #         on_message=on_message,
# #         on_close=on_close,
# #     )
# #     dhan_feed.run_forever()
# #     print('socket started')
# #
# # # Background thread to manage the event loop
# # def start_event_loop():
# #     loop = asyncio.new_event_loop()
# #     asyncio.set_event_loop(loop)
# #     loop.run_until_complete(run_dhan_feed())
# #
# # # Start the WebSocket feed
# # @app.route("/start_feed", methods=["POST"])
# # def start_feed():
# #     if not session.get("feed_running"):
# #         thread = Thread(target=start_event_loop)
# #         thread.start()
# #         session["feed_running"] = True
# #         return jsonify({"status": "Feed started!"})
# #     return jsonify({"status": "Feed is already running."})
# #
# # # Stop the WebSocket feed
# # @app.route("/stop_feed", methods=["POST"])
# # def stop_feed():
# #     # Currently, stopping asyncio tasks gracefully in Flask requires more logic.
# #     session["feed_running"] = False
# #     return jsonify({"status": "Feed stopped! (Manual stop not implemented)"})
# #
# # # Get the latest LTP data
# # @app.route("/get_data", methods=["GET"])
# # def get_data():
# #     return jsonify(ltp_data)
# #
# # # Home route
# # @app.route("/")
# # def home():
# #     return render_template("index.html")
# #
# # # Flask app entry point
# # if __name__ == "__main__":
# #     app.run(debug=True)
