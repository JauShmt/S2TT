import tkinter as tk
from tkinter.filedialog import askopenfilename

import ibm_cloud_sdk_core


class MainWindow:

    def __init__(self, languageManager):
        self.languageManager = languageManager
        self.filename = ''

        self.main_window = tk.Tk()

        self.lb1 = tk.Label(self.main_window, text='Set speech language: ', font=40)
        self.lb1.grid(row=2, column=0)

        # speech language selection list :
        self.SelectedLg = tk.StringVar(self.main_window)
        self.SelectedLg.set(languageManager.getManagedLanguage(0))
        self.LgList = tk.OptionMenu(self.main_window, self.SelectedLg, *languageManager.language_list)
        self.LgList.grid(row=2, column=1)

        self.ent1 = tk.Entry(self.main_window, font=40)
        self.ent1.grid(row=2, column=2)

        self.b1 = tk.Button(self.main_window, text="Select file", font=40, command=self.getTextFromAPI)
        self.b1.grid(row=2, column=3)

        self.TextArea = tk.Text(self.main_window, wrap=tk.WORD)
        self.TextArea.grid(row=3, column=0, columnspan=4)

        # translation target language button & selection list :
        self.lb2 = tk.Label(self.main_window, text='Set translation target language: ', font=40)
        self.lb2.grid(row=4, column=0)

        self.Selected_targ_lg = tk.StringVar(self.main_window)
        self.Selected_targ_lg.set(languageManager.getManagedLanguage(0))
        self.Lgtarg = tk.OptionMenu(self.main_window, self.Selected_targ_lg, *languageManager.language_list)
        self.Lgtarg.grid(row=4, column=1)

        self.b2 = tk.Button(self.main_window, text="Translate Text", font=40, command=self.translate)
        self.b2.grid(row=4, column=2)

        # Translation text display area :
        self.TranslateArea = tk.Text(self.main_window, wrap=tk.WORD)
        self.TranslateArea.grid(row=5, column=0, columnspan=4)

        # API links
        # set later with linkToS2tApi & linkToTranslationApi
        self.s2t = None
        self.translator = None

    def GetSelected_targ_lg(self):
        return self.Selected_targ_lg.get()

    def GetSelectedLg(self):
        return self.SelectedLg.get()

    def getTextAreaContent(self):
        return self.TextArea.get('1.0', tk.END)

    def setTranslationContent(self, content):
        self.TranslateArea.delete('1.0', tk.END)
        self.TranslateArea.insert(tk.INSERT, content)

    def linkToS2tApi(self, s2t):
        self.s2t = s2t
        self.SelectedLg.trace('w', self.languageManager.set_speech_lg)
        self.Selected_targ_lg.trace('w', self.languageManager.set_targ_lg)

    def linkToTranslationApi(self, lt):
        self.translator = lt

    def insertTextArea(self, text):
        print('-Insertion in TextArea')
        self.TextArea.insert(tk.INSERT, text)

    def getFilename(self):
        self.filename = askopenfilename(
            filetypes=(("Audio files", "*.mp3 *.ogg *.mpeg *.wav *.webm"), ("All files", "*.*")))
        self.ent1.insert(tk.END, self.filename)

    def getTextFromAPI(self):

        print('Get text form TextToSpeech')

        if self.s2t is None:
            print('Error API : s2t link not set')
            return

        try:
            self.getFilename()
            with open(self.filename, mode="rb") as wav:
                try:
                    response = self.s2t.recognizeTextInFile(
                        self.filename, self.languageManager.s2t_lg, self
                    )
                    self.TextArea.insert(tk.INSERT, response)
                except ibm_cloud_sdk_core.api_exception.ApiException as e:
                    self.TextArea.insert(tk.INSERT, '-> ERROR File type is not supported')
                    print(e)
                    return
        except FileNotFoundError as e:
            print(e)

    def translate(self):
        if self.translator is None:
            print('Error API : translation link not set')
            return

        self.translator.translate(self.languageManager.translationModel, self)

    def run(self):
        self.main_window.mainloop()