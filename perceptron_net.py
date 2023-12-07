import torch
import torch.nn as nn
import numpy as np


class PerceptronNet(nn.Module):
    def __init__(self, N):
        super(PerceptronNet, self).__init__()
        self.L1 = nn.Linear(N, 2 * N)
        self.L2 = nn.Linear(2 * N, 2 * N)
        self.L3 = nn.Linear(2 * N, N)
        self.relu = nn.ReLU()
        self.Softmax = nn.Softmax(1)

    def forward(self, x):
        x = self.relu(self.L1(x))
        x = self.relu(self.L2(x))
        x = self.relu(self.L3(x))
        return x


def predict(list, net, N, N_column):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    buf = np.zeros((N), dtype=np.float32)
    for el in list:
        buf[el] += 1
    inpyt = torch.tensor(buf).to(device)
    out = net(inpyt)
    return out.argsort(descending=True)[:N_column].cpu().detach().numpy()


def load_weights(net, path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net.load_state_dict(torch.load(path, map_location=device), strict=True)
    net = net.eval()
    return net
