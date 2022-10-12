import base64
import numpy as np
import csv
import sys
import zlib
import time
import mmap

maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

csv.field_size_limit(maxInt)
   
FIELDNAMES = ['image_id', 'image_w','image_h','num_boxes', 'boxes', 'features']
infile = '../data/trainval/karpathy_val_resnet101_faster_rcnn_genome.tsv'



if __name__ == '__main__':

    # Verify we can read a tsv
    in_data = {}
    with open(infile, "rt") as tsv_in_file:
        reader = csv.DictReader(tsv_in_file, delimiter='\t', fieldnames = FIELDNAMES)
        for item in reader:
            item['image_id'] = int(item['image_id'])
            item['image_h'] = int(item['image_h'])
            item['image_w'] = int(item['image_w'])   
            item['num_boxes'] = int(item['num_boxes'])
            for field in ['boxes', 'features']:
                item[field] = np.frombuffer(base64.decodebytes(bytes(item[field], 'utf-8')), 
                      dtype=np.float32).reshape((item['num_boxes'],-1))
            in_data[item['image_id']] = item
            print(in_data)
            break
    print(in_data)
    