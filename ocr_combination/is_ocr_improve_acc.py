import json
import matplotlib.pyplot as plt
import tqdm

QUESTION_JSON = 'val2014_json/v2_mscoco_val2014_annotations.json'
ENTROPY_JSON = 'logit_entropy_analysis/val_banc1280_logit_epoch12.json'
OCR_JSON = 'ocr_combination/ocr_results_combination.json'

if __name__ == '__main__':
    ocr_result = object()
