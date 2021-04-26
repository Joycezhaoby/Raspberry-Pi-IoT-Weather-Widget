from num2words import num2words
from subprocess import call
import awsconnect


cmd_beg= 'espeak '
cmd_end= ' 2>/dev/null' # To dump the std errors to /dev/null
'''
cmd_end= ' | aplay /home/pi/Desktop/Text.wav  2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
cmd_out= '--stdout > /home/pi/Desktop/Text.wav ' # To store the voice file
'''
#text = input("Enter the Text: ")
#print(text)

#Replacing ' ' with '_' to identify words in the text entered
#text = text.replace(' ', '_')

#Calls the Espeak TTS Engine to read aloud a Text
#call([cmd_beg+cmd_out+text+cmd_end], shell=True)
#call([cmd_beg+text+cmd_end], shell=True)


def speak(text):
    text = text.replace(' ', '_')
    call([cmd_beg+text+cmd_end], shell=True)

def notify(trigger_info, weather,screen_on):
    awsconnect.send_AWS(trigger_info, weather)
    # send weather info and trigger info to aws
    # aws sends email/notifications
    # receive text string from aws
    aws_text = "something from aws"
    if screen_on:
        speak(aws_text)
        
#speak(text)