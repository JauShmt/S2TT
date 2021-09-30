import tkinter as tk
from tkinter.filedialog import askopenfilename
import ibm_cloud_sdk_core
from ibm_watson import SpeechToTextV1
import json
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pandas import json_normalize
from ibm_watson import LanguageTranslatorV3

# API
  # - s2t : SpeechToText
url_s2t = "https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/079804c4-c237-49f9-b65b-5d749d5ff502"
iam_apikey_s2t = "1gp0cp4UXZql1k0JZ3ihVuB-nPUUxKe28l5zu4f_ohiv"
authenticator_st2 = IAMAuthenticator(iam_apikey_s2t)
s2t = SpeechToTextV1(authenticator=authenticator_st2)
s2t.set_service_url(url_s2t)

  # -  lt : LanguageTranslator
url_lt = 'https://api.eu-de.language-translator.watson.cloud.ibm.com/instances/c4991030-b223-49f7-9c04-1abf8862ad62'
apikey_lt = 'MfIQ5EpLlm28Bitb17l358p8J8U3eumg-5BEMGY7bMjS'
version_lt = '2018-05-01'
authenticator_lt = IAMAuthenticator(apikey_lt)
language_translator = LanguageTranslatorV3(version=version_lt, authenticator=authenticator_lt)
language_translator.set_service_url(url_lt)

# Language handling variables
s2t_lg = 'en-US_BroadbandModel'
language_list = ['En', 'Fr']
language_source = 'en'
target_lg = 'en'

# GUI Setup
main_window = tk.Tk()

lb1 = tk.Label(main_window, text='Set speech language: ', font=40)
lb1.grid(row=2, column=0)

# speech language selection list :
SelectedLg = tk.StringVar(main_window)
SelectedLg.set(language_list[0])
LgList = tk.OptionMenu(main_window, SelectedLg, *language_list)
LgList.grid(row=2, column=1)

ent1 = tk.Entry(main_window, font=40)
ent1.grid(row=2, column=2)

TextArea = tk.Text(main_window, wrap=tk.WORD)
TextArea.grid(row=3, column=0, columnspan=4)

# translation target language button & selection list :
lb2 = tk.Label(main_window, text='Set translation target language: ', font=40)
lb2.grid(row=4, column=0)

Selected_targ_lg = tk.StringVar(main_window)
Selected_targ_lg.set(language_list[0])
Lgtarg = tk.OptionMenu(main_window, Selected_targ_lg, *language_list)
Lgtarg.grid(row=4, column=1)

# Translation text display area :
TranslateArea = tk.Text(main_window, wrap=tk.WORD)
TranslateArea.grid(row=5, column=0, columnspan=4)


# File treatment function & button
def browsefunc():
    global final_result_s2t

    filename =askopenfilename(filetypes=(("Audio files", "*.mp3 *.ogg *.mpeg *.wav *.webm"),("All files","*.*")))
    ent1.insert(tk.END, filename)

    print('browse file')

    try:
        with open(filename, mode="rb") as wav:
            try:
                print('st2_lg=' + s2t_lg)
                print('langue source=' + language_source)
                response = s2t.recognize(audio=wav, model=s2t_lg)
            except ibm_cloud_sdk_core.api_exception.ApiException as e:
                TextArea.insert(tk.INSERT, '-> ERROR File type is not supported')
                print(e)
                return

            s2t_responses_list = []
            for responses in response.result['results']:
                s2t_responses_list.append(responses['alternatives'][0]['transcript'] + '\n')
            s2t_responses_list.append('\n')

        final_result_s2t = '\n'.join(s2t_responses_list)
        TextArea.insert(tk.INSERT, final_result_s2t)
    except FileNotFoundError as e:
        TextArea.insert(tk.INSERT, '[ERROR No file selected]\n')
        print(e)


b1 = tk.Button(main_window, text="File Path", font=40, command=browsefunc)
b1.grid(row=2, column=3)


# Translation function & button
def translate():
    global TranslateArea
    global final_result_s2t
    model = language_source + '-' + target_lg
    print(model)
    try:
        tl_response = language_translator.translate(text=TextArea.get('1.0', tk.END), model_id=model)
        tl_result = tl_response.get_result()['translations'][0]['translation']
        TranslateArea.delete('1.0', tk.END)
        TranslateArea.insert(tk.INSERT, tl_result)
    except ibm_cloud_sdk_core.api_exception.ApiException as e:
        TranslateArea.delete('1.0', tk.END)
        TranslateArea.insert(tk.INSERT, 'Error 404: Selected translation language same as speech language')
        print(e)
        return


b2 = tk.Button(main_window, text="Translate Text", font=40, command=translate)
b2.grid(row=4, column=2)


# SpeechToText & translation languages handling functions :
  # - set_speech_lg : handle SpeechToText & translation source language

def set_speech_lg(*args):
    global s2t_lg
    global language_source

    print('set speech lg = ' + SelectedLg.get())

    if SelectedLg.get() == 'Fr':
        s2t_lg = 'fr-FR_BroadbandModel'
        language_source = 'fr'
    elif SelectedLg.get() == 'En':
        s2t_lg = 'en-US_BroadbandModel'
        language_source = 'en'


  # - set_targ_lg : handle LanguageTranslator target language
def set_targ_lg(*args):
    global target_lg
    print('change target')
    if Selected_targ_lg.get() == 'Fr':
        target_lg = 'fr'
    elif Selected_targ_lg.get() == 'En':
        target_lg = 'en'
    print('target lang = ' + target_lg)


# GUI links setup
SelectedLg.trace('w', set_speech_lg)
Selected_targ_lg.trace('w', set_targ_lg)

# GUI START
main_window.mainloop()
