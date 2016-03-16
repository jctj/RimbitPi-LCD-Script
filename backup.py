#!/usr/bin/python

#import
import RPi.GPIO as GPIO
import time
import os
import RPi.GPIO as GPIO
from time import gmtime, strftime
from bitcoinrpc.authproxy import AuthServiceProxy
import sys

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


def runbackup():

    access = AuthServiceProxy("http://rimbitrpc:rimbitrpc@127.0.0.1:8709")
    date = strftime("%Y%m%d%H%M%S", gmtime())
    dir = '/home/pi/' 
    move = 'sudo mv /home/pi/' + (date) + '.bak' + ' ' + '/mnt/usb'
    
    lcd_init()

    GPIO.output(LED_ON, True)
    time.sleep(0.25)
    GPIO.output(LED_ON, False)
    time.sleep(0.25)
    GPIO.output(LED_ON, True)
    time.sleep(0.25)
      
    try:
      lcd_byte(LCD_LINE_1, LCD_CMD)
      lcd_string("Pi Wallet",2)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string("Backing Up",2)
      
      os.system ("sudo mount -t vfat /dev/sda1 /mnt/usb")
      time.sleep(1)
      access.backupwallet (dir + date + '.bak')
      os.system (move)
      time.sleep(1)
      os.system ('sudo umount /mnt/usb')
        
      lcd_byte(LCD_LINE_1, LCD_CMD)
      lcd_string("Backup Complete",2)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string("Remove USB",2)

      time.sleep(2)


    except:
      lcd_byte(LCD_LINE_1, LCD_CMD)
      lcd_string("Backup Failed",2)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string("Check Wallet",2)

      time.sleep(2)

def lcd_init():
  GPIO.setwarnings(False)
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
  runbackup()
