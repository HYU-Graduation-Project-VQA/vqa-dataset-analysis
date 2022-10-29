import json
import os
import tqdm

# print(os.listdir('coco_ocr_results'))
file_list = os.listdir('coco_ocr_results')
ocr_results = list()

for file in tqdm.tqdm(file_list):
    with open('coco_ocr_results/'+file) as f1:
        ocr_result = json.load(f1)

        for elem in ocr_result:
            ocr_results.append(elem)

ocr_results = sorted(ocr_results, key=lambda d: d['img_id'])

with open("ocr_results_merged.json", "w") as fp:
        json.dump(ocr_results,fp) 