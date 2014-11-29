# LOOK ME: THE DOC STRINGS HAVE A BAD ENGLISH. WOW!

from enum import Enum
import urllib
import json
import requests


class TranslatorMode(Enum):
  """
    Don't cry(for line lenght) Python :/
  """
  Detect = "http://api.microsofttranslator.com/V2/Ajax.svc/Detect"
  DetectArray = "http://api.microsofttranslator.com/V2/Ajax.svc/DetectArray"
  LanguagesForTranslate = "http://api.microsofttranslator.com/V2/Ajax.svc/GetLanguagesForTranslate"
  LanguagesForSpeak = "http://api.microsofttranslator.com/V2/Ajax.svc/GetLanguagesForSpeak"
  Translations = "http://api.microsofttranslator.com/V2/Ajax.svc/GetTranslations"
  TranslationsArray = "http://api.microsofttranslator.com/V2/Ajax.svc/GetTranslationsArray"
  SpeakMode = "http://api.microsofttranslator.com/V2/Ajax.svc/Speak"
  Translate = "http://api.microsofttranslator.com/V2/Ajax.svc/Translate"
  TranslateArray = "http://api.microsofttranslator.com/V2/Ajax.svc/TranslateArray"


class TextUtils(object):
  @classmethod
  def put_suit_on_from_key(cls, dict_o, value):
    dict_o["from"] = value
    del dict_o["from_lang"]
    return dict_o

  @classmethod
  def format_list_to_send(self, list_data):
    formatted = "["
    for text in list_data:
      if text == list_data[-1]:
        formatted += "\"{0}\"]".format(text)
        return formatted
      formatted += "\"{0}\",".format(text)
    return formatted


class TextModel(object):
  def __init__(self, text, to_lang, from_lang=None, 
        content_type="text/plain", category=None):
    """
      This class is important because it leaves the bullet ready 
      to trigger.
    """
    self.text = text
    self.to = to_lang
    self.from_lang = from_lang
    self.contentType = content_type
    self.category = category

  def to_dict(self):
    dict_obj = TextUtils.put_suit_on_from_key(self.__dict__, 
                          self.from_lang)
    return dict_obj

    
class TextArrayModel(object):
  def __init__(
      self, texts, to_lang, from_lang=None, content_type="text/plain",
      category=None, uri=None, user=None, state=None):
    """
      This is one model for TranslateArray mode of requisition.
    """
    self.texts = texts
    self.from_lang = from_lang
    self.to = to_lang
    self.contentType = content_type #name don't like a Python because the dictionnary
    self.category = category
    self.uri = uri
    self.user = user
    self.state = state

  def to_dict(self):
    dict_initial = TextUtils.put_suit_on_from_key(self.__dict__, 
                            self.from_lang)
    return dict_initial


class TranslationsModel(TextArrayModel):
  def __init__(
      self, text, to_lang, max_translations, from_lang=None, 
      content_type="text/plain", category=None, uri=None, user=None, 
      state=None):
    """
      This is one model for Translations mode of requisition.
    """
    TextArrayModel.__init__(self, text, to_lang, from_lang, 
                content_type, category, uri, user, state)
    self.maxTranslations = max_translations
    self.text = text

  def clean_text_property(self):
    self.__dict__.pop("texts")


class TextDetectModel(object):
  def __init__(self, text):
    self.text = text

  def to_dict(self):
    return self.__dict__

  def change_property(self):
      self.__dict__["texts"] = self.text
      self.__dict__.pop("text")


class SpeakModel(object):
  def __init__(self, text, language, format_audio=None, option=None):
    """
      This class is similar to TranslatorText, but with different 
      properties.
    """
    self.text = text
    self.language = language
    self.format = format_audio
    self.options = option

  def to_dict(self):
    return self.__dict__


class AudioSpeaked(object):
  @classmethod
  def download(cls, url, path, name_audio):
    """
      Params:

        ::url = Comprises the url used to download the audio.
        ::path =  Comprises the location where the file should be saved.
        ::name_audio = Is the name of the desired audio.
      
      Definition:

      Basically, we do a get with the requests module and after that 
      we recorded in the desired location by the developer or user, 
      depending on the occasion.
    """
    if path is not None:
      with open(str(path+name_audio), 'wb') as handle:
        response = requests.get(url, stream = True)
        if not response.ok:
          raise Exception("Error in audio download.")
        for block in response.iter_content(1024):
          if not block:
            break
          handle.write(block)


class Bing(object):
  def __init__(self, client_id, client_secret):
    self._client_secret = client_secret
    self._client_id = client_id
    self._url_request = "http://api.microsofttranslator.com"
    self._grant_type = 'client_credentials'

  def _get_token(self):
    """
      Get token for make request. The The data obtained herein are used 
      in the variable header.

      Type of return:
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
    resp = requests.get(translation_url, params=params,headers=headers)
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
    infos_translate = None
    return self._get_content(infos_translate, mode_translate)

  def get_languages_for_speak(self):
    """
      Returns one array of language supported by api for speak.
    """
    mode_translate = TranslatorMode.LanguagesForSpeak.value
    infos_translate = None
    return self._get_content(infos_translate, mode_translate)

  def detect(self, text):
    """
      Params:
        ::text = Text for identify language.
      
      Returns:
        Returns language present on text.
    """
    infos_translate = TextDetectModel(text).to_dict()
    mode_translate = TranslatorMode.Detect.value
    return self._get_content(infos_translate, mode_translate)

  def detect_texts(self, texts):
    """
      Returns language present on array of text.
    """
    text_list = TextUtils.format_list_to_send(texts)
    infos_translate = TextDetectModel(text_list)
    infos_translate.change_property()
    mode_translate = TranslatorMode.DetectArray.value
    return self._get_content(infos_translate.to_dict(), mode_translate)

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
      texts_formated, to_lang, from_lang, content_type, category, uri, 
      user, state).to_dict()
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


