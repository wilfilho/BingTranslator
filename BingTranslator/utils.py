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


class TextUtils(object):
    @staticmethod
    def change_key(dict_o, old_key, new_key, value):
        dict_o[new_key] = value
        del dict_o[old_key]
        return dict_o

    @staticmethod
    def format_list_to_send(list_data):
        formatted = "["
        for text in list_data:
            if text == list_data[-1]:
                formatted += "\"{0}\"]".format(text)
                return formatted
            formatted += "\"{0}\",".format(text)
        return formatted


class DownloadAudio(object):
    @staticmethod
    def download(self, url, path, name_audio):
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