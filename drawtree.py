# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# drawtree.py # # # # # # # # # # # # # # # # # # # # # # # # # # #
# created by: jordan bonecutter # # # # # # # # # # # # # # # # # #
# copyright - all rights reserved # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import cairo
import math
from treehelper import num_nodes, num_ad_nodes, get_url

maxurl = 30
def draw_tree_pdf(tree, fname):
    # get the layout of the tree
    fhandle = open(fname, "wb")
    structure = [{} for _ in range(len(tree))]
    i = 0
    for level in tree:
        j = 0
        curr = structure[i]
        for key in level.keys():
            curr.update({key:j})
            j += 1
        i += 1
    typecolors = {"": (150, 150, 150), "Other": (150, 150, 150), "unknown": (150, 150, 150)}
    typecolors.update({"Image": (230, 230, 20)})
    typecolors.update({"Stylesheet": (20, 230, 100)})
    typecolors.update({"Script": (255, 20, 20)})
    typecolors.update({"EventSource": (20, 230, 100)})
    typecolors.update({"Font": (20, 230, 100)})
    typecolors.update({"Media": (255, 20, 20)})
    typecolors.update({"Fetch": (230, 230, 20)})
    typecolors.update({"Document": (230, 230, 20)})
    typecolors.update({"XHR": (230, 230, 20)})

    # get the height and max width
    # of the tree
    h = len(structure)
    w = 0
    for level in structure:
        if len(level) > w:
            w = len(level)

    # picture parameters
    rad   = 200
    bufx  = 100
    bufy  = 300
    thck  = 10
    tsize = 50
    tbuf  = 6

    # create a new image
    while True:
        try:
            # get the image size
            size = (bufx + w*(bufx+(2*rad)), bufy + h*(bufy+(2*rad)))
            surface = cairo.PDFSurface(fhandle, size[0], size[1])
            break
        except cairo.Error:
            rad   = int(rad/2)
            bufx  = int(bufx/2)
            bufy  = int(bufy/2)
            thck  = int(thck/2)
            tsize = int(tsize/2)
            tbuf  = int(tbuf/2)

    ctx     = cairo.Context(surface)
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0,0,size[0], size[1])
    ctx.fill()

    fnt = cairo.ToyFontFace("Menlo", cairo.FontSlant.NORMAL, cairo.FontWeight.NORMAL)
    opt = cairo.FontOptions()
    fnt = cairo.ScaledFont(fnt, cairo.Matrix(size[0]/60,0,0,size[0]/60,0,0),cairo.Matrix(1,0,0,1,0,0), opt)
    ctx.set_scaled_font(fnt)
    nnt = str(num_nodes(tree))
    net = str(num_ad_nodes(tree, True))
    nit = str(num_ad_nodes(tree, False))
    inf = str(nnt+","+net+","+nit)
    ext = fnt.text_extents(inf)
    ctx.move_to(0, ext.height)

    ctx.set_source_rgb(50/255,20/255,255/255)
    ctx.show_text(nnt)
    ctx.set_source_rgb(0,0,0)
    ctx.show_text(",")
    ctx.set_source_rgb(255/255,20/255,50/255)
    ctx.show_text(net)
    ctx.set_source_rgb(0,0,0)
    ctx.show_text(",")
    ctx.set_source_rgb(255/255,20/255,200/255)
    ctx.show_text(nit)
    ctx.stroke()

    fnt = cairo.ToyFontFace("Menlo", cairo.FontSlant.NORMAL, cairo.FontWeight.NORMAL)
    opt = cairo.FontOptions()
    fnt = cairo.ScaledFont(fnt, cairo.Matrix(tsize, 0, 0, tsize, 0, 0), cairo.Matrix(1, 0, 0, 1, 0, 0), opt)
    ctx.set_scaled_font(fnt)

    ctx.set_line_cap (cairo.LineCap.BUTT)
    ctx.set_line_join(cairo.LineJoin.ROUND)
    ctx.set_line_width(thck)

    # draw!
    plev = -1
    c0xp = 0
    c0yp = 0
    slen = len(structure)
    # iterate through the levels of the tree
    for level in range (0, len(structure)):
        # get the width of the current level
        llen = len(structure[level])

        # find the x center coordinate
        ctr = size[0]/2
        rng = llen*(2*rad) + (llen-1)*bufx
        c0x = ctr - (rng/2) + rad

        # find the y center coordinate
        ctr = size[1]/2
        rng = slen*(2*rad) + (slen-1)*bufy
        c0y = ctr - (rng/2) + rad
        cy  = c0y + level*(2*rad + bufy)

        # calculate number of unique parents
        puni = {}
        index = 0
        for child in tree[level]:
            for parent in tree[level][child]["parents"]:
                if parent not in puni:
                    puni.update({parent: index})
                    index += 1

        for item in structure[level].keys():
            if tree[level][item]["ad"] == "yes":
                color = (255/255, 20/255, 50/255)
            elif tree[level][item]["ad"] == "no":
                color = (50/255, 20/255, 255/255)
            else:
                color = (255/255, 20/255, 200/255)

            # since we are iterating "horizontally", we
            # need only update the x position
            cx  = c0x + structure[level][item]*(2*rad + bufx)

            # if we aren't at the top level then
            # draw a line connecting it to its parent(s)
            if plev != -1:
                thisp    = 0
                thisptot = len(tree[level][item]["parents"])
                # iterate through parents
                for parent in tree[level][item]["parents"].keys():

                    # get the index of the parent
                    pindex = structure[level-1][parent]
                    cpx    = c0xp + (pindex)*(2*rad + bufx)
                    cpy    = c0yp
                
                    # get the width of the parent layer
                    plsize = len(puni)
                    # calculate on offset so that lines dont intersect
                    offy = int((puni[parent]+2)*bufy/(plsize+3))
                    ofrx = int((thck*(thisptot-1)) + (2*thck*(thisptot-1)))
                    of0x = int(-ofrx/2)
                    offx = int(of0x + thisp*ofrx/thisptot)
                    # draw 3 lines to connect the parent and child
                    ctx.move_to(cx+offx, cy-0.5*rad)
                    ctx.line_to(cx+offx, cy-rad-offy)
                    ctx.line_to(cpx    , cy-rad-offy)
                    ctx.line_to(cpx    , cpy+rad)
                    ctx.stroke()

                    thisp += 1

            
            # draw centered text
            try:
                sqtxt = str(tree[level][item]["squish"])
            except KeyError:
                sqtxt = ""

            # draw the circle + text
            ctx.set_source_rgb(color[0], color[1], color[2])
            ctx.arc(cx, cy, rad, 0, 2*math.pi)
            ctx.fill()

            if "types" in tree[level][item]:
                ntypes = len(tree[level][item]["types"])
                if ntypes == 1:
                    try: 
                        color = typecolors[list(tree[level][item]["types"])[0]]
                    except KeyError:
                        color = typecolors[""]
                    ctx.set_source_rgb(color[0]/255, color[1]/255, color[2]/255)
                    ctx.arc(cx, cy, rad+2*thck, 0, math.pi*2)
                    ctx.stroke()
                else:
                    for idt, t in enumerate(tree[level][item]["types"]):
                        try:
                            color = typecolors[t]
                        except KeyError:
                            color = typecolors[""]
                        ctx.set_source_rgb(color[0]/255, color[1]/255, color[2]/255)
                        a1 = math.fmod(idt*2*math.pi/ntypes+math.pi/2, math.pi*2)
                        a2 = math.fmod((idt+1)*2*math.pi/ntypes+math.pi/2, math.pi*2)
                        ctx.arc(cx, cy, rad+2*thck, a1, a2)
                        ctx.stroke()

            elif "type" in tree[level][item]:
                try:
                    color = typecolors[tree[level][item]["type"]]
                except:
                    color = typecolors[""]
                ctx.set_source_rgb(color[0]/255, color[1]/255, color[2]/255)
                ctx.arc(cx, cy, rad+2*thck, 0, 2*math.pi)
                ctx.stroke()

            ctx.set_source_rgba(0, 0, 0, 1.0)

            ext = fnt.text_extents(get_url(item)[:maxurl])
            ctx.move_to(cx-ext.width/2, cy-tbuf)
            ctx.show_text(get_url(item)[:maxurl])

            ext = fnt.text_extents(sqtxt)
            ctx.move_to(cx-ext.width/2, cy+ext.height + tbuf)
            ctx.show_text(sqtxt)
            ctx.stroke()
        # remember the parent level and center
        # of the circle at the beginning of the parent level
        plev = level
        c0xp = c0x
        c0yp = cy

    # save the image
    ctx.show_page()

