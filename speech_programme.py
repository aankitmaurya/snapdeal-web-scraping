# run these commands to import all libraries
# sudo pip install SpeechRecognition
# sudo apt-get install python-pyaudio python3-pyaudio
# pip install google-api-python-client



import speech_recognition as sr
recording = sr.Recognizer()
with sr.Microphone() as source:
	recording.adjust_for_ambient_noise(source)
	print("Please Say something:")
	audio = recording.listen(source)
	print("time up")
try:
	# print("You said: \n" + recording.recognize_google(audio))
	a = recording.recognize_google(audio)
	print("=============",a)
	if (a == "Swami"):
		print("yes you are right")
	else:
		print("not recognised")
except Exception as e:
   print(e)
