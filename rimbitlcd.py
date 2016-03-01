#!/usr/bin/python

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

#import
import os
import RPi.GPIO as GPIO
import time
from bitcoinrpc.authproxy import AuthServiceProxy
import netifaces as ni
import requests
import math
import urllib2
import simplejson
import httplib
from urlparse import urlparse

# Define GPIO to LCD mapping
LCD_RS = 26
LCD_E  = 19
LCD_D4 = 13 
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11
LED_ON = 15

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005


def main():
  while True:
    
    # Rimbit RPC Settings
    # Set RPC USerName and PassWD
    access = AuthServiceProxy("http://rimbitrpc:rimbitrpc@127.0.0.1:8709")

    #Choose Currency
    #Choices are case sensitive
    #Supported currencies are usd eur cny cad rub btc
    currency = "usd"

    #RPC getinfo
    info = access.getinfo()

    #Change info to string for future searching
    getinfo = "'"+str(info)+"'"

    #Used to determin lock state
    locked = "You cannot earn interest until you unlock your wallet"
    encryptedunlocked ="unlocked_until"

    #Zero values show as "0E-8"
    zero = "0E-8"

    #Check for lock status
    if locked in getinfo:
      status = "Locked"
    elif encryptedunlocked in getinfo:
      status = "Unlocked"
    else:
      status = "Not Encrypted"
    #Define split based on locked or unlocked wallet
    if status == "Locked":
      a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu, vv, ww, xx, yy  = getinfo.split()

      #When locked "NewMint" info is at split qq
      newmint = qq
      connectedpeers = b
    elif status == "Unlocked":
      a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo, pp, qq,  = getinfo.split()

      #When Unlocked "NewMint info is at split ii
      newmint = ii
      connectedpeers  = b
    else:
      a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo  = getinfo.split()
      newmint = ii
      connectedpeers  = b

    #Checks to see if newmint is "0E-8"  
    if zero in newmint:
      mint = "0"
    else:
      mint = str(newmint)

    #Remove "," from connectedpeers
    peers = connectedpeers.replace(",","")  

    #RPC getblocks
    blocks = access.getblockcount()

    #RPC getbalance
    totalbalance = access.getbalance()
    balance = str(totalbalance)
    if zero in balance:
      amount = "0"
    else:
      amount = str(balance)

    #Test Internet connection  
    hostname = "google.com"
    response = os.system("ping -c 1 " + hostname)
    if response == 0:

      #Check API Server Status
      def checkUrl(url):
        p = urlparse(url)
        conn = httplib.HTTPConnection(p.netloc)
        conn.request('HEAD', p.path)
        resp = conn.getresponse()
        return resp.status < 400

      if __name__ == '__main__':
        api = checkUrl('http://coinmarketcap-nexuist.rhcloud.com/api/rbt/price')
        if api == True:
 
          #Find current trading price of RBT
          coincap = url = "http://coinmarketcap-nexuist.rhcloud.com/api/rbt/price"
          req = urllib2.Request(url)
          opener = urllib2.build_opener()
          f = opener.open(req)
          json = simplejson.load(f)
    
          if currency == "usd":
            abv = " USD"
            price = json.get('usd')
          elif currency == "eur":
            abv = " EUR"
            price = json.get('eur')
          elif currency == "cny":
            abv = " CNY"
            price = json.get('cny')
          elif currency == "cad":
            abv = " CAD"
            price = json.get('cad')
          elif currency == "rub":
            abv = " RUB"
            price = json.get('rub')
          elif currency == "btc":
            abv = " BTC"
            price = json.get('btc')
          else:
            abv = " ???"
            price = "Incorrect Currency"

        else:
          abv = " "
          price = "API DOWN"
          

    else:
      abv = " "
      price = "Check WAN"

    #Find IP address of acctive network interface
    nic = ni.gateways()['default'][ni.AF_INET][1]
    ni.ifaddresses(nic)
    ip = ni.ifaddresses(nic)[2][0]['addr']
    
    lcd_init()

    GPIO.output(LED_ON, True)
    time.sleep(0.25)
    GPIO.output(LED_ON, False)
    time.sleep(0.25)
    GPIO.output(LED_ON, True)
    time.sleep(0.25)
    
    # Display Current Number of Blocks
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("Number of Blocks",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string(str(blocks),2)
    
    time.sleep(5) # 5 second delay
    
    lcd_init()

    GPIO.output(LED_ON, True)
    time.sleep(0.25)
    GPIO.output(LED_ON, False)
    time.sleep(0.25)
    GPIO.output(LED_ON, True)
    time.sleep(0.25)
    
    # Display Current Number of Connected Peers
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("Number of Peers",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string(str(peers),2)
    
    time.sleep(5) # 5 second delay
  
    lcd_init()

    GPIO.output(LED_ON, True)
    time.sleep(0.25)
    GPIO.output(LED_ON, False)
    time.sleep(0.25)
    GPIO.output(LED_ON, True)
    time.sleep(0.25)
    
    # Display Current Rimbit Balance
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("Wallet Balance",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string(str(amount[:12]) +" ""RBT",2)
    
    time.sleep(5)

    lcd_init()

    GPIO.output(LED_ON, True)
    time.sleep(0.25)
    GPIO.output(LED_ON, False)
    time.sleep(0.25)
    GPIO.output(LED_ON, True)
    time.sleep(0.25)
    
    # Display Current Rimbit Price in Selected Currency
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("RBT Price"+str(abv),2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string(str(price),2)

    
    time.sleep(5)
  
    lcd_init()

    GPIO.output(LED_ON, True)
    time.sleep(0.25)
    GPIO.output(LED_ON, False)
    time.sleep(0.25)
    GPIO.output(LED_ON, True)
    time.sleep(0.25)
   
    #time.sleep(5)
  
    #lcd_init()

    #GPIO.output(LED_ON, True)
    #time.sleep(0.25)
    #GPIO.output(LED_ON, False)
    #time.sleep(0.25)
    #GPIO.output(LED_ON, True)
    #time.sleep(0.25)
    
    # Display Current Lock Status
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("Pi Wallet is",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string(str(status),2)
    
    time.sleep(5) # 5 second delay
  
    lcd_init()
    
    GPIO.output(LED_ON, True)
    time.sleep(0.25)
    GPIO.output(LED_ON, False)
    time.sleep(0.25)
    GPIO.output(LED_ON, True)
    time.sleep(0.25)
    
      # Display New Mint Amount
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("New Mint",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string(str(mint[:12]) + " ""RBT",2)
    
    time.sleep(5) # 5 second delay
  
    lcd_init()

    GPIO.output(LED_ON, True)
    time.sleep(0.25)
    GPIO.output(LED_ON, False)
    time.sleep(0.25)
    GPIO.output(LED_ON, True)
    time.sleep(0.25)
    
    # Display Current IP
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("Pi Wallet IP",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string(str(ip),2)
    
    time.sleep(5)
      # Turn off backlight
  GPIO.output(LED_ON, False)
  

def lcd_init():
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
  GPIO.setup(LED_ON, GPIO.OUT) # Backlight enable  
  # Initialise display
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)  
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)  

def lcd_string(message,style):
  # Send string to display
  # style=1 Left justified
  # style=2 Centred
  # style=3 Right justified

  if style==1:
    message = message.ljust(LCD_WIDTH," ")  
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)      

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)   

if __name__ == '__main__':
  main()
