#!/usr/bin/python

# #####   Dependencies   ######
import RPi.GPIO as GPIO
import os
from time import gmtime, strftime, sleep
from bitcoinrpc.authproxy import AuthServiceProxy


def runbackup():

    access = AuthServiceProxy("http://rimbitrpc:rimbitrpc@127.0.0.1:8709")
    file_name = strftime("%Y%m%d%H%M%S", gmtime()) + '.bak'
    home_dir = '/home/pi/'
    usb = '/mnt/usb'
    move = 'sudo mv ' + home_dir + file_name + usb
    saved_file = usb + file_name

    if not os.path.exists(usb):
        os.system('sudo mkdir ' + usb)
    
    try:
        lcd_init()

        signal_success()                    # Flash drive located, starting to backup

        if os.path.exists("/dev/sda1"):
            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("Pi Wallet", 2)
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string("Backing Up", 2)

            os.system("sudo umount /dev/sda1")

            os.system("sudo mount -t vfat /dev/sda1 " + usb)
            sleep(1)
            access.backupwallet(home_dir + file_name)
            os.system(move)
            sleep(1)

            if os.path.exists(saved_file):
                lcd_byte(LCD_LINE_1, LCD_CMD)
                lcd_string("Backup Complete", 2)
                lcd_byte(LCD_LINE_2, LCD_CMD)
                lcd_string("Remove USB", 2)

            else:
                lcd_byte(LCD_LINE_1, LCD_CMD)
                lcd_string("Backup Failed", 2)
                lcd_byte(LCD_LINE_2, LCD_CMD)
                lcd_string("Check USB", 2)

        else:
            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("Backup Failed", 2)
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string("No USB Detected", 2)

        sleep(2)

    except:
        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string("Backup Failed", 2)
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string("Check Wallet", 2)

    os.system('sudo umount ' + usb)

    sleep(2)


def lcd_init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)        # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT)   # E
    GPIO.setup(LCD_RS, GPIO.OUT)  # RS
    GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
    GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
    GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
    GPIO.setup(LCD_D7, GPIO.OUT)  # DB7
    GPIO.setup(LED_ON, GPIO.OUT)  # Backlight enable

    # Initialise display
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)


def lcd_string(message, style):
    """ Send [message] to the LCD based on [style] format.
        style:  1 == Left Justified
                2 == Center Justified
                3 == Right Justified
    :param: message = string
    :param: style = int (1-3)
    :return: (none)
    """

    if style == 1:
        message = message.ljust(LCD_WIDTH, " ")
    elif style == 2:
        message = message.center(LCD_WIDTH, " ")
    elif style == 3:
        message = message.rjust(LCD_WIDTH, " ")

    for letter in message:
        lcd_byte(ord(letter), LCD_CHR)
    ''' This is slower and non-Pythonic
        for i in range(LCD_WIDTH):
            lcd_byte(ord(message[i]), LCD_CHR)
    '''


def lcd_byte(bits, mode):
    """Send [bits] to the Pi GPIO data pins.
    :param: bits = a byte of data to send
    :param: mode = Bool. True for characters, False for commands.
    :return: (none)
    """

    GPIO.output(LCD_RS, mode)   # RS

    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)

    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    sleep(E_DELAY)

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)

    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    sleep(E_DELAY)


def signal_success(num_flashes = 5):
    """Send a signal via the Pi when back up is successful."""
    for _ in range(num_flashes):
        GPIO.output(LED_ON, True)
        sleep(0.25)
        GPIO.output(LED_ON, False)
        sleep(0.25)


# #####   Global Definitions   #####
# Define GPIO to LCD mapping
LCD_RS = 26
LCD_E = 19
LCD_D4 = 13
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11
LED_ON = 15

# Define some device constants
LCD_WIDTH = 16  # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005


# #####   Main   #######
if __name__ == '__main__':
    runbackup()

