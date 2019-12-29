from app.Algs.recommend import s


def test_fake_alg():
    test_data = [("Yo creo que si".split(), "SPANISH"),
                 ("it is lost on me".split(), "ENGLISH")]

    log_probs = s.predict(test_data)
    assert log_probs[0][0] < log_probs[0][1]
