import keras
from .blocks import *

def parse_model(model):
    arch = []
    config = model.get_config()
    skip = False
    for i, layer in enumerate(config["layers"]):
        script = ""
        if skip:
            skip = False
            continue

        layer_config = layer["config"]
        class_name = layer["class_name"]

        if class_name == "Conv2D":
            if config["layers"][i+1]["class_name"] == "MaxPooling2D":
                pool = config["layers"][i+1]
                script = conv_relu_pool()
                skip = True
            else:
                script = to_Conv()
                
        elif class_name == "Dense":
            if config["layers"][i+1]["class_name"] == "Dropout":
                drop = config["layers"][i+1]
                script = dense_dropout_layer()
                skip = true
        else:
            script = dense_layer()

        arch.append(script)
    return arch


