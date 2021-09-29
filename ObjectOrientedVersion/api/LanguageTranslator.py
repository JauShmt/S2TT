import ibm_cloud_sdk_core
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import LanguageTranslatorV3


class LanguageTranslator:

    def __init__(self):
        self.url = 'https://api.eu-de.language-translator.watson.cloud.ibm.com/instances/c4991030-b223-49f7-9c04-1abf8862ad62'
        self.apikey = 'MfIQ5EpLlm28Bitb17l358p8J8U3eumg-5BEMGY7bMjS'
        self.version = '2018-05-01'
        self.authenticator = IAMAuthenticator(self.apikey)
        self.language_translator = LanguageTranslatorV3(version=self.version, authenticator=self.authenticator)
        self.language_translator.set_service_url(self.url)

    def translate(self, model, window):
        print('translation : '+model)
        try:
            tl_response = self.language_translator.translate(text=window.getTextAreaContent(), model_id=model)
            tl_result = tl_response.get_result()['translations'][0]['translation']

            window.setTranslationContent(tl_result)
        except ibm_cloud_sdk_core.api_exception.ApiException as e:
            window.setTranslationContent('Error 404: Selected translation language same as speech language')
            print(e)
