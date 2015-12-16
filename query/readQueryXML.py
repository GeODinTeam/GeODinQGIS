import xml.etree.ElementTree as ET

def createXmlDict(node):

    attributeList = node.attrib
    for child in node:
        tag = child.tag
        i=0
        while tag in attributeList:
           i+=1
           tag = child.tag+str(i)
        attributeList[tag] = createXmlDict(child)

    return attributeList

tree = ET.parse('TGClass_GQQuery.XML')
root = tree.getroot()
#print root.tag
#print root.attrib
#for child in root:
#    print child.tag, child.attrib
#print root.findall("*")[0].tag

#nodes = [root]
xmlDict = {}

#while nodes:
#    rootNode = nodes[0]
#    for child in rootNode:
#        nodes.append(child)
#        print child.tag,
#        print " : ",
#        print child.attrib
#    nodes.remove(rootNode)

xmlDict[root.tag] = createXmlDict(root)
print 
print xmlDict
