from keras import backend as K

x = K.zeros((4, 4))
print(x)
print(x := K.clip(x, 1e-8, 1-1e-8))
