# Copyright 2014 Will Filho <dookgulliver@willfilho.com>
#
# This file is part of bing_translator.
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
# along with bing_translator. If not, see <http://www.gnu.org/licenses/>.

from ms_translator import Translator
import unittest


CLIENT_ID = "BookAboutPyQt5"
CLIENT_SECRET = "RWfmb4O7eO3zbnlTqZaPu8cBmMthaXkonxQA9sQnQ+0="


class TestAll(unittest.TestCase):
	def setUp(self):
		self.translator = Translator(CLIENT_ID, CLIENT_SECRET)

	def test_detect_language(self):
		lang_detect = self.translator.detect("Hello World")
		self.assertEqual("en", lang_detect)

	def test_detect_languages(self):
		langs_detected = self.translator.detect_texts(["Hello World","Voe sem parar."])
		self.assertEqual(["en","pt"], langs_detected)

	def test_translate_method(self):
		trans = self.translator.translate("Oi", "en")
		self.assertEqual("Hi", trans)

if __name__ == "__main__":
	unittest.main()
