import torch.nn as nn 
import torch.nn.functional as F

class BoWClassifier(nn.Module):#nn.Module 这是继承torch的神经网络模板
    def __init__(self, num_labels, vocab_size): 
        super(BoWClassifier, self).__init__()
        self.linear = nn.Linear(vocab_size, num_labels)
    def forward(self, bow_vec):
        return F.log_softmax(self.linear(bow_vec))
