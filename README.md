
# Work sample - extracting an element value from an XML file

## Update!!
* I added this snippet to notify the user if element doesnt contain a value, I feel a bit foolish since the solution was actually quite simple. I attempted to implement it within both characters-method and endElement-method, but without success. However I then realized (during a shower) that this gets the job done.

```python
if handler.target_text.strip() == "" or None:
    print(f"{handler.target_element} doesnt contain a value")
else:
    print(f"Value of target in {handler.parent_element} with ID {handler.attribute_value}: \n\t------> {handler.target_text} <------")
```

## Strategy
* As I had no prior experience working with XML, the research begun. I ended up at W3schools and found out about XPath, this became my initial solution for the work sample: a combination of the xml.Etree-parser and Xpath. A rather simplistic solution, with the main logic is captured in this code snippet:

```python
x_path = f".//{element}[@id='{attribute}']/target"
```  

* Although the code itself accomplished the job, I couldnt shake off the recruiter's advice: *"Let the problem sink in"*. It took a few more days and all of a sudden it struced me like lightning: why is the ID such a high number? Back to the drawing board. 
The high ID number led me to consider that the document might just be a part of a larger, a much larger document. I discovered the possibility of streaming the XML-file instead of just loading everything into memory.
I found a couple of interesting parsers for this purpose, but I opted for the use of **xml.sax (Simple API for XML)**. First, its a read-only parser, which suits the problem perfect, extract an element value. Secondly, as the file could potentially be a substantial chunk of code, streaming is an ideal solution, taking memory allocation in consideration.


## Sources
- *https://docs.python.org/3/library/xml.sax.handler.html#contenthandler-objects*
- *https://nanonets.com/blog/parse-xml-files-using-python/*
- *https://vegibit.com/python-xml-parsing/*
- *Python & XML, av Christopher A. Jones, Fred L. Drake, O'Reilly (Chapter 1 - 3)*


## How to use the application
- This is where the user inputs the search values for the parse.
- **Attribute name, attribute value, parent element and the target element.**
```python
handler = RetrieveTargetValue("id", "42007", "trans-unit", "target")
```

## Code Comments
- The main idea of the code is to get to the right element with the right id value, then extract the chosen element value.
- Creating the class and instanziating object attributes in the constructor. 
```python
     class RetrieveTargetValue(ContentHandler):
        def __init__(self, attribute_name, attribute_value, parent_element, target_element):
            self.target_text = ""
            self.attribute_name = attribute_name
            self.attribute_value = attribute_value
            self.parent_element = parent_element
            self.target_element = target_element
            self.id_value = None
            self.is_inside_target = 0
```

- startElement is the first call-back method, this contains the main logic for the parsing. Checking for the right parent element, instanziating id_value with the value of id. Then checks for the id we are looking for. If we find it, we set a mark with the flag, is_inside_target. This is a signal for the next call-back method, characters. Reset the id_value and handle potential error in the code. 
```python
        def startElement(self, name, attrs):
            if name == self.parent_element:
                self.id_value = attrs.getValue(self.attribute_name)
            if self.id_value == self.attribute_value:
                self.is_inside_target = 1
                self.id_value = None
            elif not self.id_value:
                raise ValueError(f"Couldnt find the {self.parent_element} element with {self.attribute_name} {self.attribute_value}")
            else:
                self.id_value = None
                self.is_inside_target = 0
```

- I did stuggle here, as I tried to add some validation but it wouldnt work out as expected. I finally solved it, read update above.
- If the conditions from the startElement method is met and we are in the correct element, we assign value into target_text, this is where the extraction of the element value occurs. 
```python
         def characters(self, value):
            if self.is_inside_target == 1 and self.target_element:
                self.target_text = value
```


- Checks if the current element name matches the target element and if its inside the target.
- Set the flag to 0 and reset the value of id_value, this is due to the endElement not just searching the element we're looking for, but rather since its searching through every single element in the file.
```python
        def endElement(self, name):
            if name == self.target_element and self.is_inside_target == 1:
                self.is_inside_target = 0
                self.id_value = None
```


```python
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
if handler.target_text.strip() == "" or None:
    print(f"{handler.target_element} doesnt contain a value")
else:
    print(f"Value of target in {handler.parent_element} with ID {handler.attribute_value}: \n\t------> {handler.target_text} <------")

# Creating an output file in .json
with open("output.json", "w") as outfile:
    json.dump(handler.target_text, outfile)
```
=======

