from annotated_text import AnnotatedText, AnnotatedSection
import xml.etree.ElementTree as etree
from functools import reduce
import utils
import re

class AlternativesAnnotatedSection():

    def __init__(self, text, start_index, end_index):
        
        if end_index < start_index or end_index > len(text) - 1 or start_index < 0:            
            raise Exception("Invalid segment specification")

        self.section = text[start_index: end_index + 1]
        self.init = start_index
        self.end_index = end_index
        self.groups = []

    def new_group(self):
        self.groups.append([])

    def tag_section(self, text, start_index, end_index, classes):
        self.groups[-1].append(AnnotatedSection(text, start_index, end_index, classes))         

class HaremAnnotator(AnnotatedText):
    """ Class for annotating text with recieved entities """
    def __init__(self, harem_doc_xml):
        harem_xml = etree.XML(harem_doc_xml)
        
        self.doc_id = harem_xml.find("DOCID").text
        self.gender = harem_xml.find("GENERO").text
        self.origin = harem_xml.find("ORIGEM").text
        super().__init__(self._get_xml_text(harem_xml.find('TEXTO')))
        self.alternatives_sections = []
        self._annotate_harem_doc(harem_xml)
        
    def _tag_alt_element(self, alt_element, current_index):
        subtrees = self._get_alt_tag_subtrees(alt_element)
        alt_sec = AlternativesAnnotatedSection(self._text, current_index, current_index + len(self._get_alt_element_text(alt_element)))
        for subtree in subtrees:
            alt_sec.new_group()
            i = current_index
            for xml_type, value in self._yield_xml_elements(subtree):
                if xml_type == "text":
                    i += len(value)
                elif xml_type == "simple_xml_element":
                    alt_sec.tag_section(self._text, i, i + len(value.text) - 1, [value.tag])
                    i += len(value.text)

                elif xml_type == "alt_xml_element":
                    raise Exception("Invalid ALT tag inside ALT tag")

        self.alternatives_sections.append(alt_sec)
            
    def _get_alt_tag_subtrees(self, alt_element):
        # Gets the subtree as string
        ALT_regex = re.compile('<ALT>(.*)</ALT>')
        ALT_subtree_str = ALT_regex.search(etree.tostring(alt_element).decode("utf-8")).group(1)
        # TODO: possible bug: the '|' character is used not to divide, but as part of the text itself
        subtrees = ALT_subtree_str.split("|")
        # Enclose in 'SUBELEMENT' tag
        subtrees = ["".join(["<SUBELEMENT>", subtree, "</SUBELEMENT>"]) for subtree in subtrees]
        # Build elements
        subtrees = [etree.XML(subtree) for subtree in subtrees]
        return subtrees

    def _get_alt_element_text(self, alt_element):
        subtrees = self._get_alt_tag_subtrees(alt_element)
        return "".join(list(subtrees[0].itertext()))

    def _get_simple_element_text(self, simple_element):
        return "".join(list(simple_element.itertext()))

    def _get_xml_text(self, xml_element):
        text = []
        for xml_type, value in self._yield_xml_elements(xml_element):
            if xml_type == "text":
                text.append(value)
            elif xml_type == "alt_xml_element":
                text.append(self._get_alt_element_text(value))
            elif xml_type == "simple_xml_element":
                text.append(self._get_simple_element_text(value))
        
        return "".join(text)

    def _yield_xml_elements(self, xml_element):
        
        segments = list(xml_element.itertext())
        elements = list(xml_element.iter())[1:] # jump 'text' element

        el_i = 0
        seg_i = 0
        
        while seg_i < len(segments):
            
            if el_i < len(elements):
                element = elements[el_i]
                element_segments = list(element.itertext())
                element_subelements = list(element.iter())

                if  element_segments == segments[seg_i:seg_i + len(element_segments)]:
                    elemet_type = "alt_xml_element" if element.tag == "ALT" else "simple_xml_element"
                    yield (elemet_type, element)
                    el_i += len(element_subelements)
                    seg_i += len(element_segments)
                    continue
            
            yield ("text", segments[seg_i])
            seg_i += 1

    def _annotate_harem_doc(self, harem_xml_element):
        current_index = 0
        for xml_type, value in self._yield_xml_elements(harem_xml_element.find('TEXTO')):

            if xml_type == "text":
                current_index += len(value)

            if xml_type == "simple_xml_element":
                element_text = self._get_simple_element_text(value)
                print(self._text[current_index:current_index + len(element_text)])
                self.tag_section(current_index, current_index + len(element_text) - 1, [value.tag])
                current_index += len(element_text)

            if xml_type == "alt_xml_element":
                self._tag_alt_element(value, current_index)
                current_index += len(self._get_alt_element_text(value))