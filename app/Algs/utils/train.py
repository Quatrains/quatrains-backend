import torch
import torch.nn as nn 
from torch import autograd
import torch.nn.functional as F 
import torch.optim as optim 
from . import readdata

def make_bow_vector(sentence, word_to_ix):
    vec = torch.zeros(len(word_to_ix))
    for word in sentence:
        vec[word_to_ix[word]] += 1
    return vec.view(1, -1)

def make_target(label, label_to_ix):
    return torch.LongTensor([label_to_ix[label]])

label_to_ix = { "SPANISH": 0, "ENGLISH": 1 }

def Train(model, optimizer, model_save_path):
  loss_function = nn.NLLLoss()
#   optimizer = optim.SGD(model.parameters(), lr=0.1)

  for epoch in range(100):
      for instance, label in readdata.data:
          model.zero_grad()

          bow_vec = autograd.Variable(make_bow_vector(instance, readdata.word_to_ix))
          target = autograd.Variable(make_target(label, label_to_ix))

          log_probs = model(bow_vec)

          loss = loss_function(log_probs, target)
          loss.backward()
          optimizer.step()

        #   import pdb; pdb.set_trace()

          torch.save({
              'model_state_dict': model.state_dict(),
              'optimizer_state_dict': optimizer.state_dict()
          }, model_save_path)
