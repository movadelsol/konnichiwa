import os
import glob
import cv2
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import glob

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

# Environmental local variables 'r' indicates following string suppose to be treated as a row string. 
PATH_TO_CKPT=r'D:\work\Latest_object_detection_demo\out-11APR19-V1\frozen_inference_graph.pb'
PATH_TO_LABELS=r'D:\work\Latest_object_detection_demo\data\annotations\label_map.pbtxt'
#PATH_TO_TEST_IMAGES_DIR=r'D:\work\Latest_object_detection_demo\test'
#PATH_TO_TEST_IMAGES_DIR=r'D:\work\Saki_detector_dataset-b\images\N8'
PATH_TO_TEST_IMAGES_DIR=r'D:\work\Latest_object_detection_demo\data\images\testimg'
num_classes = 1

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append(r"D:\work\models\research")
from object_detection.utils import ops as utils_ops

# This is needed to display the images.
# %matplotlib inline

from object_detection.utils import label_map_util

from object_detection.utils import visualization_utils as vis_util

def initialize():
  detection_graph = tf.Graph()
  with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
#
  label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
  categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=num_classes, use_display_name=True)
  category_index = label_map_util.create_category_index(categories)
  return detection_graph, category_index

def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)


def run_inference_for_single_image(image, graph):
    with graph.as_default():
        with tf.Session() as sess:
            # Get handles to input and output tensors
            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}
            for key in [
                'num_detections', 'detection_boxes', 'detection_scores',
                'detection_classes', 'detection_masks'
            ]:
                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)
            if 'detection_masks' in tensor_dict:
                # The following processing is only for single image
                detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)

                detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(detection_masks, detection_boxes, image.shape[0], image.shape[1])
                detection_masks_reframed = tf.cast(tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                # Follow the convention by adding back the batch dimension
                tensor_dict['detection_masks'] = tf.expand_dims(detection_masks_reframed, 0)
            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

            # Run inference
            output_dict = sess.run(tensor_dict,feed_dict={image_tensor: np.expand_dims(image, 0)})
            # all outputs are float32 numpy arrays, so convert types as appropriate
            output_dict['num_detections'] = int(output_dict['num_detections'][0])
            output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.uint8)
            output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
            output_dict['detection_scores'] = output_dict['detection_scores'][0]
            if 'detection_masks' in output_dict:
                output_dict['detection_masks'] = output_dict['detection_masks'][0]
#            print("######### Run INference for single image::#Detection:{}".format(output_dict['num_detections']))

    return output_dict

if __name__ == "__main__":
  TEST_IMAGE_PATHS = glob.glob(os.path.join(PATH_TO_TEST_IMAGES_DIR, "*.jpg"))
  assert len(TEST_IMAGE_PATHS) > 0, 'No image found in `{}`.'.format(PATH_TO_TEST_IMAGES_DIR)
  print(TEST_IMAGE_PATHS)

  detection_graph, category_index = initialize()

  for image_path in TEST_IMAGE_PATHS:
    print("Image processing:",image_path)
    image = Image.open(image_path)
    # the array based representation of the image will be used later in order to prepare the
    # result image with boxes and labels on it.
    image_np = load_image_into_numpy_array(image)
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    # Actual detection.
    output_dict = run_inference_for_single_image(image_np, detection_graph)
#    print("######### MAIN::#Detection:{}".format(output_dict['num_detections']))
#    print("######### MAIN::DetectionScores:{}".format(output_dict['detection_scores']))
    x=output_dict['detection_scores']
    x0=x[x > 0.5]
#    print("Number of Circle detected:{}".format(x0.size))
#    x1=np.sort(x)[::-1]
#    x2=x1[:40]
#    print("Sorted scores:{}".format(x2))
#    print("######### MAIN::DetectionBoxes:{}".format(output_dict['detection_boxes']))
#    print("######### MAIN::#Detection:{}".format(output_dict['num_detections']))
    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        output_dict['detection_boxes'],
        output_dict['detection_classes'],
        output_dict['detection_scores'],
        category_index,
        instance_masks=output_dict.get('detection_masks'),
        use_normalized_coordinates=True,
        max_boxes_to_draw=50,
        line_thickness=2)
#    print("image size",IMAGE_SIZE)
#    plt.figure(figsize=IMAGE_SIZE)
#    plt.imshow(image_np)
    outfn = "./out/test/"+os.path.split(image_path)[1]
    print("Final out{}, #Cicle:{}".format(outfn,x0.size))
    image_np = image_np[...,[2,1,0]] # RGB->BGR (open-cv)
    cv2.imwrite(outfn, image_np)
