# This script makes the HAREM annotated file comply with xml specifications

file = "./ColeccaoDouradaHAREM_original.xml"

regexp = "<\/?([^" "]*).*>"
pat = re.compile(regexp)

print pat.findall(s)

def fix_tag_names(str):
    """
    Changes the character '|' found in the tags by the character '-'
    """

    


def modify_HAREM (file_path, output_filename="ColeccaoDouradaHAREM_modified.xml"):
    """
    Creates a new version of the harem annotated file complying with xml.
    Nests every article under a "data" tag and fixes the names of the tags
    """

    with open (file_path,"r") as original, open(output_filename,"w") as modified:
        
        modified.write
        for line in original:
            new_line = 