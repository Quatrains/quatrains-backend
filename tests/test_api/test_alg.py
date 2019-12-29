import sys
sys.path.insert(1, '../../app/Algs/')
import recommend


def test_fake_alg():
  test_data = [("Yo creo que si".split(), "SPANISH"),
              ("it is lost on me".split(), "ENGLISH")]  

  log_probs = predict.predict(test_data)
  assert log_probs[0] < log_probs[1]

  
