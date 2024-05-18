import tensorflowjs as tfjs
from tensorflow.keras.models import Sequential, load_model

model_titles = ['families', 'germanic', 'hellenic', 'romance', 'slavic', 'uralic']


def convert(model_title):
  model = load_model(f'../models/model_{model_title}.keras')
  tfjs.converters.save_keras_model(model, f'./converted_models/model_{model_title}')
  print(f'Converted: {model_title}')


for m in model_titles:
  convert(m)
