import torch
import torch.nn as nn
import torch.nn.functional as F

class Network(nn.Module):
    def __init__(self, input_size, output_size):
        super(Network, self).__init__()
        self.fc = nn.Linear(input_size, output_size)

    def forward(self, x):
        x = self.fc(x)
        x = F.softmax(x, dim=x.dim()-1)  # Cela appliquera softmax sur la dernière dimension, qu'importe le shape de x
        return x