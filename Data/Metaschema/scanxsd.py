from lxml import etree

types = []


def pf(val):
    return val.removeprefix('{http://www.w3.org/2001/XMLSchema}') if isinstance(val, str) else '<!--comment-->'


def process_element(element):
    if (tag := pf(element.tag)) in ('element', 'group', 'simpleType', 'complexType'):
        if 'name' in element.attrib:
            types.append({element.attrib['name']: tag})


def print_element(level, n, element):
    process_element(element)
    print(level*' .', n, pf(element.tag), dict(element.attrib))
    for k, child in enumerate(element, start=1):
        print_element(level+1, k, child)


parser = etree.XMLParser(remove_blank_text=True)
tree = etree.parse('metaschema.xsd', parser)
print('Errors:', len(tree.parser.error_log))
print_element(0, 1, tree.getroot())

