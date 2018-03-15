from ConllFileManager import ConllFileManager
from collections import Counter


class ConllFilesStatistics(ConllFileManager):
    def __init__(self, directory, file_extension = '*.testa', encoding = 'latin-1'):
        super().__init__(directory, file_extension, encoding)
        self.n_sentences = None
        self.max_sentence_len = None
        self.words_count = None
        self.labels_count = None

    def _get_statistics(self):
        self.n_sentences = 0
        self.max_sentence_len = 0
        self.words_count = Counter()
        self.labels_count = Counter()


        for sentence in self.yield_sentences():
            words = [t[0] for t in sentence]
            labels = [t[1] for t in sentence]

            self.words_count.update(words)
            self.labels_count.update(labels)

            self.max_sentence_length = max(self.max_sentence_length, len(sentence))
    
    @property
    def words(self):
        return list(self.words_count.keys())
    
    @property
    def tags(self):
        return list(self.words_count.keys())
