import requests
import os
import subprocess
from subprocess import PIPE,Popen
import sys
import platform
from random import randint


def owl_speak(input_text):
    url_path = 'http://localhost:59125/process?INPUT_TYPE=TEXT&OUTPUT_TYPE=AUDIO&INPUT_TEXT={0}&OUTPUT_TEXT=&effect_Volume_selected=&effect_Volume_parameters=amount%3A2.0%3B&effect_Volume_default=Default&effect_Volume_help=Help&effect_TractScaler_selected=&effect_TractScaler_parameters=amount%3A1.5%3B&effect_TractScaler_default=Default&effect_TractScaler_help=Help&effect_F0Scale_selected=&effect_F0Scale_parameters=f0Scale%3A2.0%3B&effect_F0Scale_default=Default&effect_F0Scale_help=Help&effect_F0Add_selected=&effect_F0Add_parameters=f0Add%3A50.0%3B&effect_F0Add_default=Default&effect_F0Add_help=Help&effect_Rate_selected=&effect_Rate_parameters=durScale%3A1.5%3B&effect_Rate_default=Default&effect_Rate_help=Help&effect_Robot_selected=&effect_Robot_parameters=amount%3A100.0%3B&effect_Robot_default=Default&effect_Robot_help=Help&effect_Whisper_selected=&effect_Whisper_parameters=amount%3A100.0%3B&effect_Whisper_default=Default&effect_Whisper_help=Help&effect_Stadium_selected=&effect_Stadium_parameters=amount%3A100.0&effect_Stadium_default=Default&effect_Stadium_help=Help&effect_Chorus_selected=&effect_Chorus_parameters=delay1%3A466%3Bamp1%3A0.54%3Bdelay2%3A600%3Bamp2%3A-0.10%3Bdelay3%3A250%3Bamp3%3A0.30&effect_Chorus_default=Default&effect_Chorus_help=Help&effect_FIRFilter_selected=&effect_FIRFilter_parameters=type%3A3%3Bfc1%3A500.0%3Bfc2%3A2000.0&effect_FIRFilter_default=Default&effect_FIRFilter_help=Help&effect_JetPilot_selected=&effect_JetPilot_parameters=&effect_JetPilot_default=Default&effect_JetPilot_help=Help&HELP_TEXT=&exampleTexts=&VOICE_SELECTIONS=cmu-slt-hsmm%20en_US%20female%20hmm&AUDIO_OUT=WAVE_FILE&LOCALE=en_US&VOICE=cmu-slt-hsmm&AUDIO=WAVE_FILE'.format(input_text)
    r = requests.get( url_path )

    if platform.system() == 'Windows':
        with open(os.path.join('D://','owlspeak.wav'),'wb') as f:
            f.write(r.content)
        subprocess.call('"C://Program Files (x86)//Windows Media Player//wmplayer.exe" /play /close /close "D://owlspeak.wav"')

        # import winsound
        # winsound.PlaySound('D://owlspeak.wav', winsound.SND_FILENAME)
    else :
        with open(os.path.join('/tmp', 'owlspeak.wav'), 'wb') as f:
            f.write(r.content)
        Popen(["aplay", "-f", "dat", "/tmp/owlspeak.wav"])


def play_mp3(mp3_file_name,play_random=False):
    location_to_mp3 = ''
    song_to_play = ''
    if play_random:
        path = os.path.join('./songs', '')
        songs = os.listdir(path)
        print(songs)
        song_to_play = songs[randint(0,len(songs))]
        print(song_to_play)
    else:
        path = os.path.join('./songs', mp3_file_name)
        song_to_play = path

    if song_to_play is None or song_to_play == '':
        owl_speak('sorry, the song you requested does not exists')

    mp3_cmd = ['omxplayer', '-o', 'local',song_to_play]
    Popen(mp3_cmd)


if __name__ == "__main__":
    play_mp3('',True)
    play_mp3('national_anthem.mp3',False)