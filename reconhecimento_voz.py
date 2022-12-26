# -*- coding: utf-8 -*-
"""
Created on Fri May  1 19:22:15 2020

@author: aserpa
"""

import speech_recognition as sr
import win32com.client as wincl
import time
from googletrans import Translator as tl


#Define a saida usando o audio do WIndows
speak = wincl.Dispatch("SAPI.SpVoice")
vcs = speak.GetVoices()


#Define o Microfone
mic = sr.Microphone()

#Entrada do Mic
mic.device_index = 1

#Iniciando
speak.Voice
speak.SetVoice(vcs.Item (0))   #Usando portugues
speak.Speak('Olá, eu sou Judiiti!')#, a tradutora ambulante!')
#speak.Speak('Agora aprendi Espanhol também')
speak.Speak('VocÊ quer traduzir para Inglês ou Espanhol?')
#speak.Speak('Qual a palavra')# ou frase a ser traduzida do Português para o Inglês?')


#Usando o Mic como fonte e jogando o audio na variavel audio
with mic as source:
    sr.Recognizer().adjust_for_ambient_noise(source)
    audio = sr.Recognizer().listen(source)
    

#time.sleep(3)
#Usando o Google para reconhecimento de TTS
vGrava = sr.Recognizer().recognize_google(audio, language='pt-BR')    
#vGrava = sr.Recognizer().recognize_google(audio, language='en-US')   #Ingles


#Define o Idioma
if vGrava == 'espanhol':
    vLang = 'es'
elif (vGrava == 'ingles' or vGrava == 'inglês'):
    vLang = 'en'


print(vGrava)
print(vLang)

speak.Speak('Ok, entendi. Vamos traduzir para o ' + vGrava)
speak.Speak('Qual palavra?')

#Usando o Mic como fonte e jogando o audio na variavel audio
with mic as source:
    sr.Recognizer().adjust_for_ambient_noise(source)
    audio = sr.Recognizer().listen(source)
    

#Usando o Google para reconhecimento de TTS
vGrava = sr.Recognizer().recognize_google(audio, language='pt-BR')    #Portugues
#vGrava = sr.Recognizer().recognize_google(audio, language='en-US')   #Ingles

print('Palavra a ser traduzida: '+vGrava)

#Faz a tradução
vTrans = tl(service_urls=['translate.google.com.br']).translate(vGrava, src='pt', dest=vLang)

print('Tradução: '+vTrans.text)


#time.sleep(2)
#Retorna o valor traduzido na voz definida usando ingles como saida
speak.Voice
speak.SetVoice(vcs.Item (1))
speak.Speak(vTrans.text)















