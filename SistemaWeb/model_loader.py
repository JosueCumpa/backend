import tensorflow as tf

def load_model():
    model= tf.keras.models.load_model('SistemaWeb/modelos/modelo_final_94.h5')
    return model

modelo = load_model()