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
                keyval = line.split()
                if (len(keyval) == 2):
                    self._l[keyval[0]] = keyval[1].rstrip()

    def get_pronunciation(self, str_input):
        uyirmei = {'ா': 'ஆ', 'ி': 'இ', 'ீ': 'ஈ', 'ு': 'உ', 'ூ': 'ஊ', 'ெ': 'எ', 'ே': 'ஏ', 'ை': 'ஐ', 'ொ': 'ஒ', 'ோ': 'ஓ',
                   'ௌ': 'ஔ'}
        delay = 0.1
        for word in str_input.split():
            l = len(word)
            i = 0
            while i < l:
                letter = word[i]
                if ((i + 1) < l and word[i + 1] in ['்', 'ா', 'ி', 'ீ', 'ு', 'ூ', 'ெ', 'ே', 'ை', 'ொ', 'ோ', 'ௌ']):
                    letter = letter + word[i + 1]
                    i += 1
                if letter in self._l:
                    print(letter)
                    _thread.start_new_thread(TextToSpeech._play_audio, (self._l[letter], delay,))
                i = i + 1
                delay += 0.15
            delay += 0.75

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
