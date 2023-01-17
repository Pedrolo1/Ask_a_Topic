# THIS FILE WILL HAVE ALL THE FUNCTIONS RELATED TO TRANSCRIPTS DOWNLOADING AND PROCESSING

import os
import whisper
import torch
from tqdm import tqdm

# agnostic device
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# a funcion that takes a path of a mp4 file and return the transcript
def audio_to_transcript(path, model = 'small'):
    model = whisper.load_model(model).to(device)
    
    transcription = model.transcribe(path)
    
    # vamos a coger la transcripcion y vamos addear el titulo del video al inicio un una nueva linea
    nombre = os.path.basename(path).split('.')[0]
    text_prepare = nombre + ':\n' + transcription['text']
    
    # save this transcript in a file txt
    with open(path.split('.')[0] + '.txt', 'w') as f:
        f.write(text_prepare)
        
    # now delete the mp4 file
    os.remove(path)
    
    # return the path of the transcript
    return path.split('.')[0] + '.txt'

# a funcion that takes a path of a folder and return a list of transcripts
def folder_to_transcripts(path, model = 'small'):
    lista_paths = os.listdir(path)
    path_transcripts = []
    for file in tqdm(lista_paths):
        if file.endswith(".mp4"):
            print(f"Transcribing {file}...")
            path_transcripts.append(audio_to_transcript(os.path.join(path, file), model))
            
    return path_transcripts