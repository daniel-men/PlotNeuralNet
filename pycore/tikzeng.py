
import os

def to_head( projectpath ):
    pathlayers = os.path.join( projectpath, 'layers/' ).replace('\\', '/')
    return r"""
\documentclass[border=8pt, multi, tikz]{standalone} 
\usepackage{import}
\subimport{"""+ pathlayers + r"""}{init}
\usetikzlibrary{positioning}
\usetikzlibrary{3d} %for including external image 
"""

def to_cor():
    return r"""
\def\ConvColor{rgb:yellow,5;red,2.5;white,5}
\def\ConvReluColor{rgb:yellow,5;red,5;white,5}
\def\PoolColor{rgb:red,1;black,0.3}
\def\UnpoolColor{rgb:blue,2;green,1;black,0.3}
\def\FcColor{rgb:blue,5;green,2.5;white,5}
\def\FcReluColor{rgb:blue,5;red,5;white,4}
\def\SoftmaxColor{rgb:magenta,5;black,7}   
\def\DropoutColor{rgb:yellow,5}
\def\FlattenColor{rgb:yellow,1;red,2;white,7}
"""

def to_begin():
    return r"""
\newcommand{\copymidarrow}{\tikz \draw[-Stealth,line width=0.8mm,draw={rgb:blue,4;red,1;green,1;black,3}] (-0.3,0) -- ++(0.3,0);}

\begin{document}
\begin{tikzpicture}
\tikzstyle{connection}=[ultra thick,every node/.style={sloped,allow upside down},draw=\edgecolor,opacity=0.7]
\tikzstyle{copyconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:blue,4;red,1;green,1;black,3},opacity=0.7]
"""

# layers definition

def to_input( pathfile, to='(-3,0,0)', width=8, height=8, name="temp" ):
    return r"""
\node[canvas is zy plane at x=0] (""" + name + """) at """+ to +""" {\includegraphics[width="""+ str(width)+"cm"+""",height="""+ str(height)+"cm"+"""]{"""+ pathfile +"""}};
"""

def base_layer(name, layer_type, fill_color, band_color=None, offset="(0,0,0)", to="(0,0,0)", width=2, height=40, depth=40, opacity=0.5, caption=None, x_label=None, y_label=None, z_label=None):
    line_storage = []
    pic_def = "\pic[shift={{ {} }}] at {}".format(offset, to)
    layer_def = "\t{{{}={{".format(layer_type)
    line_storage = [
        pic_def,
        layer_def,
        "\t\tname={},".format(name),
        "\t\tfill={},".format(fill_color),
        "\t\twidth={},".format(width),
        "\t\tdepth={},".format(depth),
        "\t\theight={},".format(height),
        "\t\topacity={},".format(opacity)
    ]

    if x_label:
        line_storage.append("\t\txlabel={},".format(x_label))

    if y_label:
        line_storage.append("\t\tylabel={},".format(y_label))

    if z_label:
        line_storage.append("\t\tzlabel={},".format(z_label))

    if caption:
        line_storage.append("\t\tcaption={},".format(caption))

    if band_color:
        line_storage.append("\t\tbandfill={},".format(band_color))

    line_storage.append("\t\t}")
    line_storage.append("\t};")
    return "\n".join(line_storage)

