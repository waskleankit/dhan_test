import streamlit as st
import asyncio
from dhanhq import marketfeed

# Define callback functions
async def on_connect(instance):
    st.write("Connection established")

async def on_message(instance, message):
    if message["type"] == "Ticker Data":
        token = message['security_id']
        ltp = f"{message['LTP']}"
        st.session_state["ltp_data"] = f"LTP for token {token}: {ltp}"

async def on_close(instance):
    st.write("WebSocket closed.")

# Function to run Dhan feed
def run_dhan_feed():
    st.write("WebSocket starting runforever.")
    client_id = '1101864216'
    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQwMDI3NDA2LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMTg2NDIxNiJ9.9Pr25SUPuI5pKPk2vJtZ30_FoEi8qQIttlHUKs_wXpGFa_9-wjufjSK-Oqh5hPX6j1Q8eviHXGTVOCeq5qw0Bw'

    dhan_feed = marketfeed.DhanFeed(
        client_id=client_id,
        access_token=access_token,
        instruments=[(2, '54666')],
        subscription_code=15,
        on_connect=on_connect,
        on_message=on_message,
        on_close=on_close
    )
    dhan_feed.run_forever()
    st.write("WebSocket started runforever.")

# Wrapper to run asyncio tasks in Streamlit
def start_feed():
    if "feed_task" not in st.session_state:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        st.session_state.feed_task = loop.create_task(run_dhan_feed())
        st.write("WebSocket feed started!")

# Stop the WebSocket feed
def stop_feed():
    if "feed_task" in st.session_state:
        st.session_state.feed_task.cancel()
        st.write("WebSocket feed stopped.")
        del st.session_state.feed_task

# Streamlit UI
st.title("Dhan Market Feed")
st.write("Real-time market data using DhanHQ WebSocket")

# Initialize session state for LTP data
if "ltp_data" not in st.session_state:
    st.session_state["ltp_data"] = "No data received yet."

# Display real-time LTP data
st.text("Live Market Data:")
st.text(st.session_state["ltp_data"])

# Run or stop feed based on button clicks
if st.button("Start Feed"):
    start_feed()

if st.button("Stop Feed"):
    stop_feed()



#
# from dhanhq import marketfeed
#
# async def on_connect(instance):
#     print("Connection established")
# async def on_message(instance, message):
#     if message["type"] == "Ticker Data":
#         token = message['security_id']
#         ltp = f"{message['LTP']}"
#         print("LTP", ltp)
#
# async def on_close(instance):
#     print("Web socket closed.")
# def run_dhan_feed():
#     client_id = '1101864216'
#     access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQwMDI3NDA2LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMTg2NDIxNiJ9.9Pr25SUPuI5pKPk2vJtZ30_FoEi8qQIttlHUKs_wXpGFa_9-wjufjSK-Oqh5hPX6j1Q8eviHXGTVOCeq5qw0Bw'
#
#     dhan_feed = marketfeed.DhanFeed(
#         client_id=client_id,
#         access_token=access_token,
#         instruments=[(2, '54666')],
#         subscription_code=15,
#         on_connect=on_connect,
#         on_message=on_message,
#         on_close=on_close
#     )
#     dhan_feed.run_forever()
#
# run_dhan_feed()
