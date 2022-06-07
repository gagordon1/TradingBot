import torch
def load_NN(path):
    info = torch.load(path)
    model = info["Modules"][0]
    data = info["State"]
    state_dict = {}
    for key in data:
        state_dict[key[4:]] = data[key]
    model.load_state_dict(state_dict)
    return model