def draw_tree(tree, fname):
    # get the layout of the tree
    structure = [{} for _ in range(len(tree))]
    i = 0
    for level in tree:
        j = 0
        curr = structure[i]
        for key in level.keys():
            curr.update({key:j})
            j += 1
        i += 1
    typecolors = {"": (150, 150, 150), "Other": (150, 150, 150), "unknown": (150, 150, 150)}
    typecolors.update({"Image": (230, 230, 20)})
    typecolors.update({"Stylesheet": (20, 230, 100)})
    typecolors.update({"Script": (255, 20, 20)})
    typecolors.update({"EventSource": (20, 230, 100)})
    typecolors.update({"Font": (20, 230, 100)})
    typecolors.update({"Media": (255, 20, 20)})
    typecolors.update({"Fetch": (230, 230, 20)})
    typecolors.update({"Document": (230, 230, 20)})
    typecolors.update({"XHR": (230, 230, 20)})

    # get the height and max width
    # of the tree
    h = len(structure)
    w = 0
    for level in structure:
        if len(level) > w:
            w = len(level)

    # picture parameters
    rad   = 200
    bufx  = 100
    bufy  = 300
    thck  = 10
    tsize = 50
    tbuf  = 6

    # create a new image
    while True:
        try:
            # get the image size
            size = (bufx + w*(bufx+(2*rad)), bufy + h*(bufy+(2*rad)))
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, size[0], size[1])
            break
        except cairo.Error:
            rad   = int(rad/2)
            bufx  = int(bufx/2)
            bufy  = int(bufy/2)
            thck  = int(thck/2)
            tsize = int(tsize/2)
            tbuf  = int(tbuf/2)

    ctx     = cairo.Context(surface)
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0,0,size[0], size[1])
    ctx.fill()

    fnt = cairo.ToyFontFace("Menlo", cairo.FontSlant.NORMAL, cairo.FontWeight.NORMAL)
    opt = cairo.FontOptions()
    fnt = cairo.ScaledFont(fnt, cairo.Matrix(size[0]/60,0,0,size[0]/60,0,0),cairo.Matrix(1,0,0,1,0,0), opt)
    ctx.set_scaled_font(fnt)
    nnt = str(num_nodes(tree))
    net = str(num_ad_nodes(tree, True))
    nit = str(num_ad_nodes(tree, False))
    inf = str(nnt+","+net+","+nit)
    ext = fnt.text_extents(inf)
    ctx.move_to(0, ext.height)

    ctx.set_source_rgb(50/255,20/255,255/255)
    ctx.show_text(nnt)
    ctx.set_source_rgb(0,0,0)
    ctx.show_text(",")
    ctx.set_source_rgb(255/255,20/255,50/255)
    ctx.show_text(net)
    ctx.set_source_rgb(0,0,0)
    ctx.show_text(",")
    ctx.set_source_rgb(255/255,20/255,200/255)
    ctx.show_text(nit)
    ctx.stroke()

    fnt = cairo.ToyFontFace("Menlo", cairo.FontSlant.NORMAL, cairo.FontWeight.NORMAL)
    opt = cairo.FontOptions()
    fnt = cairo.ScaledFont(fnt, cairo.Matrix(tsize, 0, 0, tsize, 0, 0), cairo.Matrix(1, 0, 0, 1, 0, 0), opt)
    ctx.set_scaled_font(fnt)

    ctx.set_line_cap (cairo.LineCap.BUTT)
    ctx.set_line_join(cairo.LineJoin.ROUND)
    ctx.set_line_width(thck)

    # draw!
    plev = -1
    c0xp = 0
    c0yp = 0
    slen = len(structure)
    # iterate through the levels of the tree
    for level in range (0, len(structure)):
        # get the width of the current level
        llen = len(structure[level])

        # find the x center coordinate
        ctr = size[0]/2
        rng = llen*(2*rad) + (llen-1)*bufx
        c0x = ctr - (rng/2) + rad

        # find the y center coordinate
        ctr = size[1]/2
        rng = slen*(2*rad) + (slen-1)*bufy
        c0y = ctr - (rng/2) + rad
        cy  = c0y + level*(2*rad + bufy)

        # calculate number of unique parents
        puni = {}
        index = 0
        for child in tree[level]:
            for parent in tree[level][child]["parents"]:
                if parent not in puni:
                    puni.update({parent: index})
                    index += 1

        for item in structure[level].keys():
            if tree[level][item]["ad"] == "yes":
                color = (255/255, 20/255, 50/255)
            elif tree[level][item]["ad"] == "no":
                color = (50/255, 20/255, 255/255)
            else:
                color = (255/255, 20/255, 200/255)

            # since we are iterating "horizontally", we
            # need only update the x position
            cx  = c0x + structure[level][item]*(2*rad + bufx)

            # if we aren't at the top level then
            # draw a line connecting it to its parent(s)
            if plev != -1:
                thisp    = 0
                thisptot = len(tree[level][item]["parents"])
                # iterate through parents
                for parent in tree[level][item]["parents"].keys():

                    # get the index of the parent
                    pindex = structure[level-1][parent]
                    cpx    = c0xp + (pindex)*(2*rad + bufx)
                    cpy    = c0yp
                
                    # get the width of the parent layer
                    plsize = len(puni)
                    # calculate on offset so that lines dont intersect
                    offy = int((puni[parent]+2)*bufy/(plsize+3))
                    ofrx = int((thck*(thisptot-1)) + (2*thck*(thisptot-1)))
                    of0x = int(-ofrx/2)
                    offx = int(of0x + thisp*ofrx/thisptot)
                    # draw 3 lines to connect the parent and child
                    ctx.move_to(cx+offx, cy-0.5*rad)
                    ctx.line_to(cx+offx, cy-rad-offy)
                    ctx.line_to(cpx    , cy-rad-offy)
                    ctx.line_to(cpx    , cpy+rad)
                    ctx.stroke()

                    thisp += 1

            
            # draw centered text
            try:
                sqtxt = str(tree[level][item]["squish"])
            except KeyError:
                sqtxt = ""

            # draw the circle + text
            ctx.set_source_rgb(color[0], color[1], color[2])
            ctx.arc(cx, cy, rad, 0, 2*math.pi)
            ctx.fill()

            if "types" in tree[level][item]:
                ntypes = len(tree[level][item]["types"])
                if ntypes == 1:
                    try: 
                        color = typecolors[list(tree[level][item]["types"])[0]]
                    except KeyError:
                        color = typecolors[""]
                    ctx.set_source_rgb(color[0]/255, color[1]/255, color[2]/255)
                    ctx.arc(cx, cy, rad+2*thck, 0, math.pi*2)
                    ctx.stroke()
                else:
                    for idt, t in enumerate(tree[level][item]["types"]):
                        try:
                            color = typecolors[t]
                        except KeyError:
                            color = typecolors[""]
                        ctx.set_source_rgb(color[0]/255, color[1]/255, color[2]/255)
                        a1 = math.fmod(idt*2*math.pi/ntypes+math.pi/2, math.pi*2)
                        a2 = math.fmod((idt+1)*2*math.pi/ntypes+math.pi/2, math.pi*2)
                        ctx.arc(cx, cy, rad+2*thck, a1, a2)
                        ctx.stroke()

            elif "type" in tree[level][item]:
                try:
                    color = typecolors[tree[level][item]["type"]]
                except:
                    color = typecolors[""]
                ctx.set_source_rgb(color[0]/255, color[1]/255, color[2]/255)
                ctx.arc(cx, cy, rad+2*thck, 0, 2*math.pi)
                ctx.stroke()

            ctx.set_source_rgba(0, 0, 0, 1.0)

            ext = fnt.text_extents(get_url(item)[:maxurl])
            ctx.move_to(cx-ext.width/2, cy-tbuf)
            ctx.show_text(get_url(item)[:maxurl])

            ext = fnt.text_extents(sqtxt)
            ctx.move_to(cx-ext.width/2, cy+ext.height + tbuf)
            ctx.show_text(sqtxt)
            ctx.stroke()
        # remember the parent level and center
        # of the circle at the beginning of the parent level
        plev = level
        c0xp = c0x
        c0yp = cy

    # save the image
    surface.write_to_png(fname)
