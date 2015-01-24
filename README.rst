Microsoft Translator API for Python
-----------------------------------

The *Microsoft* offers an online translation API to make requests
through various forms (Http, Ajax, SOAP or OData.). The features
provided by this API are very useful when we want to perform
translations, multiple translations or even listen to the pronunciation
of a certain word or phrase in desejada.Esta language library is an
implementation in Python that allows to use most of the features present
in this API. Basically what we do is, make a request to the Ajax API
method by **requests** module and get the desired response. Below is a
list of features offered by this library:

-  Translation of one or multiple phrases and texts.
-  Obtaining all possible translations for a word or multiple phrases.
-  So speak, where you can hear the pronunciation of phrases or text in
   the desired language.
-  This language detection on single or multiple sentences or texts.
-  Obtaining all possible languages for translation and so speak.

Installation
~~~~~~~~~~~~

You can use pip to make download and installation of the library. It is
noteworthy that, it uses three modules: requests, json and urllib. Using
the pip: ``sh $ pip install ms_translator`` ### Getting credentials

First of all, for us to use Microsoft's API we have to get a credential.
Which to some extent is free, unlike the Google Translator API that is
only within 30 days. It is noteworthy that the restriction to the free
acquisition of credentials is 2 million characters per month, that is,
you should not spend it. If you have an application that is used by a
lot of customers, recommend reviewing it. To see all the steps that must
be taken, go to the following link and follow the tutorial present in
it: http://blogs.msdn.com/b/translation/p/gettingstarted1.aspx

The information that we will use are: the *client\_id* and
*client\_secret*. These credentials are used in the request for
adqurirmos the token that allows us to perform translations. ### Getting
Started The use of the library is very simple, just by knowing what are
the methods and their parameters. For example, we do a simple
translation as follows: \`\`\`python from ms\_translator import
Translator #importing Translator class for translations.

client\_id = "" client\_secret = ""

translator = Translator(client\_id, client\_secret) phrase\_translated =
translator.translate("Hello World", "pt") #translating phrase print
(phrase\_translated) \`\`\` To see the code of all languages, access the
following link: http://msdn.microsoft.com/en-us/library/hh456380.aspx.
In the previous example, we use the *'en'* code to have displaced who
wish to translate our words into Portuguese. ##### The *translate*
method

The translate method may receive a number of parameters, as we can see
in the table below.

\| Parameter Name \| Description \|
\|----------------\|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\|
\| text \| Is the text to be translated. This parameter is required. \|
\| to\_lang \| This parameter corresponds to the language to which the
text should be translated. This parameter is required. \| \| from\_lang
\| This parameter corresponds to this language in the current sentence.
This parameter is not required because the Microsoft API recognizes this
language in the text by default. \| \| contentType \| This parameter
defines the type of data returned. By default it is set to "text/plain",
but you can use another option, which is "text/html". This parameter is
not required. \| \| category \| Matches the category of the sentence. By
default this parameter is set to "General". This parameter is not
required. \|

One of the other methods in this library, much like the translate method
is **translate\_texts**. The difference between these two methods is
that the latter accepts a list of strings as parameter. Besides the
aforementioned differences, the translate\_texts method allows the use
of three additional parameters. Consider the table below:

\| Parameter Name \| Description \|
\|----------------\|--------------------------------------------------------------------------------------------------------\|
\| uri \| A string containing the content location of this translation.
\| \| user \| A string used to track the originator of the submission.
\| \| state \| User state to help correlate request and response. The
same contents will be returned in the response. \|

Example of use:
``python phrases_translated = translator.translate_texts(["Hello World","Python is all"], "pt") #translating phrase print (phrase_translated)``
The return will be something like this:
``[{'OriginalTextSentenceLengths': [9], 'TranslatedText': 'Olá o mundo', 'From': 'en', 'TranslatedTextSentenceLengths': [12]}, {'OriginalTextSentenceLengths': [10], 'TranslatedText': 'Python é tudo', 'From': 'en', 'TranslatedTextSentenceLengths': [15]}]``
##### The *get\_translations* method The **get\_translations** method
returns all possible translations for a word in the language. This
method is very similar to the previous (**translate\_texts**), the
difference is that you must pass as parameter only a text/word and he
has a parameter called maxTranslations that is required. This parameter
defines the number of possible translations that the API should return
to you. Example of use:
``python trans = translator.get_translations("Speak", "pt", 2) print (trans)``
The return will be something like this:
``{'Translations': [{'MatchDegree': 100, 'Rating': 5, 'MatchedOriginalText': '', 'TranslatedText': 'Fala', 'Count': 0}, {'MatchDegree': 99, 'Rating': 1, 'MatchedOriginalText': 'speak', 'TranslatedText': 'Falar', 'Count': 1}], 'From': 'en'}``
The other very similar method to this is the
**get\_multiple\_translations**. The difference between this and the
former is that you will pass this parameter as a list of strings rather
than just a string. Example of use:
``python trans = translator.get_translations(["Speak","Fly"], "pt", 2) print (trans)``
### The *detect* method The detect method, as its name implies,
identifies the language used in a given sentence. He will receive only
one parameter, which is the desired phrase. Example of use:
``python trans = translator.detect("My name is Jonas") print (trans)``
In return we will have the code of the corresponding language to the
text. In the example above, we get an answer the following: 'en';
Indicating that the text is in English. We can also identify the present
languages in various texts by simply we use the **detect\_texts**
method, which receive as parameter a list of strings. Example of use:
``python trans = translator.detect_texts(["My name is Jonas","Voar, subir, cair."]) print (trans)``
##### The *speak\_phrase* method

The speak\_phrase method is responsible for providing us with a link to
download the audio containing the desired phrase. This method will
receive different parameters from previous. Let's look at the table
below:

\| Parameter Name \| Description \|
\|----------------\|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\|
\| text \| Text to be spoken. This parameter is required. \| \| language
\| Language in which the text should be spoken. \| \| format\_audio \|
This parameter defines the audio format. By default the audio defined by
Microsoft API file format is the "audio/wav", but you can use another
parameter, which is, "audio/mp3". This parameter is not required. \| \|
option \| This parameter defines the audio quality. By default, the
quality used by the API is "MinQuality", but we can use the value
"MaxQuality" to indicate that we want a better quality audio with. Worth
to emphasize that this will influence the size of the file to download.
This parameter is not required. \|

Example of use:

``python trans = translator.speak_phrase("Back to the future", "en", "audio/mp3", "MaxQuality") print (trans)``
In return we will have a string containing a URL to perform download the
audio. To do this, we can use **AudioSpeaked** class with the
**download** method, to use the audio locally. Example of use:
\`\`\`python from ms\_translator import Translator, AudioSpeaked

client\_id = "" client\_secret = ""

translator = Translator(client\_id, client\_secret) url =
translator.speak\_phrase("Back to the future", "en", "audio/mp3",
"MaxQuality") AudioSpeaked.download(url, "audios/","aud01.mp3") \`\`\`
The **download** of AudioSpeaked class classmethod receive three
parameters. The first is the url to download the audio, the second the
directory where it is stored and finally the audio name. Note that audio
extension must be the same length stated in the call **speak\_phrase**
method. For example, in the above code I set that I would have an
extension "audio/mp3" and download method I set the file name with an
extension mp3.

License
~~~~~~~

Microsoft Translator API for Python

Copyright (c) 2014, Will Filho, All rights reserved.

This library is free software; you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 3.0 of the License, or (at
your option) any later version.

This library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this library.
