from torch import nn
import torch
import numpy as np
from typing import List


class LSTM(nn.Module):
    def __init__(self, output_size, hidden_size, n_layers=1):
        super(LSTM, self).__init__()
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.n_layers = n_layers
        self.LSTM = nn.LSTM(self.output_size, self.hidden_size, self.n_layers)
        self.dropout = nn.Dropout(0.2)
        self.fc = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, x, hidden):
        out, (h, c) = self.LSTM(x, hidden)
        out = self.dropout(out)
        x = self.fc(out)
        return x, (h, c)


def predict(
    list_item: List,
    net: LSTM,
    var_size: int,
    N_column: int,
    num_level: int,
    hide_neuron: int,
):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    h0 = torch.randn(num_level, hide_neuron).to(device)
    c0 = torch.randn(num_level, hide_neuron).to(device)
    for item in list_item:
        buf = np.zeros((var_size), dtype=np.float32)
        buf[item] += 1
        input_batch = torch.tensor([buf]).to(device)
        out, (h0, c0) = net(input_batch, (h0, c0))
    return out.argsort(descending=True)[0][:N_column].cpu().detach().numpy()
