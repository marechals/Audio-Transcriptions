# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 07:22:28 2019

@author: ASUS
"""

from pydub import AudioSegment
import speech_recognition as sr 
from pydub.effects import normalize
import os
from tqdm import tqdm

#%%
#con audiosegment se convierte el formato a wav

#una vez hecha la muestra de ruido en un segundo en el que haya silencio

# en algunas es mejor no limpiar el ruido, probar con y sin ruido, limpiar de ruido con la lbreria sox en el cmd de anaconda hacer el perfil de ruido con sox ruido.wav -n noiseprof noise.prof 
#luego limpiar el audio con sox Entrevista_1_Coventry_Policy_norm_16k.wav Entrevista_1_Coventry_Policy_norm_16k_clean.wav noisered noise.prof 0.21  este ultimo parametro entre 0.2 y 0.3
#e puede haccer el trim de ejemplo de ruido con sox audio.wav noise-audio.wav trim 0 0.900 esto es : sox in.ext out.ext trim {start: s.ms} {duration: s.ms}
#sirvio mas solo bajar el frame_rate a 16000

#con la libreria ffmpeg se divide el audio original en pequeños fragmentos
#este es el codigo para partir en fragmentos en la cmd de anacodna ffmpeg -i William_norm_16k.wav -f segment -segment_time 20 -c copy parts/out%05d.wav la ultima parte significa que en la carpeta parts/palabra out y 5 digitos seguidos de la extencion .wav
#se sacan algunas estadisticas de los audios para comprobar su caldiad o almenos saber algo sobre su calidad
#se crea la funcion para transcribir, hace uso de la aip de google
#se crea la función para iterar en los audios con un seudocontrol de errores
#limpiar el archivo de texto de comillas
#correccion manual de la transcripcion

# convert m4a file to wav 
                                                       
sound = AudioSegment.from_file("William.mp3", "mp3")
sound.export("William.wav", format="wav")

    #%%                                                  
entrevista = AudioSegment.from_file("William.wav", "wav")

#quitar los ruidos iniciales dejando los segundos a partir de los cuales no estan, en este caso a partir
#del segundo 2 
entrevista=entrevista[:]

#normalizar el volumen
entrevista_norm = normalize(entrevista)
# Create a new wav file with adjusted frame rate
entrevista_norm_16k = entrevista_norm.set_frame_rate(16000)
entrevista_norm_16k = entrevista_norm_16k + 5

entrevista_norm_16k.export("William_norm_16k.wav", format="wav")
#%%
#encontrar un segundo en el cual haya silencio para establecer como ruido, en este caso min 8 54 al 8 55

#entrevista=entrevista[29000:30000]
#ruido.export("ruido.wav", format="wav")

recognizer=sr.Recognizer()
entrevista_ruidosa= sr.AudioFile("out00033.wav")
with entrevista_ruidosa as source:
    recognizer.adjust_for_ambient_noise(source,duration=0.2)
    entrevista_ruidosa_audio=recognizer.record(source)
    
trans=recognizer.recognize_google(entrevista_ruidosa_audio,language="es-CO")
print(trans) 
    
#%%

def show_pydub_stats(filename):
  """Returns different audio attributes related to an audio file."""
  # Create AudioSegment instance
  audio_segment = AudioSegment.from_file(filename)
  
  # Print audio attributes and return AudioSegment instance
  print(f"Channels: {audio_segment.channels}")
  print(f"Sample width: {audio_segment.sample_width}")
  print(f"Frame rate (sample rate): {audio_segment.frame_rate}")
  print(f"Frame width: {audio_segment.frame_width}")
  print(f"Length (ms): {len(audio_segment)}")
  return audio_segment

# Try the function
print(show_pydub_stats("out00000.wav"))


#%%

#separar los canales en algunos casos vienen varios canales
# Split stereo phone call and check channels
channels = entrevista_norm_16k.split_to_mono()
print(f"Split number channels: {channels[0].channels}, {channels[1].channels}")

# Save new channels separately
entrevista_norm_16k_channel_1 = channels[0]
entrevista_norm_16k_channel_2 = channels[1]

entrevista_norm_16k_channel_1.export("Laura_norm_16k_chan_1.wav", format="wav")
entrevista_norm_16k_channel_2.export("Laura_norm_16k_chan_2.wav", format="wav")
#%%

def transcribe_audio(filename):
  """Takes a .wav format audio file and transcribes it to text."""
  # Setup a recognizer instance
  recognizer = sr.Recognizer()
  recognizer.energy_threshold = 100
  # Import the audio file and convert to audio data
  audio_file = sr.AudioFile(filename)
  with audio_file as source:
      #utiliza la funcion nativa para el ruido
    recognizer.adjust_for_ambient_noise(source,duration=0.2)
    audio_data = recognizer.record(source)
  
  # Return the transcribed text
  return recognizer.recognize_google(audio_data,language="es-CO")
  
print(transcribe_audio('out00007.wav'))
#print(transcribe_audio('Entrevista_1_parte_2_Coventry_Policy.wav'))
#print(transcribe_audio('out0000.wav'))
#%%
folder = sorted(os.listdir('C:/Users/ASUS/Desktop/Entrevistas_Javeriana/parts/'))
text_list = []
def create_text_list(folder):
  # Create empty list
  
  # Go through each file and show progress tqdm
  for file in tqdm(folder):
    try:
      # Make sure the file is .wav
      if file.endswith(".wav"):
          print(f"Transcribing file: {file}...")
      
      # Transcribe audio and append text to list
          text = transcribe_audio(file)
          text_list.append(text)
          with open("transcripcion.txt", "a+") as file:
              file.write(str(text_list))
    except:
        pass
  return text_list
    
  print(text_list)


    
create_text_list(folder)


