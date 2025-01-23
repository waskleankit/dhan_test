from flask import Flask, request, Response
import time
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_postback():
    def generate():
        while True:
            data = request.get_json()

            # Extract relevant information
            url = data['url']
            headers = data['headers']
            timestamp = data['time']

            # Process the response data as needed
            output = {
                'timestamp': timestamp,
                'url': url,
                'headers': headers
            }

            yield f"data: {json.dumps(output)}\n\n"
            time.sleep(2)  # Simulate a 2-second delay

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run()


# from flask import Flask, render_template, request, jsonify, session
# import asyncio
# from dhanhq import marketfeed
# from threading import Thread
#
# # Create Flask app
# app = Flask(__name__)
# app.secret_key = "your_secret_key"  # Required for Flask sessions
#
# # Initialize a variable to store the LTP data
# ltp_data = {"message": "No data received yet."}
#
# # Define callback functions
# async def on_connect(instance):
#     print("Connection established")
#
# async def on_message(instance, message):
#     if message["type"] == "Ticker Data":
#         token = message["security_id"]
#         ltp = f"{message['LTP']}"
#         ltp_data["message"] = f"LTP for token {token}: {ltp}"
#         print(ltp_data["message"])
#
# async def on_close(instance):
#     print("WebSocket closed.")
#
# # Function to run Dhan feed
# def run_dhan_feed():
#     client_id = "1101864216"
#     access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQwMDI3NDA2LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMTg2NDIxNiJ9.9Pr25SUPuI5pKPk2vJtZ30_FoEi8qQIttlHUKs_wXpGFa_9-wjufjSK-Oqh5hPX6j1Q8eviHXGTVOCeq5qw0Bw"
#
#     dhan_feed = marketfeed.DhanFeed(
#         client_id=client_id,
#         access_token=access_token,
#         instruments=[(2, "54666")],
#         subscription_code=15,
#         on_connect=on_connect,
#         on_message=on_message,
#         on_close=on_close,
#     )
#     dhan_feed.run_forever()
#     print('socket started')
#
# # Background thread to manage the event loop
# def start_event_loop():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(run_dhan_feed())
#
# # Start the WebSocket feed
# @app.route("/start_feed", methods=["POST"])
# def start_feed():
#     if not session.get("feed_running"):
#         thread = Thread(target=start_event_loop)
#         thread.start()
#         session["feed_running"] = True
#         return jsonify({"status": "Feed started!"})
#     return jsonify({"status": "Feed is already running."})
#
# # Stop the WebSocket feed
# @app.route("/stop_feed", methods=["POST"])
# def stop_feed():
#     # Currently, stopping asyncio tasks gracefully in Flask requires more logic.
#     session["feed_running"] = False
#     return jsonify({"status": "Feed stopped! (Manual stop not implemented)"})
#
# # Get the latest LTP data
# @app.route("/get_data", methods=["GET"])
# def get_data():
#     return jsonify(ltp_data)
#
# # Home route
# @app.route("/")
# def home():
#     return render_template("index.html")
#
# # Flask app entry point
# if __name__ == "__main__":
#     app.run(debug=True)
