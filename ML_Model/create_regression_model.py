import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

print(tf.__version__)

data = pd.read_csv('data/ML data/data_cleaned.csv')

train_dataset = data.sample(frac=0.8, random_state=0)
test_dataset = data.drop(train_dataset.index)

train_features = train_dataset.copy()
test_features = test_dataset.copy()

train_labels = train_features.pop('LapTimeQ')
test_labels = test_features.pop('LapTimeQ')

normalizer = tf.keras.layers.Normalization(axis=-1)

normalizer.adapt(np.array(train_features))

first = np.array(train_features[:1])

with np.printoptions(precision=2, suppress=True):
    print('First example:', first)
    print()
    print('Normalized:', normalizer(first).numpy())


def build_and_compile_model(norm):
    model = keras.Sequential([
        norm,
        layers.Dense(64, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(1)
    ])

    model.compile(loss='mean_absolute_error',
                  optimizer=tf.keras.optimizers.Adam(0.001),
                  )
    return model


dnn_model = build_and_compile_model(normalizer)
dnn_model.summary()

history = dnn_model.fit(
    train_features,
    train_labels,
    verbose=0,
    epochs=500)

results = dnn_model.evaluate(test_features, test_labels, verbose=0)

test_predictions = dnn_model.predict(test_features).flatten()

sample = pd.read_csv('data/ML data/testing_data_cleaned.csv')

result = pd.DataFrame()

for i in range(20):
    Vals = pd.DataFrame()
    temp = sample.iloc[i].to_frame().transpose()
    idx = temp.index[0]
    ActualTime = temp.loc[idx, 'LapTimeQ']
    PredictedTime = dnn_model.predict(temp.drop(columns=['DriverNumber', 'LapTimeQ']))[0][0]
    LapTime_Dif = (PredictedTime - ActualTime)
    Vals['Drv_No'] = temp['DriverNumber']
    Vals['ActualTime'] = ActualTime
    Vals['PredictedTime'] = PredictedTime
    Vals['LapTime_Dif'] = LapTime_Dif
    result = pd.concat((result, Vals), axis=0)
result = result.sort_values('ActualTime')
result['Actual_POS'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
result = result.sort_values('PredictedTime')
result['Predicted_POS'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
result['POS_Dif'] = result['Predicted_POS'] - result['Actual_POS']
print(result)

fig, ax = plt.subplots(figsize=(8, 8))

sns.scatterplot(data=result,
                x="LapTime_Dif",
                y="POS_Dif",
                ax=ax,
                hue="Drv_No",
                palette='tab10',
                s=80,
                linewidth=1,
                legend='auto',
                edgecolor='black')

ax.hlines(y=0, xmin=result['LapTime_Dif'].min(), xmax=result['LapTime_Dif'].max(), color='k', linestyles='dotted')
ax.vlines(x=0, ymin=result['POS_Dif'].min(), ymax=result['POS_Dif'].max(), color='k', linestyles='dotted')

plt.show()