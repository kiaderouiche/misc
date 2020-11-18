# Copyright (C) 2012 LibreSoft
# Copyright (C) 2020 Adgon Solutions, Algeria
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors :
#       Jesus M. Gonzalez-Barahona  <jgb@gsyc.es>*
#       K.I.A.Derouiche <kamel.derouiche@gmail.com>

# Description
# -----------
# This extension prints data from the table generated by the MessageWords ext.

import pathlib

from pycvsanaly2.extensions import Extension, register_extension
from pycvsanaly2.utils import uri_to_filename



class CommonWords:
    """Class with common words in English, read from a file"""

    def is_in(self, word):
        """Is word in common words?"""

        return (word in self.words)

    def __init__(self):
        """Initialize the class by reading from file"""

        self.words = []
        filename = pathlib.Path(__file__).resolve().parent + "/list_words.txt"
        file = open(filename, 'r')
        for line in file:
            if not line.startswith('#'):
                self.words.append(line.strip())
        file.close()


class MessageWordsPrint(Extension):
    """Extension to print data about word frequencies.

    It shows data in the table generated by the MessageWords extension.
    """

    deps = ['MessageWords']

    def __init__(self):
        """Initializes by instantiating some vars."""

        self.theCommonWords = CommonWords()

    def _get_repo_id(self, repo, uri, cursor) -> int:
        """Get repository id from repositories table"""

        path = uri_to_filename(uri)
        if path is not None:
            repo_uri = repo.get_uri_for_path(path)
        else:
            repo_uri = uri
        cursor.execute("SELECT id FROM repositories WHERE uri = '%s'" %
                       repo_uri)
        return (cursor.fetchone()[0])

    def _wordToExclude(self, word) -> bool:
        """Is this a word to exclude?"""

        if "@" in word or "/" in word or "_" in word:
            return True
        elif word.isdigit():
            return True
        elif self.theCommonWords.is_in(word):
            return True
        else:
            return False

    def run(self, repo, uri, db):
        """Extract commit message from scmlog table and do some analysis.
        """

        cnn = db.connect()
        # Cursor for reading from the database
        cursor = cnn.cursor()
        # Cursor for writing to the database
        write_cursor = cnn.cursor()
        repo_id = self._get_repo_id(repo, uri, cursor)

        cursor.execute("SELECT MIN(date) FROM words_freq")
        minDate = cursor.fetchone()[0]
        cursor.execute("SELECT MAX(date) FROM words_freq")
        maxDate = cursor.fetchone()[0]

        lastMonth = (maxDate.year - minDate.year) * 12 + maxDate.month - minDate.month

        for period in range(0, lastMonth):
            wordsFreq = {}
            month = (minDate.month + period) % 12 + 1
            year = minDate.year + (period + minDate.month) // 12
            date = str(year) + "-" + str(month) + "-01"
            query = """SELECT word, times
               FROM words_freq
               WHERE date = '%s' ORDER BY times DESC"""
            cursor.execute(query % date)
            rows = cursor.fetchall()
            print('*** ' + date + ":", end=' ')
            count = 0
            for (text, times) in rows:
                if not self._wordToExclude(text):
                    count += 1
                    print(text + " (" + str(times) + ")", end=' ')
                if count > 10:
                    break
            print()


register_extension("MessageWordsPrint", MessageWordsPrint)
