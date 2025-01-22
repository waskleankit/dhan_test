
from dhanhq import marketfeed

async def on_connect(instance):
    print("Connection established")
async def on_message(instance, message):
    if message["type"] == "Ticker Data":
        token = message['security_id']
        ltp = f"{message['LTP']}"
        print("LTP", ltp)

async def on_close(instance):
    print("Web socket closed.")
def run_dhan_feed():
    client_id = '1101864216'
    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQwMDI3NDA2LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMTg2NDIxNiJ9.9Pr25SUPuI5pKPk2vJtZ30_FoEi8qQIttlHUKs_wXpGFa_9-wjufjSK-Oqh5hPX6j1Q8eviHXGTVOCeq5qw0Bw'

    dhan_feed = marketfeed.DhanFeed(
        client_id=client_id,
        access_token=access_token,
        instruments=[(2, '54666')]
    )
    dhan_feed.run_forever()

run_dhan_feed()