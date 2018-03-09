import sys
sys.path.insert(0, '../src')

from annotated_text import AnnotatedText
from simple_match_annotator import EntityMatchAnnotator, Entity
from HAREM_annotator import HaremAnnotator
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
        e1 = Entity(["B1", "B1 E1", "B1 I1 E1"],["c1","c2","c3"])
        e2 = Entity(["B2", "B2 E2", "B2 I2 E2"],["c3"])
        in_between_string = "O O O"
        
        text = e1.names[0] + in_between_string + e1.names[2] + in_between_string + e2.names[2]
        annotated = EntityMatchAnnotator(text, [e1, e2])

        results = {e1.names[0]: e1.classes, e1.names[2]: e1.classes, e2.names[2]: e2.classes}

        for a in annotated._annotations:
            self.assertTrue(a.section in results)
            self.assertTrue(sorted(a.classes) == sorted(results[a.section]))
            del results[a.section]

        self.assertEqual(0, len(results))

class harem_annotator_tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # For the purposes of testing the 'harem_simple.xml' file is a subsection of the harem corpus without the "ALT" tags (i.e <ALT>)
        cls.harem_simple = "./test_resources/harem_simple.xml"
        cls.harem_simple_fixed = "./test_resources/harem_simple_fixed.xml"
        utils.fix_HAREM_XML(cls.harem_simple, cls.harem_simple_fixed)

        # Has 'ALT' tag
        cls.harem_with_alt = "./test_resources/harem_with_alt.xml"
        cls.harem_with_alt_fixed = "./test_resources/harem_with_alt_fixed.xml"
        utils.fix_HAREM_XML(cls.harem_with_alt, cls.harem_with_alt_fixed)

        # full HAREM
        cls.harem_full = "../resources/ColeccaoDouradaHAREM/ColeccaoDouradaHAREM.xml"
        cls.harem_full_fixed = "../resources/ColeccaoDouradaHAREM/ColeccaoDouradaHAREM_fixed.xml"
        utils.fix_HAREM_XML(cls.harem_full, cls.harem_full_fixed)

    def test_simple_matches(self):
        doc_xml = next(utils.get_HAREM_DOCS_XML(self.harem_simple_fixed))
        annotator = HaremAnnotator(doc_xml)

        text = '''
Legi�o da Boa Vontade comemora 10�. anivers�rio
 
A Legi�o da Boa Vontade comemora amanh� o 10�. anivers�rio da sua implanta��o em Portugal com cerim�nias de car�cter religioso e de conv�vio -- disse ontem fonte da organiza��o. 
Uma reuni�o ter� lugar no espa�o de cultura ecum�nica do Porto, que contar� com a presen�a de benfeitores, colaboradores, amigos e simpatizantes interessados. 
A Legi�o da Boa Vontade, institui��o educacional, cultural, beneficente e filantr�pica, foi fundada no Brasil pelo jornalista, radialista e poeta Alziro Zarur no programa de r�dio �Hora da Boa Vontade�, na R�dio Globo do Rio de Janeiro. 
Ap�s a morte de Alziro Zarur, Jos� Paiva Netto, tamb�m jornalista, radialista e escritor, presidiu a esta obra, tendo-a expandido a outros pa�ses. 
A Legi�o da Boa Vontade ocupa, hoje, o 4.� lugar entre as organiza��es inscritas na Organiza��o Mundial das Na��es Unidas. 
Em Portugal, a Legi�o da Boa Vontade iniciou o seu trabalho a 2 de Mar�o de 1989, dando ajuda material e espiritual � popula��o portuguesa mais carenciada atrav�s de programas como � Um passo em frente � ,  � Ronda-da-caridade � e  Semente da Boa vontade � .
'''
        # check if the text was built correctlly
        self.assertTrue(annotator._text == text)

        simple_sections = [(["ORGANIZACAO"], "Legi�o da Boa Vontade")
                          ,(["VALOR"], "10�.")
                          ,(["ORGANIZACAO"], "Legi�o da Boa Vontade")
                          ,(["VALOR"], "10�.")
                          ,(["LOCAL"], "Portugal")
                          ,(["LOCAL"], "Porto")
                          ,(["ORGANIZACAO"], "Legi�o da Boa Vontade")
                          ,(["LOCAL"], "Brasil")
                          ,(["PESSOA"], "Alziro Zarur")
                          ,(["LOCAL"], "Hora da Boa Vontade")
                          ,(["LOCAL"], "R�dio Globo")
                          ,(["LOCAL"], "Rio de Janeiro")
                          ,(["PESSOA"], "Alziro Zarur")
                          ,(["PESSOA"], "Jos� Paiva Netto")
                          ,(["ORGANIZACAO"], "Legi�o da Boa Vontade")
                          ,(["VALOR"], "4.�")
                          ,(["ORGANIZACAO"], "Organiza��o Mundial das Na��es Unidas")
                          ,(["LOCAL"], "Portugal")
                          ,(["ORGANIZACAO"], "Legi�o da Boa Vontade")
                          ,(["TEMPO"], "2 de Mar�o de 1989")
                          ,(["ABSTRACCAO"], "Um passo em frente")
                          ,(["ABSTRACCAO"], "Ronda-da-caridade")
                          ,(["ABSTRACCAO"], "Semente da Boa vontade")]
                          
        # validate simple sections
        self.assertTrue(len(simple_sections) == len(annotator._annotations))
        for a in annotator._annotations:
            matches = [s for s in simple_sections if a.section == s[1] and sorted(a.classes) == sorted(s[0])]

            self.assertTrue(len(matches) >= 1)

    def test_alt_and_simple_matches(self):
        doc_xml = next(utils.get_HAREM_DOCS_XML(self.harem_with_alt_fixed))
        annotator = HaremAnnotator(doc_xml)

        text = '''
PCP de Braga promove lanche e interven��o pol�tica 
A Comiss�o Concelhia de Braga do PCP promove s�bado um lanche e uma interven��o pol�tica, que v�o decorrer no Centro de Trabalho do PCP. 
Esta iniciativa insere-se nas comemora��es dos 78 anos de exist�ncia do PCP, que se celebram precisamente dia 6. 
'''
        # check if the text was built correctlly
        self.assertTrue(annotator._text == text)

        # simple in the sense it does not contain 'ALT' tags
        simple_sections =  [("Comiss�o Concelhia de Braga do PCP", ["ORGANIZACAO"]),
         ("Centro de Trabalho do PCP", ["LOCAL"]),
         ("78 anos", ["VALOR"]),
         ("PCP", ["ORGANIZACAO"]),
         ("6", ["TEMPO"])]

        alt_groups = [[("PCP", ["ORGANIZACAO"]), ("Braga", ["LOCAL"])],
                      [("PCP de Braga", ["ORGANIZACAO"])]]

        # validate simple sections
        self.assertTrue(len(simple_sections) == len(annotator._annotations))
        for a in annotator._annotations:
            matches = [s for s in simple_sections if a.section == s[0] and sorted(a.classes) == sorted(s[1])]
            self.assertTrue(len(matches)== 1)

        results = [[(s.section, s.classes) for s in g] for g in annotator.alternatives_sections[0].groups]

        self.assertTrue(sorted(alt_groups) == sorted(results))
    
    def test_all(self):
        for doc_xml in utils.get_HAREM_DOCS_XML(self.harem_full_fixed):
            annotator = HaremAnnotator(doc_xml)

if __name__ == '__main__':
    unittest.main()