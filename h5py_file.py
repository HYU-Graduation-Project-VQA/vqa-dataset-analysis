import h5py
import numpy as np
import json

h5py_file = h5py.File('val.hdf5', 'r')

# keys
    # <KeysViewHDF5 ['image_bb', 'image_features', 'pos_boxes', 'spatial_features']>
        # image_bb
        # <HDF5 dataset "image_bb": shape (1281164, 4), type "<f4">

        # image_features
        # <HDF5 dataset "image_features": shape (1281164, 2048), type "<f4">

        # pos_boxes
        # <HDF5 dataset "pos_boxes": shape (40504, 2), type "<i4">

        # spatial_features
        # <HDF5 dataset "spatial_features": shape (1281164, 6), type "<f4">

# print(h5py_file['image_bb'])

qid = int(input("Question ID: "))

with open("results/val2014_qids.json", "rb") as fp:
    qid_list = json.load(fp)
try:
    start, end = h5py_file['pos_boxes'][qid_list.index(qid)]
except ValueError:
    print("QID {qid} is not in the list!".format(qid=qid))
    exit(0)

print(start, end)

features = h5py_file['image_features'][start: end, :]
spatials = h5py_file['spatial_features'][start: end, :]

print(features)
print()
print(spatials)