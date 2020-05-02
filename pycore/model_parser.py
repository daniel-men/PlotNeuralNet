import keras
from .layers import *

def parse_keras_model(model, legend=False):
    paths, multi_path = find_connections(model)
    arch = [to_head( '.' ),
    to_cor(),
    to_begin()]
    config = model.get_config()
    skip = False
    last_layer = ""
    legend_layers = set()
    layers = {l["config"]["name"]: l for l in config["layers"]}
    for i, layer in enumerate(layers):
        script = ""
        if skip:
            skip = False
            continue

        layer_config = layers[layer]["config"]
        class_name = layers[layer]["class_name"]

        if multi_path and layer not in paths:
            for d in [d for d in paths.values() if isinstance(d, dict)]:
                if layer in d:
                    pass

        if i == 0:
            offset = "(0,0,0)"
            to = "(0,0,0)"
        else:
            offset = "(1,0,0)"
            to = "({}-east)".format(last_layer)

        if class_name == "Conv2D":
            if i < len(config["layers"])-1 and config["layers"][i+1]["class_name"] == "MaxPooling2D":
                pool = config["layers"][i+1]
                script = ConvReLuPoolLayer(layer_config, pool_name=pool["config"]["name"], offset=offset, to=to)
                skip = True
                last_layer = pool["config"]["name"]
                legend_layers.add("Conv2D + ReLu")
                legend_layers.add("MaxPooling2D")
            else:
                if layer_config["activation"] == "relu":
                    script = ConvReLuLayer(layer_config, offset=offset, to=to)
                    legend_layers.add("Conv2D + ReLu")
                else:
                    script = ConvLayer(layer_config["name"], offset=offset, to=to)
                    legend_layers.add("Conv2D")
                last_layer = layer_config["name"]
                
        elif class_name == "Dense":
            if i < len(config["layers"])-1 and config["layers"][i+1]["class_name"] == "Dropout":
                drop = config["layers"][i+1]
                script = DenseDropoutLayer(layer_config, drop["config"]["name"], offset=offset, to=to)
                skip = True
                last_layer = drop["config"]["name"]
                legend_layers.add("Dropout")
            else:
                script = DenseLayer(layer_config, offset=offset, to=to)
                last_layer = layer_config["name"]
            legend_layers.add("Dense")

        elif class_name == "Dropout":
            script = DropoutLayer(layer_config, offset=offset, to=to)
            last_layer = layer_config["name"]
            legend_layers.add("Dropout")

        elif class_name == "Flatten":
            script = FlattenLayer(layer_config=layer_config, offset=offset, to=to)
            last_layer = layer_config["name"] 
            legend_layers.add("Flatten")       
        else:
            continue
        
        arch.append(script)

        for in_layer in model.layers[i]._inbound_nodes[0].inbound_layers:
            if "input" in in_layer.name:
                continue
            arch.append(to_connection("{}".format(in_layer.name), "{}".format(layer_config["name"])))
    
    if legend:
        to = "(0,0,0)"
        offset = "(0,-5,5)"
        for i, legend_layer in enumerate(legend_layers):            
            if i > 0:
                offset = "(0,-1,1)"
                to = "({}-north)".format(last_legend_layer)
            arch.append(legendBox(legend_layer, offset=offset, to=to))
            last_legend_layer=legend_layer

    arch.append(to_end())
    return arch

def find_connections(model):
    multi_path = False
    #model.get_config()["layers"].reverse()
    predecessors = {}

    if not any(["inbound_nodes" in layer for layer in model.get_config()["layers"]]):
        return model.get_config()["layers"], multi_path

    for layer in model.get_config()["layers"]:
        if "inbound_nodes" in layer:
            inbound_layers = layer["inbound_nodes"]
            if len(inbound_layers) > 0:
                inbound_layers = [il[0] for il in inbound_layers[0]]
                name = layer["config"]["name"]
                if name in predecessors:
                    predecessors[name].extend(inbound_layers)
                else:
                    predecessors[name] = inbound_layers

    paths = {}
    for layer, pre in predecessors.items():
        if len(pre) > 1:
            multi_path = True
            paths[layer] = pre
            for pred in pre:
                pred_orig = pred
                l = {}
                while pred in predecessors:
                    l[pred] = predecessors[pred]
                    pred = predecessors[pred][0]
                paths[pred_orig] = l
        else:
            paths[layer] = pre

    if multi_path:
        # Remove double entries from path
        for k,v in paths.copy().items():
            if isinstance(v, dict):
                for k_ in v:
                    if k == k_:
                        continue
                    paths.pop(k_)
    print(paths)
    return paths, multi_path
    


