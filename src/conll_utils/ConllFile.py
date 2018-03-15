class ConllFile(object):
    def __init__(self, conllu_path, encoding = 'latin-1'):
        self._conllu_path = conllu_path
        self._encoding = encoding

    def yield_sentences(self):
        sentence = []
        for line in open(self._conllu_path, 'r', encoding = self._encoding):
            stripped_line = line.strip().split(' ')
            
            if line == '\n':
                yield sentence
                sentence = []
            else:
                sentence.append(tuple(stripped_line))