import json
import matplotlib.pyplot as plt
import tqdm
import numpy as np

PATH1 = "ocr_combination/results_json(only model, ocrX)/"
PATH2 = "ocr_combination/results_json(ocrO)/"
PATH3 = "ocr_combination/results_json(ocrO, combination)/"

file_name = "annotation_OCR_result(thr={thr}).json"

threshold = [3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0]

list1 = [0.19564875491480999, 0.1856260894828588, 0.1755869302137959, 0.16571556751906685, 0.15451347004423, 0.14460178996261472, 0.13620445474443157, 0.12942209217264083, 0.12361809045226131, 0.11872356785851595, 0.11162585484226781, 0.10814374353671148, 0.10384846662657847, 0.1010548523206751, 0.09841140529531568, 0.09398778769375293, 0.09105346744309158, 0.09186116098144824, 0.08733528550512445, 0.09700499168053243, 0.1296943231441048]
list2 = list()
list3 = list()

# for elem in threshold:
#     PATH = PATH1 + file_name.format(thr=elem)
#     json_file = object()
#     with open(PATH, 'r') as f1:
#         json_file = json.load(f1)
#     num = len(json_file)
#     score = 0.0
#     for q in json_file:
#         print(q)
#         score += q["score"]
#     score /= num
#     list1.append(score)

for elem in tqdm.tqdm(threshold):
    PATH = PATH2 + file_name.format(thr=elem)
    json_file = object()
    with open(PATH, 'r') as f1:
        json_file = json.load(f1)
    
    num = len(json_file)
    score = 0.0
    for q in json_file:
        score += q["score"]
    score /= num
    list2.append(score)

for elem in tqdm.tqdm(threshold):
    PATH = PATH3 + file_name.format(thr=elem)
    json_file = object()
    with open(PATH, 'r') as f1:
        json_file = json.load(f1)
    
    num = len(json_file)
    score = 0.0
    for q in json_file:
        score += q["score"]
    score /= num
    list3.append(score)

plt.plot(threshold, list1, color='blue', marker='*', label='Only Model')
plt.plot(threshold, list2, color='dodgerblue', marker='*', label='OCR')
plt.plot(threshold, list3, color='deepskyblue', marker='*', label='OCR + Combination')

plt.xlabel('threshold')
plt.xticks(threshold)
plt.ylabel('total score')
plt.title("The Effect of OCR in terms of Performance")
plt.legend()

plt.show()