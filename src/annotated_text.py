       
class TextSection(object):
    """ An a section of a text """
    def __init__(self, text, start_index, end_index):
        
        if end_index < start_index or end_index > len(text) - 1 or start_index < 0:
            raise Exception("Invalid segment specification")

        self.section = text[start_index: end_index + 1]
        self.start_index = start_index
        self.end_index = end_index

class TaggedTextSection(TextSection):
    """ A tagged section of a text """
    def __init__(self, text, start_index, end_index, classes):
        super().__init__(text, start_index, end_index)
        self.classes = classes

class AnnotatedGroup(TextSection):
    """ Group of possible taggings for a section """
    
    def __init__(self, text, start_index, end_index):
        super().__init__(text, start_index, end_index)
        self.tagged_sections = []

    def tag_section(self, text, start_index, end_index, classes):
        """ Tags a section of the group """
        section_start = start_index - self.start_index
        section_end = end_index - self.start_index
        new_section = TaggedTextSection(text, section_start, section_end, classes)
        self._validate_new_section(new_section)
        self.tagged_sections.append(new_section)
    
    def _validate_new_section(self, new_section):
        """ Validates inexistence of overlapping """
        if not self.tagged_sections:
            return
        
        elif new_section.end_index >= self.tagged_sections[-1].start_index:
            raise Exception("Overlapping sections!")

class AnnotatedText(TextSection):
    """ Text with annotated sections """

    def __init__(self, text):
        self._text = text
        self.groups = []

    def new_group(self):
        """ Sets the current group to a new one """
        self.groups.append(Anno)

    def tag_section(self, start_index, end_index, classes):
        """ Annotates a section of the text with information """

        annotation = AnnotatedSection(self._text, start_index, end_index, classes)
        self._annotations.append(annotation)
        return annotation