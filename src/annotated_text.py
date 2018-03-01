class AnnotatedSection(object):
    """ An annotation in a section of the text """
    
    def __init__(self, text, start_index, end_index, classes):

        if end_index < start_index or end_index > len(text) - 1 or start_index < 0:
            raise Exception("Invalid segment specification")

        self.section = text[start_index: end_index + 1]
        self.init = start_index
        self.end_index = end_index
        self.classes = classes

class AnnotatedText(object):
    """ Text with annotated sections """

    def __init__(self, text):
        self._text = text
        self._annotations = []

    def tag_section(self, start_index, end_index, classes):
        """ Annotates a section of the text with information """

        annotation = AnnotatedSection(self._text, start_index, end_index, classes)
        self._annotations.append(annotation)
        return annotation