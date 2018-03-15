class ConllSentenceEncoder(object):
    def __init__(self, words, labels):
        self._words = words
        self._labels = labels

        self._words_dict = {word: index for index, word in enumerate(self._words)}
        self._labels_dict = {label: index for index, label in enumerate(self._labels)}
    
    def encode_sentence(self, sentence):
        words = [t[0] for t in sentence]
        labels = [t[1] for t in sentence]

        enc_words = [self._words_dict[w] for w in words]
        enc_labels = [self._words_dict[l] for l in labels]

        return enc_words, enc_labels