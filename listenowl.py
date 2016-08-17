from subprocess import Popen,PIPE
import owlspeak
import announcements
voice_commands = [
[['wise', 'owlie'],'greeting'],
[['what','weather'],'weather_info'],
[['traffic','office'],'traffic_info'],
[['play','song'],'play_song'],
[['tell','news'],'play_news'],
[['something', 'new'],'play_trivia'],
[['tell','story'],'play_story'],
[['are', 'you'],'play_im_fine'],
[['play','national'],'play_anthem'],
]
def identify_words():
    pass

def speak_spoken_words():
    pocket_sphinx_cmd = ['pocketsphinx_continuous','-hmm', '/usr/local/share/pocketsphinx/model/en-us/en-us',
                         '-lm','/home/pi/Downloads/wiseowl/4647.lm',
                         '-dict', '/home/pi/Downloads/wiseowl/4647.dic',
                         '-samprate','16000/8000/48000',
                         '-adcdev', 'plughw:0,0',
                         '-inmic', 'yes',
                         '-logfn','/dev/null'
                         ]

    #pocket_sphinx_cmd = ['cmd']

    exe_cmd = ''
    with Popen(pocket_sphinx_cmd, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        print("---------- LISTENING ----------")
        for line in p.stdout:

            print(line, end='')
            line = line.replace('\n','').lower()
            for cmd in voice_commands:
                lset = (set(line.split(' ')))
                cset = (set(cmd[0]))
                intersection_len = (len(lset.intersection(cset)))
                #print(lset,cset,intersection_len)
                if intersection_len == 2:
                    print("---------MATCH FOUND-----------")

                    exe_cmd = cmd[1]
                    print(exe_cmd)
                    br = True
                    p.kill()
                    perform_cmd(exe_cmd)
                    return



def perform_cmd(exe_cmd):
    if exe_cmd == 'greeting':
        owlspeak.owl_speak(announcements.play_greeting())
    elif exe_cmd == 'weather_info':
        owlspeak.owl_speak(announcements.play_weather_info())
    elif exe_cmd == 'traffic_info':
        owlspeak.owl_speak(announcements.play_traffic_info('to_office'))
    elif exe_cmd == 'play_song':
        owlspeak.play_mp3('',True)
    elif exe_cmd == 'play_news':
        owlspeak.owl_speak(announcements.play_top_news())
    elif exe_cmd == 'play_trivia':
        owlspeak.owl_speak(announcements.play_trivia())
    elif exe_cmd == 'play_story':
        owlspeak.owl_speak(announcements.play_story())
    elif exe_cmd == 'play_im_fine':
        owlspeak.owl_speak(announcements.play_im_fine())
    elif exe_cmd == 'play_anthem':
        owlspeak.play_mp3('national_anthem.mp3',False)

if __name__ == "__main__":
    #speak_spoken_words()

    line = 'play some song'

    for cmd in voice_commands:
        lset  = (set(line.split(' ')))
        cset = (set(cmd[0]))
        intersection_len = (len(lset.intersection(cset)))
        if intersection_len == 2:
            perform_cmd(cmd[1])

