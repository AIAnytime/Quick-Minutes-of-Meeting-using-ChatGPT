import subprocess
import whisper
import openai
import os
import sys
from fastapi import FastAPI, File, UploadFile 
import aiofiles

openai.api_key = ""

model = whisper.load_model("base")

app = FastAPI()

def video_to_audio(video_file):
    audio_file = "input_audio.mp3"
    subprocess.call(["ffmpeg", "-y", "-i", video_file, audio_file], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    return audio_file

def audio_to_transcript(audio_file):
    result = model.transcribe(audio_file)
    transcript = result["text"]
    return transcript

def MoM_generation(prompt):
    response = openai.Completion.create(model="text-davinci-003",
                                        prompt= "Can you generate the Minute of Meeting in form of bullet points for the below transcript?\n"+prompt, 
                                        temperature=0.7, 
                                        max_tokens=256, 
                                        top_p=1,
                                        frequency_penalty=0, 
                                        presence_penalty=0)
    return response['choices'][0]['text']

audio_file = video_to_audio('interview.mp4')
transcript = audio_to_transcript(audio_file)
final_result = MoM_generation(transcript)

print(final_result)


