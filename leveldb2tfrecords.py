import caffe
import leveldb
import numpy as np
from caffe.proto import caffe_pb2

import tensorflow as tf

db = leveldb.LevelDB('/shared/TORCS_Training_1F')
#db = leveldb.LevelDB('/shared/TORCS_baseline_testset/TORCS_Caltech_1F_Testing_280')

datum = caffe_pb2.Datum()

filename = '/shared/TORCS_train.tfrecords'  # address to save the TFRecords file
# open the TFRecords file
writer = tf.python_io.TFRecordWriter(filename)

from tqdm import tqdm

for key, value in tqdm(db.RangeIter()):
    
    ################### parse data from LevelDB

    datum.ParseFromString(value)
    
    # explore data
    #print help(datum)
    #for k1, v1, in datum.ListFields():
    #   if type(v1) is not str:
    #       print k1.full_name, v1
    #   else:
    #       print k1.full_name, v1[:10]
    #print help(datum.ListFields()[0][0])
    
    #l = len(datum.float_data)
    #for j in range(l):
    #   print datum.float_data.pop()

    # 13 numbers are described in http://deepdriving.cs.princeton.edu/paper.pdf, "fast" mysteriously was not described, but fast = 1 seems to indicate that a road is making an abrupt turn now, and the desired speed should be decreased.

    fast = datum.float_data.pop()

    dist_RR = datum.float_data.pop()
    dist_MM = datum.float_data.pop()
    dist_LL = datum.float_data.pop()    
    
    toMarking_RR = datum.float_data.pop()
    toMarking_MR = datum.float_data.pop()
    toMarking_ML = datum.float_data.pop()
    toMarking_LL = datum.float_data.pop()

    dist_R = datum.float_data.pop()
    dist_L = datum.float_data.pop()

    toMarking_R = datum.float_data.pop()
    toMarking_M = datum.float_data.pop()
    toMarking_L = datum.float_data.pop()

    angle = datum.float_data.pop()
    
    img = caffe.io.datum_to_array(datum)
    #CxHxW to HxWxC
    img = np.transpose(img, (1,2,0))
    #BGR to RGB
    img = img[:,:,::-1]
        
    ################### write data to TFRecords 

    # Create a feature
    feature = {'fast': tf.train.Feature(float_list=tf.train.FloatList(value=[fast])),
        'dist_RR': tf.train.Feature(float_list=tf.train.FloatList(value=[dist_RR])),
        'dist_MM': tf.train.Feature(float_list=tf.train.FloatList(value=[dist_MM])),
        'dist_LL': tf.train.Feature(float_list=tf.train.FloatList(value=[dist_LL])),
        'toMarking_RR': tf.train.Feature(float_list=tf.train.FloatList(value=[toMarking_RR])),
        'toMarking_MR': tf.train.Feature(float_list=tf.train.FloatList(value=[toMarking_MR])),
        'toMarking_ML': tf.train.Feature(float_list=tf.train.FloatList(value=[toMarking_ML])),
        'toMarking_LL': tf.train.Feature(float_list=tf.train.FloatList(value=[toMarking_LL])),
        'dist_R': tf.train.Feature(float_list=tf.train.FloatList(value=[dist_R])),
        'dist_L': tf.train.Feature(float_list=tf.train.FloatList(value=[dist_L])),
        'toMarking_R': tf.train.Feature(float_list=tf.train.FloatList(value=[toMarking_R])),
        'toMarking_M': tf.train.Feature(float_list=tf.train.FloatList(value=[toMarking_M])),
        'toMarking_L': tf.train.Feature(float_list=tf.train.FloatList(value=[toMarking_L])),
        'angle': tf.train.Feature(float_list=tf.train.FloatList(value=[angle])),
        'image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img.tostring()]))}

    # Create an example protocol buffer
    example = tf.train.Example(features=tf.train.Features(feature=feature))

    # Serialize to string and write on the file
    writer.write(example.SerializeToString())
    
writer.close()
