import sys
sys.path.insert(0, '../src')

from annotated_text import AnnotatedText
from simple_match_annotator import EntityMatchAnnotator, Entity
import unittest
import utils

class test_text_annotation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._text = "A text for tagging"

    def test_annotate(self):
        annotated = AnnotatedText(self._text)
        annotation = annotated.tag_section(2,5,"class")
        self.assertEqual('text', annotation.section)

    def test_annotate_out_of_bounds(self):

        annotated = AnnotatedText(self._text)
        
        # case 1 - end index greater than sentence length
        with self.assertRaises(Exception):
            annotated.tag_section(2,len(self._text)+1,"class")

        # case 2 - start index maller than 0
        with self.assertRaises(Exception):
            annotated.tag_section(-1,3,"class")

        # case 3 - end index smaller than start index
        with self.assertRaises(Exception):
            annotated.tag_section(3,2,"class")

class utils_tests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # for the purposes of testing the following code will be used
        # B - Beginning of the searched string
        # I - Inside of the searched string
        # E - End of the searched string
       
        cls.str1 = "B"
        cls.str2 = "B E"
        cls.str3 = "B I E"

    def test_match_strings(self):
        
        # base case
        text = self.str1
        matches = utils.match_strings(text, [self.str1])
        correct = {self.str1:[(0,0)]}
        self.assertEqual(matches, correct)

        # base case many matches
        text = self.str1+self.str1
        matches = utils.match_strings(text, [self.str1])
        correct = {self.str1:[(0,0),(1,1)]}
        self.assertEqual(matches, correct)

        # base case many matches with elements in between
        elements_between = "---"
        text = self.str1 + elements_between + self.str1
        matches = utils.match_strings(text, [self.str1])
        correct = {self.str1:[(0,len(self.str1)-1), (0+len(self.str1)+len(elements_between),0+2*len(self.str1)+len(elements_between)-1 )]}
        self.assertEqual(matches, correct)

        # search for multi-character string
        text = self.str2
        matches = utils.match_strings(text, [self.str2])
        correct = {self.str2:[(0,len(self.str2)-1)]}
        self.assertEqual(matches, correct)

        # search for multi-character string in incomplete occurence
        text = self.str2[1:]
        matches = utils.match_strings(text, [self.str2])
        correct = {self.str2:[]}
        self.assertEqual(matches, correct)

        # search for many matches for multi-character string
        text = self.str2+self.str2
        matches = utils.match_strings(text, [self.str2])
        correct = {self.str2:[(0,len(self.str2)-1),(len(self.str2),2*len(self.str2)-1) ]}
        self.assertEqual(matches, correct)

        # multi-character string many matches with elements in between
        elements_between = "---"
        text = self.str2 + elements_between + self.str2
        matches = utils.match_strings(text, [self.str2])
        correct = {self.str2:[(0,len(self.str2)-1), (0+len(self.str2)+len(elements_between),0+2*len(self.str2)+len(elements_between)-1 )]}
        self.assertEqual(matches, correct)

        # many multi-character string many matches with elements in between
        elements_between = "---"
        text = self.str2 + elements_between + self.str2 + elements_between + self.str3
        matches = utils.match_strings(text, [self.str2, self.str3])
        correct = {self.str2:[(0,len(self.str2) - 1), (0+len(self.str2)+len(elements_between),0 + 2*len(self.str2)+len(elements_between) - 1)],
                   self.str3:[(2*len(self.str2) + 2*len(elements_between), 2*len(self.str2) + 2*len(elements_between) + len(self.str3) - 1 )]}
        self.assertEqual(matches, correct)

class simple_match_annotator_tests(unittest.TestCase):
    
    def test_entity_match_annotator(self):
        e1 = Entity(["B1", "B1 E1", "B1 I1 E1"],["c1","c2"])
        e2 = Entity(["B2", "B2 E2", "B2 I2 E2"],["c3"])
        in_between_string = "O O O"
        
        text = e1.names[0] + in_between_string + e1.names[2] + in_between_string + e2.names[2]
        annotated = EntityMatchAnnotator(text, [e1, e2])

        section_strings = [e1.names[0], e1.names[2], e2.names[2]]
        for a in annotated._annotations:
            self.assertTrue(a.section in section_strings)
            section_strings.remove(a.section)

if __name__ == '__main__':
    unittest.main()