# Descript: Send Crypto currency prices
# Import Libraries
# pip install BeautifulSoup4
from bs4 import BeautifulSoup
import requests
import time
import smtplib
import ssl
import json
from email.mime.text import MIMEText as MT
from email.mime.multipart import MIMEMultipart as MM

DOGE = 'DOGEUSDT'
BTC = 'BTCUSDT'

# Store email address receiver/sender
receiver = 'phonenumber'
#receiver = 'email'
sender = 'emailSender'
sender_password = 'passwordSender'

# Get Price Function
def get_crypto_price(coin):
  # Get URL
  url = "https://www.google.com/search?q="+coin+"+price"

  # Make request
  HTML = requests.get(url)

  # Parse HTML
  soup = BeautifulSoup(HTML.text, 'html.parser')

  # Find price
  text = soup.find("div", attrs={'class':'BNeawe iBp4i AP7Wnd'}).text

  # Return text
  return text

def get_ticker_price(ticker):
  # Curl ticker info
  url = "https://api.binance.com/api/v3/ticker/24hr?symbol="+ticker
  HTML = requests.get(url)
  soup = BeautifulSoup(HTML.text, 'html.parser')
  site_json = json.loads(soup.text)
  return site_json['askPrice']

def get_ticker_change(ticker):
  # Curl ticker info
  url = "https://api.binance.com/api/v3/ticker/24hr?symbol="+ticker
  HTML = requests.get(url)
  soup = BeautifulSoup(HTML.text, 'html.parser')
  site_json = json.loads(soup.text)
  return site_json['priceChangePercent']

# Send emails
def send_email(sender, receiver, sender_password, text_price):
  # Create a MIMEMulitpart Object
  msg = MM()
  msg['Subject'] = "Crypto Prices"
  msg['From'] = sender
  msg['To'] = receiver
  
  # Create HTML for msg
  HTML = """<html>
              <body>
                <h1>New Crypto Price</h1>
                <h2>"""+text_price+"""</h2>
              </body>
            </html>"""

  # Create hHTML MIMEText Object
  MTObj = MT(HTML, "html")

  # Attach the MIMEText Object
  msg.attach(MTObj)

  # Create SSL context object
  SSL_context = ssl.create_default_context()
  # Create SMTP connection
  server = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, context=SSL_context)
  # Login to the email
  server.login(sender, sender_password)
  # Send the email
  server.sendmail(sender, receiver, msg.as_string())

  # Send alert function
def send_alert():
  oldtimeBTC = time.time()
  oldtimeDGE = time.time()
  # Create infinite loop to send/show price
  while True:
    t = time.localtime()
    current_time = time.strftime("%H:%M", t)
    # Get price
    BTCPrice = get_ticker_price(BTC)
    DOGEPrice = get_ticker_price(DOGE)
    # Check changes
    BTCChange = float(get_ticker_change(BTC))
    DOGEChange = float(get_ticker_change(DOGE))
    #print("BTC: "+BTCPrice+" Change: "+str(BTCChange)+" DOGE: "+DOGEPrice+" Change: "+str(DOGEChange))
    
    if (BTCChange < -10 or BTCChange > 10) and (time.time() - oldtimeBTC > 3600):
      print("BTC is now " + BTCPrice + " It has changed " + str(BTCChange) + " in the last 24 hours")
      price_text = "BTC is now " + BTCPrice + " It has changed " + str(BTCChange) + " in the last 24 hours"
      send_email(sender, receiver, sender_password, price_text)
      oldtimeBTC = time.time()
    if (DOGEChange < -10 or DOGEChange > 10) and (time.time() - oldtimeDGE > 3600):
      print("DOGE is now " + DOGEPrice + " It has changed " + str(DOGEChange) + " in the last 24 hours")
      price_text = "DOGE is now " + DOGEPrice + " It has changed " + str(DOGEChange) + " in the last 24 hours"
      send_email(sender, receiver, sender_password, price_text)
      oldtimeDGE = time.time()
    if current_time == '20:30':
      price_text = "BTC: "+BTCPrice+" DOGE: "+DOGEPrice
      send_email(sender, receiver, sender_password, price_text)
      time.sleep(600)

send_alert()

