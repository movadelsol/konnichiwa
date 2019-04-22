import os
import re

# constant definitions
base='./'
pipeline_file='ssd_mobilenet_v1_coco.config'
test_record_fname = './data/annotations/test.record'
train_record_fname = './data/annotations/train.record'
label_map_pbtxt_fname = './data/annotations/label_map.pbtxt'
#fine_tune_checkpoint='D:\work\pre-trained-models\ssd_mobilenet_v2_coco_2018_03_29\model.ckpt'
fine_tune_checkpoint='D:\work\pre-trained-models\ssd_mobilenet_v1_coco_2018_01_28\model.ckpt'
batch_size = 24
num_steps=10000
##
def get_num_classes(pbtxt_fname):
    from object_detection.utils import label_map_util
    label_map = label_map_util.load_labelmap(pbtxt_fname)
    categories = label_map_util.convert_label_map_to_categories(
        label_map, max_num_classes=90, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    return len(category_index.keys())
## base
if __name__ == "__main__":
    pipeline_fname = os.path.join('D:/work/models/research/object_detection/samples/configs/', pipeline_file)
    assert os.path.isfile(pipeline_fname), '`{}` not exist'.format(pipeline_fname)
    print("START")
    num_classes = get_num_classes(label_map_pbtxt_fname)
    with open(pipeline_fname) as f:
        s = f.read()
    dest= os.path.join(base+pipeline_file)
    print("Dest",dest)
    with open(dest, 'w') as f:
    # fine_tune_checkpoint
        s = re.sub('fine_tune_checkpoint: ".*?"',
            'fine_tune_checkpoint: "{}"'.format(fine_tune_checkpoint), s)
    
    # tfrecord files train and test.
        s = re.sub('(input_path: ".*?)(train.record)(.*?")', 'input_path: "{}"'.format(train_record_fname), s)
        s = re.sub('(input_path: ".*?)(val.record)(.*?")', 'input_path: "{}"'.format(test_record_fname), s)

    # label_map_path
        s = re.sub('label_map_path: ".*?"', 'label_map_path: "{}"'.format(label_map_pbtxt_fname), s)

    # Set training batch_size.
        s = re.sub('batch_size: [0-9]+','batch_size: {}'.format(batch_size), s)

    # Set training steps, num_steps
        s = re.sub('num_steps: [0-9]+','num_steps: {}'.format(num_steps), s)
    
    # Set number of classes num_classes.
        s = re.sub('num_classes: [0-9]+','num_classes: {}'.format(num_classes), s)
        f.write(s)
        print("Function {} complete.".format(pipeline_fname))

