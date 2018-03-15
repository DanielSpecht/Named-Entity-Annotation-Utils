from ConllFile import ConllFile
import glob
import os

class ConllFileManager(object):
    def __init__(self, directory, file_extension = '*.testa', encoding = 'latin-1'):
        self._file_extension = file_extension
        self._directory = directory
        self._encoding = encoding

    def yield_sentences(self):
        files = glob.glob(os.path.join(self._directory, self._file_extension))
        for file in files:
            conll_file = ConllFile(file, self._encoding)
            for sentence in conll_file.yield_sentences():
                yield sentence

#c = ConllFileManager("/home/daniel/Repositories/Models/conll2002/files")
#for sentence in c.yield_sentences():
#    print(len(sentence))
#print(len(list(c.yield_sentences())))