# Written by Alex I. Ramirez @alexram1313
# arcompware.com
import re
import wave
import pyaudio
import _thread
import time
import io

class TextToSpeech:
    CHUNK = 1024

    def __init__(self, words_pron_dict: str = 'tamil-letters.txt'):
        self._l = {}
        self._load_words(words_pron_dict)

    def _load_words(self, words_pron_dict: str):
        file = io.open(words_pron_dict, mode="r", encoding="utf-8")
        # with open(words_pron_dict, 'r') as file:
        for line in file:
            if not line.startswith(';;;'):
                key, val = line.split('  ', 2)
                self._l[key] = val.rstrip()

    def get_pronunciation(self, str_input):
        uyirmei = {'ா': 'ஆ', 'ி': 'இ', 'ீ': 'ஈ', 'ு': 'உ', 'ூ': 'ஊ', 'ெ': 'எ', 'ே': 'ஏ', 'ை': 'ஐ', 'ொ': 'ஒ', 'ோ': 'ஓ',
                   'ௌ': 'ஔ'}
        delay = 0.1
        for word in str_input.split():
            list_pron = []
            l = len(word)
            i = 0
            while i < l:
                letter = word[i]
                letter2 = ''
                if ((i+1) < l and word[i+1] == '்'):
                    letter = letter + word[i+1]
                    i += 1
                elif ((i+1) < l and word[i + 1] in ['ா', 'ி', 'ீ', 'ு', 'ூ', 'ெ', 'ே', 'ை', 'ொ', 'ோ', 'ௌ']):
                    letter = letter + '்'
                    letter2 = uyirmei[word[i+1]]
                    i += 1
                elif (word[i] in ['க', 'ங', 'ச', 'ஞ', 'ட', 'ண', 'த', 'ந', 'ப', 'ம', 'ய', 'ர', 'ல', 'வ', 'ள', 'ழ', 'ற', 'ன']):
                    letter = letter + '்'
                    letter2 = 'அ'
                if letter in self._l:
                    list_pron.append(self._l[letter])
                if letter2 in self._l:
                    list_pron.append(self._l[letter2])
                i = i + 1
            print(list_pron)
            for pron in list_pron:
                _thread.start_new_thread(TextToSpeech._play_audio, (pron, delay,))
                delay += 0.2
            delay += 0.5

    def _play_audio(sound, delay):
        try:
            time.sleep(delay)
            wf = wave.open("sounds/female/" + sound + ".wav", 'rb')
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
