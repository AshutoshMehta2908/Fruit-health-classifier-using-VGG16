# -*- coding: utf-8 -*-
"""Fruits fresh,rotten classification, VGG16

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/#fileId=https%3A//storage.googleapis.com/kaggle-colab-exported-notebooks/fruits-fresh-rotten-classification-vgg16-70745655-0556-4c99-a882-49893481cefe.ipynb%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com/20240725/auto/storage/goog4_request%26X-Goog-Date%3D20240725T222852Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D3411fbaa2050cbdced27c4f3035b0a0d6c183afb848bef0bf9d0ec79e8344781dd3bafff0b6c00519bbadfe2c54661e9a7fe2730bf2dc2c8bbf2df6d8d7c6235e622723444946ebd926eda60be70bd8253e44fae22335db7e84106d9eb6893ef0ec5efe375252cd1211735c69f695fd0a1a64e8c04a1c2a16000a96ee3e09379864a8dd1ce4019eac251233aefde0b582259dbae600b33378754a6c64a940301ab1b911d8edbd6771ce972a6179f2140fe969066beff4a1d2e70b895a0edc362ebaa155c713c0e9c59b243e85de518d657e9831c593362058db798869e43fdba4330fa18d96ee95ae0764ff51297e32e85732cd1edc56e19806cd3c6195e9e5a
"""

# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES
# TO THE CORRECT LOCATION (/kaggle/input) IN YOUR NOTEBOOK,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.

import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'fruits-dataset-for-classification:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F4381992%2F7522318%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240725%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240725T222852Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D819675b30b5ff8762ae54d1417a20f3e81f886f3807fe3e7b67df2801f41cd75505682ee2a4187566489c31d94619e074ce945e44895bfbf033aafb1aec0196dcf0eadaefce9e40314a08044c2252fabf4aa2d5ed9de9d26801c8beb89c401b8f3a9acc78ff7f2818b6b621621c5ed3e63e74ccdf7bda6f3f42ee1fd778e1e72dc7f014a4ed3a24868da86117bad66bafc090ccce46fc1f0ace602c7d3d900ff56a59fbef0c9117ed3c74d4be68d892b4483ddbf44d48f2aadf76f77019e081d81aa3a6dc010fc76881f3d6774b57831abd04a9162f47c59ed50fe9ec41bcef49c63ea9cba18a056ad5bb8d8ee793fe24a85b3d173721735a6d67f4b972207f6'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

!umount /kaggle/input/ 2> /dev/null
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

import os
import cv2
import keras
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pandas as pd
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications import VGG16
import keras
import tensorflow as tf

"""### Read Data"""

furits="/kaggle/input/fruits-dataset-for-classification"
os.listdir(furits)

images=[]
labels=[]
for i,file in  enumerate(os.listdir(furits)):
    for img in os.listdir(os.path.join(furits,file)):
        im=(os.path.join(furits,file,img))
        images.append(im)
        labels.append(i)

"""### chek data balance"""

class_title={0:'fresh_peaches_done',
             1:'fresh_pomegranates_done',
             2:'fresh_strawberries_done',
             3:'rotten_peaches_done',
             4:'rotten_pomegranates_done',
             5:'rotten_strawberries_done'}



result=[]
for i in range(6):
    result.append({"label":class_title[i],"count":labels.count(i)})

df=pd.DataFrame(result)
df["count"].plot(kind="pie",labels=df['label'].values,autopct='%1.1f%%')

from sklearn.utils import resample
import pandas as pd

min_class =min(labels.count(i) for i in range(6))
balance_labels=[]
balance_images=[]

for i in range(6):
    class_indices=[index for index,label in enumerate(labels) if label ==i]
    balanced_indices=resample(class_indices,replace=True,n_samples=min_class,random_state=42)
    balance_labels.extend([labels[index] for index in balanced_indices])
    balance_images.extend([images[index] for index in balanced_indices])

"""### display data after balanced"""

result_balanced=[]
for i in range(6):
    result_balanced.append({"label_balanced":class_title[i],"count_balanced":balance_labels.count(i)})

df_balanced=pd.DataFrame(result_balanced)
df_balanced["count_balanced"].plot(kind="pie",labels=df_balanced['label_balanced'].values,autopct='%1.1f%%')

"""### Split Data"""

x_train,x_test,y_train,y_test=train_test_split(balance_images,balance_labels,test_size=0.2,random_state=42)

from sklearn.utils.class_weight import compute_class_weight
import numpy as np

# class_weights=compute_class_weight(class_weight='balanced',classes=np.unique(y_train),y=y_train)
# class_weights_dict=dict(enumerate(class_weights))

y_train=list(map(str,y_train))
y_test=list(map(str,y_test))

"""### Data agumention"""

train_datagen=ImageDataGenerator(

                        rescale=1./255.0,
                        rotation_range=40,
                        width_shift_range=0.2,
                        height_shift_range=0.2,
                        shear_range=0.2,
                        zoom_range=0.2,
                        horizontal_flip=True,
                )

test_datagen=ImageDataGenerator(rescale=1.0/255)

train_genertor=train_datagen.flow_from_dataframe(

                    dataframe=pd.DataFrame({'imgs':x_train,'labels':y_train}),
                    x_col='imgs'
                    ,y_col='labels',
                    target_size=(224,224),
                    class_mode="categorical",
                    shuffle=False,
                    batch_size=64,
                )


test_genertor=test_datagen.flow_from_dataframe(
                    dataframe=pd.DataFrame({'imgs':x_test,'labels':y_test}),
                     x_col='imgs'
                    ,y_col='labels',
                    target_size=(224,224),
                    class_mode="categorical",
                    shuffle=False,
                    batch_size=64,
                )



"""### Display some of images"""

fig,ax=plt.subplots(6,3,figsize=(8,15))
classes=list(range(6))

for class_idx in classes:
    for i in range(3):
        img,label=next(train_genertor)
        for idx,val in enumerate(label[0]):
            if val==1:
                x=idx
                break
        ax[class_idx,i].imshow(img[0])
        ax[class_idx,i].set_title(class_title[x])
plt.tight_layout()
plt.show()

"""### Bulid model structure"""

Model=VGG16(include_top=False,weights='imagenet',pooling='avg',input_shape=(224,224,3))

for layer in Model.layers:
   layer.trainable=False

model=keras.Sequential()
model.add(Model)
model.add(keras.layers.Dense(256,activation="relu"))
model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Dense(128,activation="relu"))
model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Dense(6,activation="softmax"))
model.summary()

model.compile(
optimizer=keras.optimizers.Adam(learning_rate=0.001),
loss=keras.losses.CategoricalCrossentropy(),
metrics=["accuracy"],
)

history = model.fit(train_genertor,validation_data=test_genertor,verbose=2,epochs=30,steps_per_epoch=len(train_genertor.classes)//64)

fig, ax = plt.subplots(1,2, figsize=(10, 8))

ax[0].plot(history.history['accuracy'], label='accuracy')
ax[0].plot(history.history['val_accuracy'], label='val_accuracy')
ax[0].set_xlabel('Epoch')
ax[0].set_ylabel('Accuracy')
ax[0].legend()

ax[1].plot(history.history['loss'], label='loss')
ax[1].plot(history.history['val_loss'], label='val_loss')
ax[1].set_xlabel('Epoch')
ax[1].set_ylabel('Loss')
ax[1].legend()

plt.tight_layout()
plt.show()