# Conv
def to_Conv( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" " ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +r""",
        xlabel={{"""+ str(n_filer) +""", }},
        zlabel="""+ str(s_filer) +""",
        fill=\ConvColor,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# Convolution + ReLu
def to_ConvRelu( name, offset="(0,0,0)", to="(0,0,0)", width=2, height=40, depth=40, x_label=None, y_label=None, z_label=None, caption=None):
    return base_layer(name, "RightBandedBox", "\\ConvColor", band_color="\\ConvReluColor", offset=offset, to=to, width=width, height=height, opacity=1., depth=depth, x_label=x_label, y_label=y_label, caption=caption)


# Conv,Conv,relu
# Bottleneck
def to_ConvConvRelu( name, s_filer=256, n_filer=(64,64), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40, caption=" " ):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {RightBandedBox={
        name="""+ name +""",
        caption="""+ caption +""",
        xlabel={{ """+ str(n_filer[0]) +""", """+ str(n_filer[1]) +""" }},
        zlabel="""+ str(s_filer) +""",
        fill=\ConvColor,
        bandfill=\ConvReluColor,
        height="""+ str(height) +""",
        width={ """+ str(width[0]) +""" , """+ str(width[1]) +""" },
        depth="""+ str(depth) +"""
        }
    };
"""



# Pool
def to_Pool(name, offset="(0,0,0)", to="(0,0,0)", x_label=None, y_label=None, z_label=None, width=1, height=32, depth=32, opacity=0.5, caption=None):
    return base_layer(name, "Box", "\\PoolColor", offset=offset, to=to, width=width, height=height, opacity=opacity, depth=depth, y_label=y_label, caption=caption)

# Flatten
def flatten(name, offset="(0,0,0)", to="(0,0,0)", y_label=" ", width=1, height=1, depth=20, opacity=0.5, caption=None):
    return base_layer(name, "Box", "\\FlattenColor", offset=offset, to=to, width=width, height=height, opacity=opacity, depth=depth, y_label=y_label, caption=caption)


# unpool4, 
def to_UnPool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5, caption=" "):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {Box={
        name="""+ name +r""",
        caption="""+ caption +r""",
        fill=\UnpoolColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""



def to_ConvRes( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=6, height=40, depth=40, opacity=0.2, caption=" " ):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {RightBandedBox={
        name="""+ name + """,
        caption="""+ caption + """,
        xlabel={{ """+ str(n_filer) + """, }},
        zlabel="""+ str(s_filer) +r""",
        fill={rgb:white,1;black,3},
        bandfill={rgb:white,1;black,2},
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""


# ConvSoftMax
def to_ConvSoftMax( name, s_filer=40, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" " ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +""",
        zlabel="""+ str(s_filer) +""",
        fill=\SoftmaxColor,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# SoftMax
def to_SoftMax( name, s_filer=10, offset="(0,0,0)", to="(0,0,0)", width=1.5, height=3, depth=25, opacity=0.8, caption=" " ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +""",
        xlabel={{" ","dummy"}},
        zlabel="""+ str(s_filer) +""",
        fill=\SoftmaxColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""


def dense_layer(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, opacity=1., x_label=None, y_label=None, z_label=None, caption=None):
    return base_layer(name, "Box", "\\FcColor", offset=offset, to=to, width=width, height=height, opacity=opacity, depth=depth, x_label=x_label, y_label=y_label, caption=caption)

def dropout_layer(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, opacity=1., x_label=None, y_label=None, z_label=None, caption=None):
    return base_layer(name, "Box", "\\DropoutColor", offset=offset, to=to, width=width, height=height, opacity=opacity, depth=depth, x_label=x_label, y_label=y_label, caption=caption)


def to_connection( of, to):
    return r"""
\draw [connection]  ("""+of+"""-east)    -- node {\midarrow} ("""+to+"""-west);
"""

def to_skip( of, to, pos=1.25):
    return r"""
\path ("""+ of +"""-southeast) -- ("""+ of +"""-northeast) coordinate[pos="""+ str(pos) +"""] ("""+ of +"""-top) ;
\path ("""+ to +"""-south)  -- ("""+ to +"""-north)  coordinate[pos="""+ str(pos) +"""] ("""+ to +"""-top) ;
\draw [copyconnection]  ("""+of+"""-northeast)  
-- node {\copymidarrow}("""+of+"""-top)
-- node {\copymidarrow}("""+to+"""-top)
-- node {\copymidarrow} ("""+to+"""-north);
"""

def to_end():
    return r"""
\end{tikzpicture}
\end{document}
"""


def to_generate( arch, pathname="file.tex" ):
    with open(pathname, "w") as f: 
        for c in arch:
            print(c)
            f.write( c )
     


