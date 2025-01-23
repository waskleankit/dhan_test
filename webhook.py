from flask import Flask, request
from threading import Thread

# Initialize Flask app
app = Flask(__name__)

# Global list to store received data
received_data = []

# Flask route for webhook
@app.route('/webhook', methods=['POST', 'GET'])
def webhook_handler():
    try:
        # Capture headers, data, and client IP
        headers = dict(request.headers)
        data = request.get_json() if request.is_json else request.get_data(as_text=True)
        ip_address = request.remote_addr

        # Append received data to the global list
        received_data.append({
            "headers": headers,
            "data": data,
            "ip_address": ip_address
        })

        # Respond to webhook request
        return "Webhook received successfully", 200
    except Exception as e:
        return f"Error: {e}", 500

# Function to run Flask app in a separate thread
def start_flask():
    app.run(host="0.0.0.0", port=8500)

# Start Flask server
flask_thread = Thread(target=start_flask, daemon=True)
flask_thread.start()

# Streamlit placeholder (to keep the app running)
import streamlit as st
st.title("Webhook Receiver")
st.write("This app is configured to receive data at `/webhook`.")
st.write("No other functionality is provided.")
st.write("Send POST/GET requests to the URL below:")
st.code("https://ankitwebhookdhantest.streamlit.app/webhook", language='bash')



# import streamlit as st
# from http.server import BaseHTTPRequestHandler, HTTPServer
# import threading
# import json
#
# # Create a server class to handle incoming requests
# class WebhookHandler(BaseHTTPRequestHandler):
#     logs = []  # Shared log for storing webhook requests
#
#     def do_POST(self):
#         # Read and log headers and data
#         content_length = int(self.headers['Content-Length'])
#         post_data = self.rfile.read(content_length).decode('utf-8')
#         WebhookHandler.logs.append({
#             "Headers": dict(self.headers),
#             "Data": post_data,
#             "IP Address": self.client_address[0]
#         })
#         # Respond to the request
#         self.send_response(200)
#         self.end_headers()
#         self.wfile.write(b"Webhook received")
#
#     def do_GET(self):
#         self.send_response(200)
#         self.end_headers()
#         self.wfile.write(b"Server running")
#
# # Start a server in a separate thread
# def start_server():
#     server = HTTPServer(('0.0.0.0', 5000), WebhookHandler)
#     server.serve_forever()
#
# # Streamlit App
# st.title("Webhook Listener in Streamlit")
# st.write("Use this app to visualize incoming webhooks.")
#
# # Start the server if not already started
# if "server_thread" not in st.session_state:
#     server_thread = threading.Thread(target=start_server, daemon=True)
#     server_thread.start()
#     st.session_state["server_thread"] = server_thread
#     st.success("Webhook server started at http://0.0.0.0:5000")
#
# # Display logs
# if WebhookHandler.logs:
#     st.subheader("Received Webhook Logs")
#     for idx, log in enumerate(WebhookHandler.logs):
#         st.markdown(f"### Log {idx + 1}")
#         st.json(log)
# else:
#     st.info("No webhooks received yet.")
#
# st.stop()
#
#
# import streamlit as st
# import json
# import time
# from threading import Event, Thread
#
# url = None
# headers = None
# timestamp = None
# stop_event = Event()
#
# def generate_event_stream():
#     global url, headers, timestamp, stop_event
#
#     while not stop_event.is_set():
#         output = {
#             'timestamp': timestamp,
#             'url': url,
#             'headers': headers
#         }
#         st.write(f"data: {json.dumps(output)}")
#         st.markdown("""---""")
#         time.sleep(0.5)
#
# def handle_postback():
#     global url, headers, timestamp
#
#     data = st.session_state.get('data', None)
#     if data:
#         url = data['url']
#         headers = data['headers']
#         timestamp = data['time']
#
#         print(f'Received new data at {timestamp}:')
#         print(f'URL: {url}')
#         print(f'Headers: {headers}')
#
# def start_update_stream():
#     global stop_event
#     stop_event.clear()
#     Thread(target=generate_event_stream, daemon=True).start()
#     st.session_state['is_running'] = True
#
# def stop_update_stream():
#     global stop_event
#     stop_event.set()
#     st.session_state['is_running'] = False
#
# st.title("Webhook Listener")
#
# if 'data' not in st.session_state:
#     st.session_state['data'] = None
#
# if 'is_running' not in st.session_state:
#     st.session_state['is_running'] = False
#
# if st.button("Start"):
#     handle_postback()
#     start_update_stream()
#
# if st.button("Stop"):
#     stop_update_stream()
#
# if st.session_state['is_running']:
#     st.write("Real-time updates are running...")
# else:
#     st.write("Real-time updates are stopped.")