from .utils.train import *
from .model.v1_model import *
from torch import autograd
from .utils import readdata
import torch.optim as optim
import os

VOCAB_SIZE = len(readdata.word_to_ix)
NUM_LABELS = 2  # ENGLISH  SPANISH


class predict():
    def __init__(self, model_save_path):
        self.model = BoWClassifier(NUM_LABELS, VOCAB_SIZE)
        self.optimizer = optim.SGD(self.model.parameters(), lr=0.1)
        self.model_save_path = model_save_path

    def train(self):
        Train(self.model, self.optimizer, self.model_save_path)

    def predict(self, data):
        print('==================')
        if os.path.exists(self.model_save_path):
            checkpoint = torch.load(model_save_path)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            self.model.eval()
            print('saved model is used')
        else:
            self.train()

        for instance, label in data:
            bow_vec = autograd.Variable(
                make_bow_vector(instance, readdata.word_to_ix))
            log_probs = self.model(bow_vec)
            print(log_probs)
        return log_probs


model_save_path = 'app/Algs/pre_trained/v1_model.pkl'
s = predict(model_save_path)
s.predict(readdata.test_data)
