from controllers.LanguageManager import LanguageManager
from api.SpeechToText import SpeechToTextAPI
from api.LanguageTranslator import LanguageTranslator
from GUI.MainWindow import MainWindow


# Creation of the processing objects
LangManager = LanguageManager()
st2 = SpeechToTextAPI(LangManager)
lt = LanguageTranslator()

# Creation of the GUI object
main_window = MainWindow(LangManager)

# Link the window to the Language manager and API objects
LangManager.linkToWindow(main_window)
main_window.linkToS2tApi(st2)
main_window.linkToTranslationApi(lt)

# Start the gui
main_window.run()
