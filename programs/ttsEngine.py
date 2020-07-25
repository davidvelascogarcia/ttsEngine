'''
 * ************************************************************
 *      Program: TTS Engine
 *      Type: Python
 *      Author: David Velasco Garcia @davidvelascogarcia
 * ************************************************************
 *
 * | INPUT PORT                           | CONTENT                                                 |
 * |--------------------------------------|---------------------------------------------------------|
 * | /ttsEngine/data:i                    | Input text to speech                                    |
 *
 * | OUTPUT PORT                          | CONTENT                                                 |
 * |--------------------------------------|---------------------------------------------------------|
 * | /ttsEngine/data:o                    | Mirror output text to speech                            |
 *
'''

# Libraries
import datetime
from gtts import gTTS
from io import BytesIO
import os
import platform
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play
import sys
import time
import yarp


print("**************************************************************************")
print("**************************************************************************")
print("                     Program: TTS Engine                                  ")
print("                     Author: David Velasco Garcia                         ")
print("                             @davidvelascogarcia                          ")
print("**************************************************************************")
print("**************************************************************************")

print("")
print("Starting system ...")
print("")

print("")
print("Loading TTS engine module ...")
print("")

print("")
print("Detecting system and release version ...")
print("")
systemPlatform = platform.system()
systemRelease = platform.release()

print("")
print("**************************************************************************")
print("Configuration detected:")
print("**************************************************************************")
print("")
print("Platform:")
print(systemPlatform)
print("Release:")
print(systemRelease)

print("")
print("")
print("**************************************************************************")
print("Initializing ttsEngine:")
print("**************************************************************************")
print("")
print("[INFO] Initializing ttsEngine ...")
print("")

# Initializing offline default engine
ttsEngineOffline = pyttsx3.init()

# Initializing online default engine
onlineTempAudioClip = BytesIO()

print("")
print("[INFO] TTS engine initialized correctly at " + str(datetime.datetime.now()) + ".")
print("")

print("")
print("**************************************************************************")
print("Loading TTS voices:")
print("**************************************************************************")
print("")
print("[INFO] Loading TTS system voices ...")
print("")

# Get system voices
systemVoices = ttsEngineOffline.getProperty('voices')

print("")
print("[INFO] System voices gotten correctly at " + str(datetime.datetime.now()) + ".")
print("")

print("")
print("**************************************************************************")
print("Voices configuration:")
print("**************************************************************************")
print("")
print("Setting tts voice ...")
print("")

# If systemPlatform is Linux
if str(systemPlatform) == "Linux":
    ttsEngineOffline.setProperty('voice', systemVoices[19].id)

# If systemPlatform is Windows
elif str(systemPlatform) == "Windows":
    ttsEngineOffline.setProperty('voice', systemVoices[1].id)

# If systemPlatform is Mac OS X
elif str(systemPlatform) == "Darwin":
    ttsEngineOffline.setProperty('voice', systemVoices[1].id)

# systemPlatform default voice
else:
    ttsEngineOffline.setProperty('voice', systemVoices[1].id)


print("")
print("[INFO] System TTS voice selected correctly at " + str(datetime.datetime.now()) + ".")
print("")

print("")
print("**************************************************************************")
print("YARP configuration:")
print("**************************************************************************")
print("")
print("Initializing YARP network ...")
print("")

# Init YARP Network
yarp.Network.init()

print("")
print("[INFO] Opening data input port with name /ttsEngine/data:i ...")
print("")

# Open ttsEngine input port
ttsEngine_inputPort = yarp.Port()
ttsEngine_inputPortName = '/ttsEngine/data:i'
ttsEngine_inputPort.open(ttsEngine_inputPortName)

# Create ttsEngine input data bottle
ttsEngineInputBottle = yarp.Bottle()

print("")
print("[INFO] Opening data output port with name /ttsEngine/data:o ...")
print("")

# Open ttsEngine output port
ttsEngine_outputPort = yarp.Port()
ttsEngine_outputPortName = '/ttsEngine/data:o'
ttsEngine_outputPort.open(ttsEngine_outputPortName)

# Create ttsEngine output data bottle
ttsEngineOutputBottle = yarp.Bottle()

print("")
print("[INFO] YARP configured correctly.")
print("")

# Variable to control speak loop
loopControlSpeak = 0

while int(loopControlSpeak) == 0:

    print("")
    print("**************************************************************************")
    print("Waiting for input TTS:")
    print("**************************************************************************")
    print("")
    print("[INFO] Waiting for input TTS text...")
    print("")

    # Receive ttsEngine text to speak
    ttsEngineInputBottle.clear()
    ttsEngine_inputPort.read(ttsEngineInputBottle)
    ttsText = ttsEngineInputBottle.toString()

    print("")
    print("**************************************************************************")
    print("Processing input request text:")
    print("**************************************************************************")
    print("")
    print("[INFO] Processing input request text ...")
    print("")

    # Clear string to remove ""
    ttsText = str(ttsText)
    ttsText = ttsText.replace('"','')

    # Print receive message
    print("")
    print("[RECEIVE] Receive: " + ttsText + " at " + str(datetime.datetime.now()) + ".")
    print("")

    # If ttsText it´s not void
    if str(ttsText) != "":

        print("")
        print("[INFO] Speaking TTS text ...")
        print("")

        # If internet connection it´s ok, use Google Assistant voice
        try:
            # Send request and get tts voice
            ttsEngineOnline = gTTS(str(ttsText), lang='es', slow=False)

            # Save into temporal file
            ttsEngineOnline.write_to_fp(onlineTempAudioClip)
            onlineTempAudioClip.seek(0)

            # Load temporal file with pydub to play
            ttsSpokenVoice = AudioSegment.from_file(onlineTempAudioClip)

            # Speak tts audio
            play(ttsSpokenVoice)

        # If internet connection it´s not ok use system offline default voice (Windows: SAPI5, Linux: MBrola, OS X: Siri)
        except:

            # Prepare text to say
            ttsEngineOffline.say(ttsText)

            # Speak the ttsText
            ttsEngineOffline.runAndWait()

        # Send text mirror ttsEngine_outputPort
        ttsEngineOutputBottle.clear()
        ttsEngineOutputBottle.addString("TTS Spoken:")
        ttsEngineOutputBottle.addString(ttsText)
        ttsEngine_outputPort.write(ttsEngineOutputBottle)

        # If receive key word exit from loopControlSpeak
        if str(ttsText) == "exit":

            # Set loopControlSpeak
            loopControlSpeak = 1

            # Say exit message
            ttsEngineOffline.say("Mensaje recibido, apagando el motor de habla")
            ttsEngineOffline.runAndWait()

        # Clear online default engine clip
        onlineTempAudioClip = BytesIO()

    # If emply ttsText
    else:
        print("")
        print("[ERROR] Error, empty message.")
        print("")

# Close YARP ports
print("[INFO] Closing YARP ports ...")
ttsEngine_inputPort.close()
ttsEngine_outputPort.close()

print("")
print("")
print("**************************************************************************")
print("Program finished")
print("**************************************************************************")
print("")
print("ttsEngine program finished correctly.")
print("")
