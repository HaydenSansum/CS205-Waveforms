from modelling_functions import gen_songs_from_pickle
from wavenet import create_wavenet

import numpy as np
import tensorflow as tf

data_path = "../../songs/pickle/"
model_path = "../../models/"
model_name = "basic_model_nf32_ns32"

song_train_data_generator = gen_songs_from_pickle(data_path, data_size=2048, n_stride=256, n_channels=256, batch_size=128, genres_to_train=['Dance'], shuffle=True, seed=205)

wavenet_model = create_wavenet(10, 256, [32, 128, 256, 512], 2)

adam_opt = tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False)
wavenet_model.compile(optimizer=adam_opt, loss='categorical_crossentropy')

wavenet_model.fit_generator(song_train_data_generator, epochs=1)

# Save model and weights out to disk
wavenet_json = wavenet_model.to_json()
with open(f"{model_path}{model_name}.json", "w") as save_model:
    save_model.write(wavenet_json)

wavenet_model.save_weights(f"{model_path}{model_name}.h5")
print(f"Model Training Complete & Model saved to {model_path}")
