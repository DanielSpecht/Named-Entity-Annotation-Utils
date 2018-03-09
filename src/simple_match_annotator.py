from annotated_text import AnnotatedText, AnnotatedSection
from functools import reduce
import utils

class Entity(object):
    """ A simple base class for representating an entity mentioned in text """
    
    def __init__(self, names, classes):
        self.names = names
        self.classes = classes

class EntityMatchAnnotator(AnnotatedText):
    """ Class for annotating text with recieved entities """
    
    def __init__(self, text, entities):
        super().__init__(text)
        self.entities = entities

        if self.entities:
            self._match_entities(entities, text)

    def _match_entities(self, entities, text):
        """ Annotates the occurences of the names of the entities
            In case of entities of different classes with same possible names, adds the two classes to the annotation.
        Args:
            entities (Entity): The entities to have their possible names 
            text (string): The text to search the strings on the text
        """
        
        names = reduce(lambda x, y: x + y, [entity.names for entity in entities])
        
        # create lookup table for names classes
        class_lookup = {name:set() for name in names}
        for entity in entities:
            for name in entity.names:
                class_lookup[name] = set(entity.classes)
                continue
            class_lookup[name].union(entity.classes)

        matches = utils.match_strings(text, names)
        i = 0
        for name in matches:
            for segment in matches[name]:
                start = segment[0]
                end = segment[1]
                i+=1
                self.tag_section(start,end, list(class_lookup[name]))