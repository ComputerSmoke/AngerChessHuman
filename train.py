from keras.preprocessing import sequence
import keras
import tensorflow as tf
import os
import numpy as np
from tensorflow.keras import datasets, layers, models
import loadFens

#prep gpu
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)

def filterByTurn(maps, outs, turns, tt):
    retmaps = []
    retouts = []
    for i,turn in enumerate(turns):
        if turn == tt:
            retmaps.append(maps[i])
            retouts.append(outs[i])
    return np.array(retmaps),np.array(retouts)

def load_model(turn):
    model = models.Sequential()
    model.add(layers.Conv2D(1000, (3, 3), activation='relu', input_shape=(8, 8, 12)))
    model.add(layers.Conv2D(1000, (3, 3), activation='relu'))
    model.add(layers.Conv2D(1000, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(2000, activation='relu'))
    model.add(layers.Dense(1000, activation='relu'))
    model.add(layers.Dense(1000, activation='sigmoid'))
    model.add(layers.Dense(1000, activation='sigmoid'))
    model.add(layers.Dense(1000, activation='relu'))
    model.add(layers.Dense(3, activation='softmax'))
    base_learning_rate = 0.00001

    model.compile(optimizer=tf.keras.optimizers.RMSprop(lr=base_learning_rate), 
                loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                metrics=['accuracy'])
    try:
        model.load_weights(tf.train.latest_checkpoint("checkpoints"+str(turn)))
    except:
        pass

    callback = tf.keras.callbacks.ModelCheckpoint(filepath="checkpoints"+str(turn),save_weights_only=True)
    return model, callback

print("loading data")
bitmaps,turns,outcomes,skipCount = loadFens.get_data(1000, 10000)

print("Splitting data")
bitmaps0,outcomes0 = filterByTurn(bitmaps, outcomes, turns, 0)
bitmaps1,outcomes1 = filterByTurn(bitmaps, outcomes, turns, 1)
print(bitmaps0[0])


black_model,black_callback = load_model(0)
white_model,white_callback = load_model(1)
print(len(outcomes0), len(bitmaps0))
epochs = 100
print("Training Black")
black_model.fit(
    bitmaps0,
    outcomes0,
    epochs=epochs,
    callbacks=[black_callback]
)
model.save("./model0")
print("Training White")
white_model.fit(
    bitmaps1,
    outcomes1,
    epochs=epochs,
    callbacks=[white_callback]
)
model.save("./model1")
