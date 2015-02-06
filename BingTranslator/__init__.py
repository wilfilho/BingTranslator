# Copyright 2014 Will Filho <dookgulliver@willfilho.com>
#
# This file is part of BingTranslator.
#
# This program free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with BingTranslator. If not, see <http://www.gnu.org/licenses/>.

from BingTranslator.models import (TranslatorMode, TextModel, TextArrayModel,
                                    TranslationsModel, SpeakModel, 
                                    TextDetectLanguageModel)
from BingTranslator.utils import TextUtils, DownloadAudio
import urllib
import json
import requests



class Translator(object):
    def __init__(self, client_id, client_secret):
        self._client_secret = client_secret
        self._client_id = client_id
        self._url_request = "http://api.microsofttranslator.com"
        self._grant_type = 'client_credentials'

    def _get_token(self):
        """
            Get token for make request. The The data obtained herein are used 
            in the variable header.

            Returns:
                To perform the request, receive in return a dictionary
                with several keys. With this method only return the token
                as it will use it for subsequent requests, such as a 
                sentence translate. Returns one string type.
        """
        informations = self._set_format_oauth()
        oauth_url = "https://datamarket.accesscontrol.windows.net/v2/OAuth2-13"
        token = requests.post(oauth_url, informations).json()
        return token["access_token"]

    def _set_format_oauth(self):
        """
            Format and encode dict for make authentication on microsoft 
            servers.
        """
        format_oauth = urllib.parse.urlencode({
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'scope': self._url_request,
            'grant_type': self._grant_type
        }).encode("utf-8")
        return format_oauth
    
    def _make_request(self, params, translation_url, headers):
        """
            This is the final step, where the request is made, the data is 
            retrieved and returned.
        """
        resp = requests.get(translation_url, params=params, headers=headers)
        resp.encoding = "UTF-8-sig"
        result = resp.json()
        return result

    def _get_content(self, params, mode_translate):
        """
            This method gets the token and makes the header variable that 
            will be used in connection authentication. After that, calls 
            the _make_request() method to return the desired data.
        """
        token = self._get_token()
        headers = {'Authorization': 'Bearer '+ token}
        parameters = params
        translation_url = mode_translate
        return self._make_request(parameters, translation_url, headers)

    def get_languages_for_translate(self):
        """
            Returns one array of language supported by api for translate.
        """
        mode_translate = TranslatorMode.LanguagesForTranslate.value
        return self._get_content(None, mode_translate)

    def get_languages_for_speak(self):
        """
            Returns one array of language supported by api for speak.
        """
        mode_translate = TranslatorMode.LanguagesForSpeak.value
        return self._get_content(None, mode_translate)

    def detect_language(self, text):
        """
            Params:
                ::text = Text for identify language.
            
            Returns:
                Returns language present on text.
        """
        infos_translate = TextDetectLanguageModel(text).to_dict()
        mode_translate = TranslatorMode.Detect.value
        return self._get_content(infos_translate, mode_translate)

    def detect_languages(self, texts):
        """
            Params:
                ::texts = Array of texts for detect languages

            Returns:
                Returns language present on array of text.
        """
        text_list = TextUtils.format_list_to_send(texts)
        infos_translate = TextDetectLanguageModel(text_list).to_dict()
        texts_for_detect = TextUtils.change_key(infos_translate, "text",
                                                    "texts", infos_translate["text"])
        mode_translate = TranslatorMode.DetectArray.value
        return self._get_content(texts_for_detect, mode_translate)

    def translate(self, text, to_lang, from_lang=None, 
                content_type="text/plain", category=None):
        """
            This method takes as a parameter the desired text to be translated
            and the language to which should be translated. To find the code 
            for each language just go to the library home page.
            The parameter ::from_lang:: is optional because the api microsoft 
            recognizes the language used in a sentence automatically.
            The parameter ::content_type:: defaults to "text/plain". In fact
            it can be of two types: the very "text/plain" or "text/html".
            By default the parameter ::category:: is defined as "general", 
            we do not touch it.
        """
        infos_translate = TextModel(text, to_lang,
            from_lang, content_type, category).to_dict()
        mode_translate = TranslatorMode.Translate.value
        return self._get_content(infos_translate, mode_translate)


    def translate_texts(
            self, texts, to_lang, from_lang=None, 
            content_type="text/plain", category=None,uri=None, 
            user=None, state = None):
        texts_formated = TextUtils.format_list_to_send(texts)
        infos_translate = TextArrayModel(
            texts_formated, to_lang, from_lang, 
            content_type, category, uri, user, state).to_dict()
        mode_translate = TranslatorMode.TranslateArray.value
        return self._get_content(infos_translate, mode_translate)

    def get_translations(
            self, text, to_lang, max_translations, from_lang=None, 
            content_type="text/plain", category=None,uri=None, 
            user=None, state = None):
        infos_translate = TranslationsModel(
            text, to_lang, max_translations, from_lang, content_type, 
            category, uri, user, state)
        infos_translate.clean_text_property()
        mode_translate = TranslatorMode.Translations.value
        return self._get_content(infos_translate.to_dict(), mode_translate)

    def get_multiple_translations(
            self, text, to_lang, max_translations, from_lang=None, 
            ontent_type="text/plain", category=None,uri=None, 
            user=None, state = None):
        texts_formated = TextUtils.format_list_to_send(text)
        infos_translate = TranslationsModel(
            texts_formated, to_lang, max_translations, 
            from_lang, content_type, category, uri, user, state).to_dict()
        mode_translate = TranslatorMode.TranslationsArray.value
        return self._get_content(infos_translate, mode_translate)

    def speak_phrase(self, text, language, format_audio=None, option=None):
        """
            This method is very similar to the above, the difference between 
            them is that this method creates an object of class 
            TranslateSpeak(having therefore different attributes) and use 
            another url, as we see the presence of SpeakMode enumerator instead
            of Translate.
            The parameter ::language:: is the same as the previous
            method(the parameter ::lang_to::). To see all possible languages go 
            to the home page of the documentation that library.
            The parameter ::format_audio:: can be of two types: "audio/mp3" or
            "audio/wav". If we do not define, Microsoft api will insert by
            default the "audio/wav". It is important to be aware that, to 
            properly name the file downloaded by AudioSpeaked
            class(which uses theclassmethod download).
            The parameter ::option:: is responsible for setting the audio quality. 
            It can be of two types: "MaxQuality" or "MinQuality". By default, if
            not define, it will be "MinQuality".
        """
        infos_speak_translate = SpeakModel(
            text, language, format_audio, option).to_dict()
        mode_translate = TranslatorMode.SpeakMode.value
        return self._get_content(infos_speak_translate, mode_translate)


