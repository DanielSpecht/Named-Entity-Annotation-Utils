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

# e1 = Entity(["B1", "B1 E1", "B1 I1 E1"],["c1","c2"])
# e2 = Entity(["B2", "B2 E2", "B2 I2 E2"],["c3"])
# in_between_string = "O O O"

# text = e1.names[0] + in_between_string + e1.names[2] + in_between_string + e2.names[2]
# print(text)

# annotated = EntityMatchAnnotator(text, [e1, e2])
# print(len(annotated._annotations))

# for a in annotated._annotations:
#     print(a.section)