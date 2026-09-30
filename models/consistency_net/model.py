import torch
import torch.nn as nn

class MultiModalConsistencyNet(nn.Module):
    def __init__(self, input_dim=4, hidden_dim=64):
        super(MultiModalConsistencyNet, self).__init__()
        
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim // 2, 1),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        """
        x: shape (batch_size, 4)
        Returns consistency probability (0.0 to 1.0)
        """
        return self.net(x)
