class LanguageManager:
    st2_lg_EN = 'en-US_BroadbandModel'
    st2_lg_FR = 'fr-FR_BroadbandModel'

    def __init__(self):
        self.s2t_lg = LanguageManager.st2_lg_EN
        self.language_list = ['En', 'Fr']
        self.language_source = 'en'
        self.target_lg = 'en'
        self.window = None
        self.setTranslationModel()

    def getManagedLanguages(self):
        return self.language_list

    def getManagedLanguage(self, index):
        return self.language_list[index]

    def setTranslationModel(self):
        self.translationModel = self.language_source + '-' + self.target_lg
        print('new translation model :'+self.translationModel)

    def linkToWindow(self, window):
        self.window = window

    def set_targ_lg(self, *args):
        print('change target :')
        if self.window is not None:
            Selected_targ_lg = self.window.GetSelected_targ_lg()
            print('gui taget selection ='+Selected_targ_lg)
            if Selected_targ_lg == 'Fr':
                self.target_lg = 'fr'
            elif Selected_targ_lg == 'En':
                self.target_lg = 'en'
            self.setTranslationModel()
        else:
            print('Error GUI link not set')

        print('target lang = '+self.target_lg)

    def set_speech_lg(self, *args):
        print('change speech lang :')
        if self.window is not None:
            SelectedLg = self.window.GetSelectedLg()
            if SelectedLg == 'Fr':
                self.s2t_lg = LanguageManager.st2_lg_FR
                self.language_source = 'fr'
            elif SelectedLg == 'En':
                self.s2t_lg = LanguageManager.st2_lg_EN
                self.language_source = 'en'
            self.setTranslationModel()
            print('speech lang = '+self.s2t_lg)
        else:
            print('Error GUI link not set')
