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


from BingTranslator.utils import TextUtils
from enum import Enum


class TranslatorMode(Enum):
    Detect = "http://api.microsofttranslator.com/V2/Ajax.svc/Detect"
    DetectArray = "http://api.microsofttranslator.com/V2/Ajax.svc/DetectArray"
    LanguagesForTranslate = "http://api.microsofttranslator.com/V2/Ajax.svc/GetLanguagesForTranslate"
    LanguagesForSpeak = "http://api.microsofttranslator.com/V2/Ajax.svc/GetLanguagesForSpeak"
    Translations = "http://api.microsofttranslator.com/V2/Ajax.svc/GetTranslations"
    TranslationsArray = "http://api.microsofttranslator.com/V2/Ajax.svc/GetTranslationsArray"
    SpeakMode = "http://api.microsofttranslator.com/V2/Ajax.svc/Speak"
    Translate = "http://api.microsofttranslator.com/V2/Ajax.svc/Translate"
    TranslateArray = "http://api.microsofttranslator.com/V2/Ajax.svc/TranslateArray"


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
        return TextUtils.change_key(dict_o = self.__dict__, 
                                    new_key = "from",
                                    old_key = "from_lang",
                                    value = self.from_lang)


class TextArrayModel(TextModel):
    def __init__(
            self, texts, to_lang, from_lang=None, content_type="text/plain",
            category=None, uri=None, user=None, state=None):
        """
            This is one model for TranslateArray mode of requisition.
        """
        TextModel.__init__(self, texts, to_lang, from_lang, 
                            content_type, category)
        self.texts = texts
        self.uri = uri
        self.user = user
        self.state = state
        self.clean_property()

    def clean_property(self):
        self.__dict__.pop("text")


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


class TextDetectLanguageModel(object):
    def __init__(self, text):
        self.text = text

    def to_dict(self):
        return self.__dict__


class SpeakModel(object):
    def __init__(self, text, language, format_audio=None, option=None):
        """
            This class is similar to TextModel, but with different 
            properties.
        """
        self.text = text
        self.language = language
        self.format = format_audio
        self.options = option

    def to_dict(self):
        return self.__dict__

