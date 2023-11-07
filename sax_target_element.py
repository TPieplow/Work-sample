# https://docs.python.org/3/library/xml.sax.handler.html#contenthandler-objects
# https://nanonets.com/blog/parse-xml-files-using-python/
# https://vegibit.com/python-xml-parsing/
# Python & XML, av Christopher A. Jones, Fred L. Drake, O'Reilly (framför allt de tre första kapitlen)

import xml.sax
import json
from xml.sax import ContentHandler
from xml.sax._exceptions import SAXParseException

# Custom handler, initializing object attributes in the "constructor".
class RetrieveTargetValue(ContentHandler):
    def __init__(self, attribute_name, attribute_value, parent_element, target_element):
        self.target_text = ""
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.parent_element = parent_element
        self.target_element = target_element
        self.id_value = None
        self.is_inside_target = 0
        self.is_text = 0
        
    # Presents a message to the user.
    def startDocument(self):
        print('Parsing started!')

    # Setting conditions to find the right target (and id).
    def startElement(self, name, attrs):
        if name == self.parent_element:
            self.id_value = attrs.getValue(self.attribute_name)
            if self.id_value == self.attribute_value:
                if self.target_element.lower():
                    self.is_inside_target = 1
                    self.id_value = None
            elif not self.id_value:
                raise ValueError(f"Couldnt find the {self.parent_element} element with {self.attribute_name} {self.attribute_value}")
            else:
                self.id_value = None
                self.is_inside_target = 0

    # If the conditions from above are met, save the value/content in a string (target_text).
    def characters(self, value):
        if self.is_inside_target == 1 and self.target_element:
                self.target_text = value    
                self.is_text = 1


    # Closing the element-tag once processing is complete.
    def endElement(self, name):
        if name == self.target_element and self.is_inside_target == 1:
            if self.is_text == 1:
                print("Text", self.target_text if self.target_text else "No value")
            self.is_inside_target = 0
            self.id_value = None

    # Presents a message when the parsing is done.
    def endDocument(self):
        print('Finished!')


# Fill in parameters: attribute_name, attribute_value, parent_element, target_element.
handler = RetrieveTargetValue("id", "42007", "trans-unit", "target")
# Creates a parser
xml_parser = xml.sax.make_parser()
# Parse the custom handler
xml_parser.setContentHandler(handler)
# Path to file
xml_file = "sma_gentext.xml"

try:
    xml_parser.parse(open(xml_file))
except SAXParseException as e:
    print(f"XML-error: {e.getMessage()}")
except Exception as e:
    print(f"Unknown error: {str(e)}")


# Console message to the user
print(f"Value of target in {handler.parent_element} with ID {handler.attribute_value}: \n\t------> {handler.target_text} <------")

# Creating an output file in .json
with open("output.json", "w") as outfile:
    json.dump(handler.target_text, outfile)



