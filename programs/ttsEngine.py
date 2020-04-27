'''
 * ************************************************************
 *      Program: TTS Engine
 *      Type: Python
 *      Author: David Velasco Garcia @davidvelascogarcia
 * ************************************************************
 */

/*
  *
  * | INPUT PORT                           | CONTENT                                                 |
  * |--------------------------------------|---------------------------------------------------------|
  * | /tts/data:i                          | Input text to speech                                    |
  *
  * | OUTPUT PORT                          | CONTENT                                                 |
  * |--------------------------------------|---------------------------------------------------------|
  * | /tts/data:o                          | Mirror output text to speech                            |
  *
'''

# Libraries

import os
import platform
import sys
import time
import pyttsx3
import yarp


print("**************************************************************************")
print("**************************************************************************")
print("                     Program: TTS Module                                  ")
print("                     Author: David Velasco Garcia                         ")
print("                             @davidvelascogarcia                          ")
print("**************************************************************************")
print("**************************************************************************")

print("")
print("Starting system...")

print("")
print("Loading TTS engine...")

print("")
print("Initializing YARP network...")

# Init YARP Network
yarp.Network.init()


print("")
print("Opening data input port with name /tts/data:i ...")

# Open input tts port
tts_inputPort = yarp.Port()
tts_inputPortName = '/tts/data:i'
tts_inputPort.open(tts_inputPortName)

# Create input data bottle
inputBottle=yarp.Bottle()

print("")
print("Opening data output port with name /tts/data:o ...")

# Open output tts port
tts_outputPort = yarp.Port()
tts_outputPortName = '/tts/data:o'
tts_outputPort.open(tts_outputPortName)

# Create output data bottle
outputBottle=yarp.Bottle()


print("")
print("Initializing tts engine...")
ttsEngine = pyttsx3.init()

print("")
print("Detecting system and release version...")
systemPlatform = platform.system()
systemRelease = platform.release()
print(" ")
print("***********************")
print("Configuration detected:")
print("***********************")
print("Platform:")
print(systemPlatform)
print("Release:")
print(systemRelease)

print("")
print("Getting system tts voices...")
systemVoices = ttsEngine.getProperty('voices')

print("")
print("Setting tts voice...")

if (systemPlatform=="Linux"):
    ttsEngine.setProperty('voice',systemVoices[19].id)
elif (systemPlatform=="Windows"):
    ttsEngine.setProperty('voice',systemVoices[1].id)
elif (systemPlatform=="Darwin"):
    ttsEngine.setProperty('voice',systemVoices[1].id)
else:
    ttsEngine.setProperty('voice',systemVoices[1].id)

exit=0

while exit==0:

    # Receive text
    inputBottle.clear()
    print("Waiting for input text...")
    tts_inputPort.read(inputBottle)
    text=inputtBottle.toString()
    print("")

    # Speak
    print("Receive: "+text)
    print("")

    if text!="":
        print("Speaking...")
        ttsEngine.say(text)
        ttsEngine.runAndWait()

        print("")

        # Send text mirror
        outputBottle.clear()
        outputBottle.addString("Text:")
        outputBottle.addString(text)

        tts_outputPort.write(outputBottle)

        if text=="exit":
            exit=1
            ttsEngine.say("Mensaje recibido, apagando el motor de habla")
            ttsEngine.runAndWait()

    else:
        print("Error, empty message.")

# Close YARP ports
print("Closing YARP ports...")
tts_inputPort.close()
tts_outputPort.close()
