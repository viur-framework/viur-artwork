import os,re, math
from xml.dom.minidom import *
from svgelements import *

iconRoots = ["../logo", "../icons"]

blockList = ["dot"]

for iconRoot in iconRoots:
    for filename in os.listdir(iconRoot):
        if not filename.endswith(".svg"):
            continue

        filePath = os.path.join(iconRoot, filename)
        source = open(filePath,'r').read()

        if 'viewBox="0 0 60 60"' in source and filename.replace(".svg","") not in blockList:
            # update default viewBox
            svg = SVG.parse(filePath)
            viewBox = [math.ceil(v) for v in svg.bbox()]

            x = int(viewBox[0])-1
            y = int(viewBox[1])-1
            w = math.ceil(viewBox[2]-x)
            h = math.ceil(viewBox[3]-y)

            source = re.sub(r'viewBox=".*?"',f'viewBox="{x} {y} {w} {h}"', source)

        #remove comments
        source = re.sub(r'\n',"", source)
        source = re.sub(r'<!--.*?-->',"", source)
        source = re.sub(r'<!DOCTYPE svg.*?>',"", source)
        source = re.sub(r'<sodipodi:namedview.*?>',"", source)
        source = re.sub(r'<defs id=".*?/>',"", source)

        dom = parseString(source)

        #remove attributes
        for attribute in ["id","data-name","enable-background","version","x","y","xml:space","title","xmlns:xlink","style","xmlns:inkscape","xmlns:sodipodi","sodipodi:docname","inkscape:version","xmlns:serif"]:
            try:
                dom.firstChild.removeAttribute(attribute)
            except:pass

        #remove all titles
        titles = dom.getElementsByTagName("title")
        for title in titles:
            title.parentNode.removeChild(title)

        #replace all colors, for unique color icons
        elements = []
        #elements.extend(dom.getElementsByTagName("path"))
        #elements.extend(dom.getElementsByTagName("rect"))
        #elements.extend(dom.getElementsByTagName("polygon"))
        #elements.extend(dom.getElementsByTagName("ellipse"))
        #elements.extend(dom.getElementsByTagName("circle"))
        for path in elements:
            if path.getAttribute("fill"):
                path.setAttribute("fill","currentcolor")

        source= dom.toxml()
        source = source.replace('<?xml version="1.0" ?>','')
        source = re.sub(r'>( *)<',"><", source)
        source = re.sub(r'\t', "", source)
        f = open(filePath, 'w').write(source)
