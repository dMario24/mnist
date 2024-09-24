from mnist.model import predict_digit, get_model_path
import os

def test_get_model_path():
  p = get_model_path()
  assert p == "/home/diginori/code/mnist/src/mnist/mnist240924.keras"

def test_predict_digit():

  my_path = __file__
  dir_name = os.path.dirname(my_path)
  png_path = os.path.join(dir_name, '0_1.png')
  r = predict_digit(png_path)
  assert r == 0