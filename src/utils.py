import re
import xml.etree.ElementTree as etree

# TODO: use a search tree
def score_strings(text, strings, text_index):
    """ Indicating how many characters in sequence in the right order are present in the text starting from 'text_index'
    
    Args:
        text (string): [description]
        strings (string): [description]
        text_index (string): [description]
    
    Returns:
        dict: a dictionary where:
            - The keys (string) are the passed strings 
            - The values (int) are the number of characters matched from the start of the defined section of the text """

    scores = {string : 0 for string in strings}
    offset = 0

    while strings and text_index + offset < len(text):
        
        #increment inplace
        for string in strings:
            if string[offset] == text[text_index + offset]:
                scores[string] += 1

        offset += 1

        # removes parsed strings and strings with unmatched characters
        strings = list(filter(lambda s : offset < len(s) and scores[s] == offset, strings))

    return scores

def match_strings(text, strings):
    """
    Returns the segments where the strings occur.

    Args:
        text (string): 
        strings (string): [description]

    Returns:
        dict: A dictionary containing the occurences for each recieved string.
            - The keys are the strings
            - The values are the occurences represented by a tuple of integers representing the character where the occurence started and ended respectivelly
            i.e. {"string1":[(1,7),(8,14)]} """

    i = 0
    strings = list(set(strings))
    matches = {string: [] for string in strings}

    while i < len(text):
         
        scores = score_strings(text, strings, i)
        #scores = filter(lambda s: len(s) == scores[s] ,scores)
        scores = {k: v for k, v in scores.items() if v == len(k)}
        
        # match at character for any name
        if not scores:
            i += 1
            continue
        
        max_score_str =  max(scores, key=scores.get)
        max_score = scores[max_score_str]

        # not exact match
        if not len(max_score_str) == max_score:
            i += 1
            continue
        
        match = (i, i + max_score - 1)
        matches[max_score_str].append(match)
        i += max_score
    
    return matches

def fix_HAREM_XML(file_path, fixed_harem_path):
    category_regex = re.compile('<\/?([\|A-Z]+)>')
    type_regex = re.compile('TIPO="([^"]*)"')
    special_character_regex = re.compile('(?!&\w+;)&')

    with open(file_path,"r") as harem, open(fixed_harem_path,"w") as fixed_harem:
        
        fixed_harem.write("<DATA>")        
        
        for line in harem:
            line_types = type_regex.findall(line)
            line_categories = category_regex.findall(line)

            line_problematic_elements = [t for t in line_types + line_categories if '|' in t ]

            line = special_character_regex.sub("&amp;",line)

            for elem in line_problematic_elements:
                line = line.replace(elem,elem.replace('|','-'))

            fixed_harem.write(line)

        fixed_harem.write("</DATA>")

def get_HAREM_DOCS_XML(file_path):
    """
    Generator for the docs in the HAREM corpus.
    Yields the xml string of the sections of the recieved document in sucession.
    
    Args:
        file_path (string): The path of the HAREM corpus
    """
    DOC_regex = re.compile('(<DOC>.*</DOC>)', re.DOTALL)

    for event, elem in etree.iterparse(file_path, events=('end',)):
        if elem.tag == "DOC":
            doc_xml_string = etree.tostring(elem).decode("utf-8")
            # filter only the relevant segment
            doc_xml_string = DOC_regex.search(doc_xml_string).group(1)
            yield doc_xml_string