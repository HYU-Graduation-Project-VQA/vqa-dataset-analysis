import json
import matplotlib.pyplot as plt
import tqdm

QUESTION_JSON = 'val2014_json/v2_mscoco_val2014_annotations.json'
ENTROPY_JSON = 'logit_entropy_analysis/val_banc1280_logit_epoch12.json'
OCR_JSON = 'ocr_combination/ocr_results_combination.json'

threshold = 3.0

def find_imgId(jsonfile, qid):
    # criteria : multiple_choice_answer
    for elem in jsonfile:
        if elem['question_id'] == qid:
            return elem['image_id'], elem['multiple_choice_answer']

def find_ocrAnswer(jsonFile, imgId):
    imgId = str(imgId).zfill(6)
    for elem in jsonFile:
        if elem['img_id'] == imgId:
            return elem['texts']

if __name__ == '__main__':
    # open JSON files
    question_json = object()
    entropy_json = object()
    ocr_json = object()

    with open(QUESTION_JSON) as f1:
        question_json = json.load(f1)
        question_json = question_json['annotations']
    with open(ENTROPY_JSON) as f2:
        entropy_json = json.load(f2)
    with open(OCR_JSON) as f3:
        ocr_json = json.load(f3)

    result_list = list()

    # 내 모델이 낸 답과 비교하기
    for q in tqdm.tqdm(entropy_json):
        isEntropyExceed = q['entropy'] >= threshold
        if (isEntropyExceed is False):
            continue
        qid = q['question_id']
        # image_id = find_imgId(question_json, qid)
        image_id, answer = find_imgId(question_json, qid)

        # answer = q['answer']
        ocr_answer = find_ocrAnswer(ocr_json, image_id)
        isBlank = False
        isExist = False
        ratio = None
        if not ocr_answer:
            isBlank = True

        elif answer in ocr_answer:
            isExist = True
            ratio = float(1/len(ocr_answer))

        # ratio: 1 / 해당 image id에서 뽑은 OCR 텍스트 전체 개수
        qdict = {'qid': qid, 'isblank': isBlank, 'isExist': isExist, 'answer': answer, 'ratio': ratio}
        result_list.append(qdict)
    
    with open('ocr_combination/annotation_OCR_result.json', 'w') as fp:
            json.dump(result_list, fp, indent=4)