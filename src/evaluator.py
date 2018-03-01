import xml.etree.ElementTree as etree

class harem_reader(object):
    """
    Functionalities for manipulating files annotated using the HAREM annotation directives
    """

    def __init__(self, file_path):
        """
        Keyword arguments:
            - file_path -- The path of the harem file
        """

        self.file_path = file_path
        self._file = None # stores the open file

    def read_articles(self):
        """
        Streams the articles of the file, yielding 'HAREM_article' objects
        """
        
        for event, elem in etree.iterparse(self.file_path, events=('start', 'end')):
            tag_name = elem.tag
            print(tag_name)

    def get_article(self):
        """
        Returns the next article of the corpus
        """
        pass 

    def next_line(self):
        """
        """
        pass


class HAREM_article(object):
    """ 
    Defines an article annotated using the HAREM annotation directives 
    """

    def __init__(self,article_xml):
        self.article_xml = article_xml