import streamlit as st
import time
from dhanhq import dhanhq

# Title and Description
st.title("Real-Time Order Tracker")
st.write("This app fetches and displays updated orders from DhanHQ in real-time.")

# Client credentials
client_id = '1101864216'
access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQwMDI3NDA2LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMTg2NDIxNiJ9.9Pr25SUPuI5pKPk2vJtZ30_FoEi8qQIttlHUKs_wXpGFa_9-wjufjSK-Oqh5hPX6j1Q8eviHXGTVOCeq5qw0Bw'

# Initialize DhanHQ client
try:
    dhan = dhanhq(client_id, access_token)
except Exception as e:
    st.error(f"Failed to initialize DhanHQ client: {e}")
    st.stop()

# Create a container to display the orders
placeholder = st.empty()

# Real-time Order Tracker Function
def fetch_orders():
    try:
        while True:
            # Fetch the list of orders
            orders = dhan.get_order_list()

            # Update the Streamlit app with the fetched orders
            with placeholder.container():
                st.subheader("Updated Orders")
                if orders:
                    st.json(orders)
                else:
                    st.info("No orders found.")
                st.write("=" * 50)

            # Sleep to avoid overwhelming the server
            time.sleep(5)
    except Exception as e:
        st.error(f"Error fetching orders: {e}")
    except KeyboardInterrupt:
        st.info("Stopped fetching orders.")

# Streamlit Button to Start Fetching Orders
if st.button("Start Tracking Orders"):
    st.info("Fetching orders...")
    fetch_orders()


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
import streamlit as st
import json
import time
from threading import Event, Thread

url = None
headers = None
timestamp = None
stop_event = Event()

def generate_event_stream():
    global url, headers, timestamp, stop_event

    while not stop_event.is_set():
        output = {
            'timestamp': timestamp,
            'url': url,
            'headers': headers
        }
        st.write(f"data: {json.dumps(output)}")
        st.markdown("""---""")
        time.sleep(0.5)

def handle_postback():
    global url, headers, timestamp

    data = st.session_state.get('data', None)
    if data:
        url = data['url']
        headers = data['headers']
        timestamp = data['time']

        print(f'Received new data at {timestamp}:')
        print(f'URL: {url}')
        print(f'Headers: {headers}')

def start_update_stream():
    global stop_event
    stop_event.clear()
    Thread(target=generate_event_stream, daemon=True).start()
    st.session_state['is_running'] = True

def stop_update_stream():
    global stop_event
    stop_event.set()
    st.session_state['is_running'] = False

st.title("Webhook Listener")

if 'data' not in st.session_state:
    st.session_state['data'] = None

if 'is_running' not in st.session_state:
    st.session_state['is_running'] = False

if st.button("Start"):
    handle_postback()
    start_update_stream()

if st.button("Stop"):
    stop_update_stream()

if st.session_state['is_running']:
    st.write("Real-time updates are running...")
else:
    st.write("Real-time updates are stopped.")