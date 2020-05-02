from .blocks import *

def ConvLayer(layer_config, offset, to):
    filters = layer_config["filters"]
    if filters > 100:
        factor = 3
    elif filters > 50:
        factor = 2
    else:
        factor = 1
    depth = int(filters / factor)
    height = int(filters / factor)
    width = int(filters / factor)
    return to_Conv(layer_config["name"], depth=depth, height=height, width=width)

def ConvReLuLayer(layer_config, offset, to):
    filters = layer_config["filters"]
    if filters > 100:
        factor = 3
    elif filters > 50:
        factor = 2
    else:
        factor = 1
    depth = int(filters / factor)
    height = int(filters / factor)
    width = int(filters / factor)
    return to_ConvRelu(layer_config["name"], depth=depth, height=height, width=layer_config["filters"], x_label='{{{{{},}}}}'.format(filters))

def ConvReLuPoolLayer(layer_config, pool_name, offset, to):
    filters = layer_config["filters"]
    if filters > 100:
        factor = 3
    elif filters > 50:
        factor = 2
    else:
        factor = 1
    depth = int(filters / factor)
    height = int(filters / factor)
    width = int(filters / factor)
    return conv_relu_pool(layer_config["name"], pool_name, x_label='{{{{{},}}}}'.format(filters), offset=offset, to=to, width=width, depth=depth, height=height)

def DenseLayer(layer_config, offset, to):
    units = layer_config["units"]
    if units > 100:
        factor = 3
    elif units > 50:
        factor = 2
    else:
        factor = 1
    height = int(units / factor)
    return dense_layer(layer_config["name"], offset, to, x_label='{{{{{},}}}}'.format(units), depth=1, height=height)

def DenseDropoutLayer(layer_config, drop_name, offset, to):
    units = layer_config["units"]
    if units > 100:
        factor = 3
    elif units > 50:
        factor = 2
    else:
        factor = 1
    height = int(units / factor)
    return dense_dropout(layer_config["name"], drop_name, x_label='{{{{{},}}}}'.format(units), offset=offset, to=to, height=height)

def DropoutLayer(layer_config, offset, to, label=False):
    if label:
        return dropout_layer(layer_config["name"], offset=offset, to=to, x_label='{{{{{},}}}}'.format(layer_config["rate"]))
    else:
        return dropout_layer(layer_config["name"], offset=offset, to=to)

def FlattenLayer(layer_config, offset, to):
    return flatten(layer_config["name"], offset=offset, to=to)

def legendBox(layer_class, offset="(0,-5,5)", to="(0,0,0)"):
    if layer_class == "Conv2D + ReLu":
        return to_ConvRelu(layer_class, offset=offset, to=to, width=3, height=3, depth=3, y_label=layer_class)
    elif layer_class == "Dense":
        return dense_layer(layer_class, offset=offset, to=to, width=3, height=3, depth=3, y_label=layer_class)
    elif layer_class == "Dropout":
        return dropout_layer(layer_class, offset=offset, to=to, width=3, height=3, depth=3, y_label=layer_class)
    elif layer_class == "Flatten":
        return flatten(layer_class, offset=offset, to=to, width=3, height=3, depth=3, y_label=layer_class)
    elif layer_class == "MaxPooling2D":
        return to_Pool(layer_class, offset=offset, to=to, width=3, height=3, depth=3, y_label=layer_class)
    else:
        raise Exception("Unknown layer: {}".format(layer_class))
