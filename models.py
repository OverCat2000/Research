import torch
import torch.nn as nn

class CNN3D(nn.Module):

    def __init__(self, in_channels, num_classes):
        super(CNN3D, self).__init__()

        self.conv = nn.Conv3d(in_channels=in_channels, out_channels=4, kernel_size=(2, 3, 3), padding=1)
        self.fc = nn.Linear(2420, num_classes)

    def forward(self, x):

        x = self.conv(x)
        x = torch.relu(x)
        x = torch.flatten(x, start_dim=1)
        x = self.fc(x)

        return x

class CNN2D(nn.Module):
    def __init__(self, in_channels, num_classes, dropout_prob, filters, fix):
        super(CNN2D, self).__init__()

        self.conv1 = nn.Conv2d(in_channels=in_channels, out_channels=filters, kernel_size=2, padding=2)
        self.dropout1 = nn.Dropout(p=dropout_prob)
        
        self.conv2 = nn.Conv2d(in_channels=filters, out_channels=filters, kernel_size=2, padding=2)
        self.dropout2 = nn.Dropout(p=dropout_prob)
        
        self.fc = nn.Linear(fix*fix*16, num_classes)

    def forward(self, x):

        x = self.conv1(x)
        x = torch.relu(x)
        x = self.dropout1(x)
        
        x = self.conv2(x)
        x = torch.relu(x)
        x = self.dropout2(x)
        
        x = torch.flatten(x, start_dim=1)
        x = self.fc(x)

        return x

class CNN1D(nn.Module):
    def __init__(self, in_channels, num_classes, dropout_prob, filters):
        super(CNN1D, self).__init__()

        self.conv1 = nn.Conv1d(in_channels=in_channels, out_channels=filters, kernel_size=2, padding=1)
        self.dropout1 = nn.Dropout(p=dropout_prob)
        
        self.conv2 = nn.Conv1d(in_channels=filters, out_channels=filters, kernel_size=2, padding=1)
        self.dropout2 = nn.Dropout(p=dropout_prob)

        self.fc = nn.Linear(13 * filters, num_classes)

    def forward(self, x):
        x = self.conv1(x)
        x = torch.relu(x)
        x = self.dropout1(x)

        x = self.conv2(x)
        x = torch.relu(x)
        x = self.dropout2(x)

        x = torch.flatten(x, start_dim=1)
        x = self.fc(x)

        return x

class MLP(nn.Module):
    def __init__(self, input_dim, num_classes, hidden_dim=64, dropout_prob=0.3):
        super(MLP, self).__init__()

        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.dropout1 = nn.Dropout(p=dropout_prob)

        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.dropout2 = nn.Dropout(p=dropout_prob)

        self.fc3 = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        
        x = torch.relu(self.fc1(x))
        x = self.dropout1(x)

        x = torch.relu(self.fc2(x))
        x = self.dropout2(x)

        x = self.fc3(x)

        return x
