import json
import matplotlib.pyplot as plt
import tqdm

QUESTION_JSON = 'val2014_json/v2_mscoco_val2014_annotations.json'
ENTROPY_JSON = '05_logit_entropy_analysis/val_banc1280_logit_epoch12.json'
OCR_JSON = '07_ocr_combination/ocr_results_combination.json'

threshold = [5.0, 4.9, 4.8, 4.7, 4.6, 4.5, 4.4, 4.3, 4.2, 4.1, 4.0, 3.9, 3.8, 3.7, 3.6, 3.5, 3.4, 3.3, 3.2, 3.1, 3.0]

score_list = [0.0, 0.3, 0.6, 0.9, 1.0]

def find_imgId(jsonfile, qid):
    # criteria : multiple_choice_answer
    for elem in jsonfile:
        if elem['question_id'] == qid:
            return elem['image_id'], elem['multiple_choice_answer'], elem['answers']

def find_ocrAnswer(jsonFile, imgId):
    imgId = str(imgId).zfill(6)
    for elem in jsonFile:
        if elem['img_id'] == imgId:
            return elem['texts']

def getScore_model(answerStr, answerList):
    num = 0
    for elem in answerList:
        if elem["answer"] == answerStr:
            num += 1
    if (num >= 4): return 4
    else:
        return num; # 0, 1, 2, 3

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

    for i in range(len(threshold)):
        print(threshold[i])
        result_list = list()

        # 내 모델이 낸 답과 비교하기
        for q in tqdm.tqdm(entropy_json):
            isEntropyExceed = (q['entropy'] >= threshold[i])
            if (isEntropyExceed is False):
                continue
            qid = q['question_id']
            # image_id = find_imgId(question_json, qid)

            # answer: multiple_choice_answer
            image_id, answer, answer10 = find_imgId(question_json, qid)

            mymodel_answer = q['answer']
            isCorrect = (mymodel_answer == answer)

            ocr_answer = find_ocrAnswer(ocr_json, image_id)
            isBlank = False
            isExist = False
            ratio = None

            score = score_list[getScore_model(mymodel_answer, answer10)]

            if not ocr_answer:
                isBlank = True

            elif answer in ocr_answer:
                isExist = True
                ratio = float(1/len(ocr_answer))

            # ratio: 1 / 해당 image id에서 뽑은 OCR 텍스트 전체 개수
            qdict = {'qid': qid, 'isblank': isBlank, 'isExist': isExist, 'answer': answer,
            'model_answer': mymodel_answer, 'isCorrect': isCorrect, 'ratio': ratio, 'score': score}
            result_list.append(qdict)
        
        with open('07_ocr_combination/results_json(only model, ocrX)/annotation_OCR_result(thr={thr}).json'.format(thr=threshold[i]), 'w') as fp:
            json.dump(result_list, fp, indent=4)