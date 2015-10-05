import sys
from xml.sax.saxutils import XMLGenerator
from xml.sax.xmlreader import AttributesImpl

g = XMLGenerator(open("test.xml","w"), 'utf-8')

def start_tag(name, attr={}, body=None):
    attr2 = AttributesImpl(attr)
    g.startElement(name, attr2)
    if body:
        g.characters(body)

def end_tag(name):
    g.endElement(name)

def tag(name, attr={}, body=None):
    start_tag(name, attr, body)
    end_tag(name)


some_list = [
    ("item0", "item-0-title", "item-0-desc"),
    ("item1", "item-1-title", "item-1-desc"),
    ("item2", "item-2-title", "item-2-desc"),
    ("item3", "item-3-title", "item-3-desc"),
    ("item4", "item-4-title", "item-4-desc"),
    ("item5", "item-5-title", "item-5-desc"),
    ("item6", "item-6-title", "item-6-desc"),
    ("item7", "item-7-title", "item-7-desc"),
    ("item8", "item-8-title", "item-8-desc"),
    ("item9", "item-9-title", "item-9-desc"),
]

g.startDocument()
print """<?xml version="1.0" encoding="utf-8'?>"""
start_tag(u'list', {u'id':str(10)})

for item in some_list:
    start_tag(u'item', {u'id': item[0]})
    tag(u'title', body=item[1])
    tag(u'desc', body=item[2])
    end_tag(u'item')

end_tag(u'list')
g.endDocument()