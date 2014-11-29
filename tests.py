from bing_translator import Bing
import unittest


CLIENT_ID = "BookAboutPyQt5"
CLIENT_SECRET = "RWfmb4O7eO3zbnlTqZaPu8cBmMthaXkonxQA9sQnQ+0="

translator = Bing(CLIENT_ID, CLIENT_SECRET)
trans = translator.translate("Chorar, voar e correr", "en")
print (trans)
