import xml.etree.ElementTree as ET


def getTargetValue(xml_file, element, attribute):
    tree = ET.parse(xml_file)

    x_path = f".//{element}[@id='{attribute}']/target"

    target_value = tree.find(x_path)

    return target_value

result = getTargetValue('sma_gentext2.xml', 'trans-unit', '42007' )

print(result.text)

with open("output.txt", 'w') as outfile:
    outfile.write(result.text)

