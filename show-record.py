#coding:utf-8
# $Id:$

from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
tf.enable_eager_execution()

import numpy as np
from IPython.display import display, Image
#import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# The following functions can be used to convert a value to a type compatible
# with tf.Example.

def _bytes_feature(value):
  """Returns a bytes_list from a string / byte."""
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _float_feature(value):
  """Returns a float_list from a float / double."""
  return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

def _int64_feature(value):
  """Returns an int64_list from a bool / enum / int / uint."""
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

##
def serialize_example(feature0, feature1, feature2, feature3):
  """
  Creates a tf.Example message ready to be written to a file.
  """

  # Create a dictionary mapping the feature name to the tf.Example-compatible
  # data type.

  feature = {
      'feature0': _int64_feature(feature0),
      'feature1': _int64_feature(feature1),
      'feature2': _bytes_feature(feature2),
      'feature3': _float_feature(feature3),
  }

  # Create a Features message using tf.train.Example.

  example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
  return example_proto.SerializeToString()

def _parse_image_function(example_proto):
  # Parse the input tf.Example proto using the dictionary above.
  return tf.parse_single_example(example_proto, image_feature_description)
def serialize_example_pyfunction(feature0, feature1, feature2, feature3):
  """
  Creates a tf.Example message ready to be written to a file.
  """

  # Create a dictionary mapping the feature name to the tf.Example-compatible
  # data type.

  feature = {
      'feature0': _int64_feature(feature0.numpy()),
      'feature1': _int64_feature(feature1.numpy()),
      'feature2': _bytes_feature(feature2.numpy()),
      'feature3': _float_feature(feature3.numpy()),
  }

  # Create a Features message using tf.train.Example.

  example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
  return example_proto.SerializeToString()

def tf_serialize_example(f0,f1,f2,f3):
  tf_string = tf.py_function(
    serialize_example_pyfunction,
    (f0,f1,f2,f3),  # pass these args to the above function.
    tf.string)      # the return type is `tf.string`.
  return tf.reshape(tf_string, ()) # The result is a scalar

# Create a dictionary with features that may be relevant.
def image_example(image_string, label):
  image_shape = tf.image.decode_jpeg(image_string).shape

  feature = {
      'height': _int64_feature(image_shape[0]),
      'width': _int64_feature(image_shape[1]),
      'depth': _int64_feature(image_shape[2]),
      'label': _int64_feature(label),
      'image_raw': _bytes_feature(image_string),
  }

  return tf.train.Example(features=tf.train.Features(feature=feature))
# Create a description of the features.
feature_description = {
    'feature0': tf.FixedLenFeature([], tf.int64, default_value=0),
    'feature1': tf.FixedLenFeature([], tf.int64, default_value=0),
    'feature2': tf.FixedLenFeature([], tf.string, default_value=''),
    'feature3': tf.FixedLenFeature([], tf.float32, default_value=0.0),
}

def _parse_function(example_proto):
  # Parse the input tf.Example proto using the dictionary above.
  return tf.parse_single_example(example_proto, feature_description)

#==============================================================================
# MANUPIRATING A TFRECORD FILE
# ここでは2枚の画像を TFRecordフォーマットで保存し、
# その後、読み出して表示する
if __name__ == '__main__':

  cat_in_snow  = tf.keras.utils.get_file('320px-Felis_catus-cat_on_snow.jpg', 'https://storage.googleapis.com/download.tensorflow.org/example_images/320px-Felis_catus-cat_on_snow.jpg')
  williamsburg_bridge = tf.keras.utils.get_file('194px-New_East_River_Bridge_from_Brooklyn_det.4a09796u.jpg','https://storage.googleapis.com/download.tensorflow.org/example_images/194px-New_East_River_Bridge_from_Brooklyn_det.4a09796u.jpg')

  image_labels = {
    cat_in_snow : 0,
    williamsburg_bridge : 1,
  }


  serialized_features_dataset = features_dataset.map(tf_serialize_example)
  filename = 'test.tfrecord'
  writer = tf.data.experimental.TFRecordWriter(filename)
  writer.write(serialized_features_dataset)

  filenames = [filename]
  raw_dataset = tf.data.TFRecordDataset(filenames)
  parsed_dataset = raw_dataset.map(_parse_function)
## WRITING A TFRECORD FILE
# Write the `tf.Example` observations to the file.
  with tf.python_io.TFRecordWriter(filename) as writer:
    for i in range(n_observations):
      example = serialize_example(feature0[i], feature1[i], feature2[i], feature3[i])
      writer.write(example)

## READING A TFRECORD FILE
#Suppose we now want to read this data back, to be input as data into a model.
#The following example imports the data as is, as a tf.Example message. This can be useful to verify that a the file contains the data that we expect. This can also be useful if the input data is stored as TFRecords but you would prefer to input NumPy data (or some other input data type), for example here, since this example allows us to read the values themselves.
#We iterate through the TFRecords in the infile, extract the tf.Example message, and can read/store the values within.

# sa L119  filename = 'test.tfrecord'
  record_iterator = tf.python_io.tf_record_iterator(path=filename)

  for string_record in record_iterator:
    example = tf.train.Example()
    example.ParseFromString(string_record)

    print(example)

    # Exit after 1 iteration as this is purely demonstrative.
    break

# Write the raw image files to images.tfrecords.
# First, process the two images into tf.Example messages.
# Then, write to a .tfrecords file.

  with tf.python_io.TFRecordWriter('images.tfrecords') as writer:
    for filename, label in image_labels.items():
      image_string = open(filename, 'rb').read()
      tf_example = image_example(image_string, label)
      writer.write(tf_example.SerializeToString())

  print("PASSED:STAGE-1")

  raw_image_dataset = tf.data.TFRecordDataset('images.tfrecords')

# Create a dictionary describing the features.
  image_feature_description = {
    'height': tf.FixedLenFeature([], tf.int64),
    'width': tf.FixedLenFeature([], tf.int64),
    'depth': tf.FixedLenFeature([], tf.int64),
    'label': tf.FixedLenFeature([], tf.int64),
    'image_raw': tf.FixedLenFeature([], tf.string),
  }

  print("PASSED:STAGE-2")
  parsed_image_dataset = raw_image_dataset.map(_parse_image_function)
  print("PASSED:STAGE-3:",parsed_image_dataset)

  for image_features in parsed_image_dataset:
    print("PASSED:LOOP-1 W,H):({},{})".format(image_features['width'],image_features['height']))
    image_raw = image_features['image_raw'].numpy()
#    img=Image(data=image_raw)
    img=mpimg.imread(data=image_raw)
    imgplot=plt.imshow(img)
    plt.show()
#    print("shape of image",img.shape)
#    img = cv.resize(img,(image_features['width'],image_features['height']))
#    cv.imshow("",img)
#    cv.waitKey()
#    display(img)
#    img = display.Image(data=image_raw)
#    print("image",img.shape)
#    print("Image shape:",reshape(image_raw,(300,300)))
#    print("Type of the Image:".format(image_f))
#    display.display(display.Image(data=image_raw))

# THIS IS THE END OF THE PROGRAM