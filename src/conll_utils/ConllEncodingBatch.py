from ConllFileManager import ConllFileManager

class ConllEncodingBatch(ConllFileManager):
    def __init__(self, directory, file_extension = '*.testa', encoding = 'latin-1'):
        super().__init__(directory, file_extension, encoding)

    def test(self, batch_size):
        c = 0
        for s in self.yield_sentences():
            

    def batch_sentences(self, batches):
        for i, o in zip(batch(X_train, batches), batch(y_train, batches)):
            yield (i, o)



# def batch(iterable, n=1):
#     l = len(iterable)
#     for ndx in range(0, l, n):
#         yield iterable[ndx:min(ndx + n, l)]


