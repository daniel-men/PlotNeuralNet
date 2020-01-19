
from .tikzeng import *

#define new block
def block_2ConvPool( name, botton, top, s_filer=256, n_filer=64, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5 ):
    return [
    to_ConvConvRelu( 
        name="ccr_{}".format( name ),
        s_filer=str(s_filer), 
        n_filer=(n_filer,n_filer), 
        offset=offset, 
        to="({}-east)".format( botton ), 
        width=(size[2],size[2]), 
        height=size[0], 
        depth=size[1],   
        ),    
    to_Pool(         
        name="{}".format( top ), 
        offset="(0,0,0)", 
        to="(ccr_{}-east)".format( name ),  
        width=1,         
        height=size[0] - int(size[0]/4), 
        depth=size[1] - int(size[0]/4), 
        opacity=opacity, ),
    to_connection( 
        "{}".format( botton ), 
        "ccr_{}".format( name )
        )
    ]


def block_Unconv( name, botton, top, s_filer=256, n_filer=64, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5 ):
    return [
        to_UnPool(  name='unpool_{}'.format(name),    offset=offset,    to="({}-east)".format(botton),         width=1,              height=size[0],       depth=size[1], opacity=opacity ),
        to_ConvRes( name='ccr_res_{}'.format(name),   offset="(0,0,0)", to="(unpool_{}-east)".format(name),    s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1], opacity=opacity ),       
        to_Conv(    name='ccr_{}'.format(name),       offset="(0,0,0)", to="(ccr_res_{}-east)".format(name),   s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1] ),
        to_ConvRes( name='ccr_res_c_{}'.format(name), offset="(0,0,0)", to="(ccr_{}-east)".format(name),       s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1], opacity=opacity ),       
        to_Conv(    name='{}'.format(top),            offset="(0,0,0)", to="(ccr_res_c_{}-east)".format(name), s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1] ),
        to_connection( 
            "{}".format( botton ), 
            "unpool_{}".format( name ) 
            )
    ]




def block_Res( num, name, botton, top, s_filer=256, n_filer=64, offset="(0,0,0)", size=(32,32,3.5), opacity=0.5 ):
    lys = []
    layers = [ *[ '{}_{}'.format(name,i) for i in range(num-1) ], top]
    for name in layers:        
        ly = [ to_Conv( 
            name='{}'.format(name),       
            offset=offset, 
            to="({}-east)".format( botton ),   
            s_filer=str(s_filer), 
            n_filer=str(n_filer), 
            width=size[2],
            height=size[0],
            depth=size[1]
            ),
            to_connection( 
                "{}".format( botton  ), 
                "{}".format( name ) 
                )
            ]
        botton = name
        lys+=ly
    
    lys += [
        to_skip( of=layers[1], to=layers[-2], pos=1.25),
    ]
    return lys


def conv_relu_pool(conv_name, pool_name, x_label, offset="(0,0,0)", to="(0,0,0)", depth=40, height=40, width=1):
    pool_offset = int(height/10)
    return "\n".join([
    to_ConvRelu(conv_name, offset=offset, to=to, width=width, height=height, depth=depth, x_label=str(x_label)),
    to_Pool(pool_name, to="({}-east)".format(conv_name), height=str(height-pool_offset), depth=str(depth-pool_offset))])

def dense_dropout(dense_name, drop_name, x_label, offset="(0,0,0)", to="(0,0,0)", depth=1, height=40, width=1):
    return "\n".join([
        dense_layer(dense_name, offset=offset, to=to, x_label=x_label, width=width, depth=depth, height=height),
        dropout_layer(drop_name, to="({}-east)".format(dense_name), width=width, depth=depth, height=height)
    ])