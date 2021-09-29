import ibm_cloud_sdk_core
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.speech_to_text_v1 import SpeechToTextV1


class SpeechToTextAPI:

    def __init__(self, languageManager):
        self.languageManager = languageManager

        self.url = "https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/079804c4-c237-49f9-b65b-5d749d5ff502"
        self.apikey = "1gp0cp4UXZql1k0JZ3ihVuB-nPUUxKe28l5zu4f_ohiv"
        self.authenticator = IAMAuthenticator(self.apikey)
        self.s2t = SpeechToTextV1(authenticator=self.authenticator)
        self.s2t.set_service_url(self.url)

    def recognizeTextInFile(self, file, model, window):
        print('recognize file : ' + file)
        print('model = ' + model)

        final_result_s2t = ''
        try:
            with open(file, mode="rb") as wav:
                try:
                    response = self.s2t.recognize(audio=wav, model=model)
                    s2t_responses_list = []
                    for responses in response.result['results']:
                        s2t_responses_list.append(responses['alternatives'][0]['transcript'] + '\n')
                    s2t_responses_list.append('\n')

                    final_result_s2t = '\n'.join(s2t_responses_list)

                except ibm_cloud_sdk_core.api_exception.ApiException as e:
                    final_result_s2t = '-> ERROR File type is not supported'
                    print(e)

        except FileNotFoundError as e:
            final_result_s2t = '[ERROR No file selected]\n'
            print(e)

        return final_result_s2t
