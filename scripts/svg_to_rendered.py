#!/usr/bin/python3
"""
Generates README.md with rendered versions of the provided images
"""

import os, glob, cairosvg, PIL

iconRoots = ["../logo", "../icons"]

output_folder = "rendered"
output_width = 2000

for iconRoot in iconRoots:
    root = os.path.abspath(iconRoot)
    rendered = os.path.join(root,output_folder)
    readme = os.open(os.path.join(root, "README.md"),
                     os.O_RDWR | os.O_CREAT)

    os.makedirs(rendered, exist_ok = True)

    for svg in sorted(glob.glob(os.path.join(root,"*.svg"))):
        base = svg.removesuffix(".svg")
        filename = base.split("/")[-1]

        # generate png from svg
        png = os.path.join(rendered, filename + ".png")
        cairosvg.svg2png(url=svg, write_to=png, output_width=output_width)
        svg.removesuffix(".svg") + ".png"

        # generate webp from png
        webp = os.path.join(rendered, filename + ".webp")
        image = PIL.Image.open(png)
        image.save(webp, format="webp")

        svg = filename+".svg"
        png = os.path.join(output_folder,filename+".png")
        webp = os.path.join(output_folder,filename+".webp")

        text = f"## {filename}\n\n"
        text += "\n".join([f"### {x}\n![{x}]({x})\n" for x in [svg, png, webp]])+"\n"

        os.write(readme,str.encode(text))

    os.close(readme)