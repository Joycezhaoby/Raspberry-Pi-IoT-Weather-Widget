from num2words import num2words
from subprocess import call
import awsconnect

cmd_beg= 'espeak '
cmd_end= ' 2>/dev/null' # To dump the std errors to /dev/null

def speak(text):
    text = text.replace(' ', '_')
    call([cmd_beg+text+cmd_end], shell=True)

# send weather info and trigger info to aws
# aws sends email/notifications
def notify(trigger_info, weather,screen_on):
    awsconnect.send_AWS(trigger_info, weather)
    aws_text = "The temperature in {}, {} drops below".format(weather[0],weather[1]) + trigger_info
    if screen_on: #annouce weather if a user is present
        speak(aws_text)