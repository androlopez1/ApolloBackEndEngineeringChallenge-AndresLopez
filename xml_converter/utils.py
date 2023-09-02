import xml.etree.ElementTree as ET

def xml_to_dict(element):

    """
    Helper function to convert an XML into a dict, in order to meet the leaf-nodes requirement.
    """

    if len(element) == 0:
        # Leaf-node
        if element.text==None:
            return {element.tag: "" }
        return {element.tag: element.text }
    else:
        # Non-leaf node
        result = {element.tag: []}
        for child in element:
            result[element.tag].append(xml_to_dict(child))
        return result