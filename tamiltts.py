#import re
import wave
import pyaudio
import time
from pydub import AudioSegment
import io

class TextToSpeech:
    CHUNK = 1024

    def __init__(self, words_pron_dict: str = 'tamil-letters.txt'):
        self._l = {}
        self._load_words(words_pron_dict)

    def _load_words(self, words_pron_dict: str):
        file = io.open(words_pron_dict, mode="r", encoding="utf-8")
        for line in file:
            if not line.startswith(';;;'):
                keyval = line.split()
                if (len(keyval) == 2):
                    self._l[keyval[0]] = keyval[1].rstrip()

    def get_pronunciation(self, str_input):
        for word in str_input.split():
            l = len(word)
            i = 0
            word_audio = None
            first_letter = 1
            while i < l:
                letter = word[i]
                prevLetter = ''
                if ((i + 1) < l and word[i + 1] in ['்', 'ா', 'ி', 'ீ', 'ு', 'ூ', 'ெ', 'ே', 'ை', 'ொ', 'ோ', 'ௌ']):
                    letter = letter + word[i + 1]
                    i += 1
                    prevLetter = word[i-3]+word[i-2]
                elif (i-2 > 0):
                    prevLetter = word[i-2]+word[i-1]
                #print (letter)
                if letter in self._l:
                    soundfile = self._l[letter]
                    if (soundfile[0] == 't' and soundfile[1] != 'r' and soundfile[1] != 't' and prevLetter != 'ட்'): 
                        if (soundfile[1] != 'h' or (soundfile[1] == 'h' and len(soundfile) > 2 and prevLetter != 'த்')):
                            soundfile = soundfile.replace('t', 'd')
                    elif (soundfile == 'mm' and i+1 < l):
                        soundfile = 'mm_long'
                    elif (soundfile == 'maa' and i+1 == l):
                        soundfile = 'maa_long'
                    elif (soundfile == 'kai' and prevLetter != 'ங்'):
                        soundfile = 'hai'
                    elif (soundfile == 'chaa' and prevLetter == 'ஞ்'):
                        soundfile = 'jaa'
                    elif (soundfile == 'ndh' and word[i+1] == 'ந'):
                        soundfile = 'nn'
                    print(letter, self._l[letter], prevLetter, soundfile, i, l)
                    sound = AudioSegment.from_wav("sounds3/" + soundfile + ".wav")
                    if (first_letter == 1):
                        word_audio = sound
                        first_letter = 0
                    else:
                        word_audio += sound
                i = i + 1
            word_audio.export("temp.wav", format="wav")
            _play_audio()
            time.sleep(0.25)

def _play_audio():
    try:
        wf = wave.open("temp.wav", 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(TextToSpeech.CHUNK)

        while data:
            stream.write(data)
            data = wf.readframes(TextToSpeech.CHUNK)

        stream.stop_stream()
        stream.close()

        p.terminate()
        return
    except:
        pass

if __name__ == '__main__':
    tts = TextToSpeech()
    while True:
        tts.get_pronunciation(input('Enter a word or phrase: '))
