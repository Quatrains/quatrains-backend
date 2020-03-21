from app.extensions import predict


def test_predict():
   idx = predict.predict(["悼亡", "月"], [], [])

   assert idx != 0

