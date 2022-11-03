import json
import tqdm

'''
    이번 실험의 목적은 OCR을 통해 단어가 잡힌 질문 및 이미지에 한해서
    실제 정답에 해당하는 단어가 OCR에 포함된 경우의 수의 비율을 산정하는 것이다.
    
    OCR을 통해 얻은 단어의 전체 집합이 실제 단어 리스트에서 차지하는 비율은 약 1/3 가량이다.
    실제로 OCR을 통해 얻은 단어의 몇 퍼센트가 실제 정답이 되는가의 비율을 보는 것이 이번 목표이다.
    
    이를 위해서는 전체 분모가 "OCR을 실행시켰을 때 단어가 하나라도 잡히는(즉, texts가 비어있지 않은) 이미지"이어야 한다.
    기존에는 전체 분모가 모든 이미지 및 question이었던 것과 차이가 있다.
'''

# question 및 이미지 별 실제 정답
ANNOTATION_JSON = "val2014_json/v2_mscoco_val2014_annotations.json"
# OCR로 긁은 단어의 전체 집합
OCR_WORDS = "04_dictionary_words/ocr_words/ocr_words.json"
# COCO 데이터셋에서 사용하는 단어의 전체 집합
REAL_WORDS = "04_dictionary_words/ocr_words/trainval_ans2label.json"
# 이미지 id별 감지된 OCR 단어 리스트
OCR_RESULTS = "07_ocr_combination/ocr_results_combination.json"

# 내 모델의 결과
MYMODEL_RESULTS = "09_improvement_test_2/1_mymodel.json"

def getOCRTexts(jsonFile, imgId):
    for img in jsonFile:
        # print(img["img_id"], type(img["img_id"]))
        # print(str(imgId).zfill(6), type(str(imgId).zfill(6)))
        if img["img_id"] == str(imgId).zfill(6):
            return img["texts"]

if __name__ == "__main__":
    annotation_json = object()
    ocr_words = object()
    real_words = object()
    ocr_results = object()
    mymodel_results = object()
    
    with open(ANNOTATION_JSON, 'r') as f:
        annotation_json = json.load(f)
        annotation_json = annotation_json['annotations']
    with open(OCR_WORDS, 'r') as f:
        ocr_words = json.load(f)
    with open(REAL_WORDS, 'r') as f:
        real_words = json.load(f)
    with open(OCR_RESULTS, 'r') as f:
        ocr_results = json.load(f)
    with open(MYMODEL_RESULTS, 'r') as f:
        mymodel_results = json.load(f)
    
    total_num = len(annotation_json)    # 전체 question 개수
    ocr_total_num = 0                   # OCR 단어가 하나라도 있는 이미지에 대응된 question의 수
    ocr_correct_num = 0
    model_success_num = 0
    
    
    ocr_results_ = dict()
    # speed up by making image_id as key!
    for elem in ocr_results:
        ocr_results_[elem['img_id']] = elem['texts']
    ocr_results = ocr_results_
    
    mymodel_results_ = dict()
    # speed up by making image_id as key!
    for elem in mymodel_results:
        mymodel_results_[str(elem['question_id'])] = elem['answer']
    mymodel_results = mymodel_results_
    
    qtypes = dict()
    
    for q in tqdm.tqdm(annotation_json):
        imgid = q["image_id"]
        if str(imgid).zfill(6) in list(ocr_results.keys()):
            ocr_list = ocr_results[str(imgid).zfill(6)]    # getOCRTexts(ocr_results, imgid)
            if ocr_list:
                ocr_total_num += 1
                if q["multiple_choice_answer"] == mymodel_results[str(q["question_id"])]:
                    model_success_num += 1
                elif q["multiple_choice_answer"] in ocr_list:
                    ocr_correct_num += 1
                    if q["question_type"] in qtypes:
                        qtypes[q["question_type"]] += 1
                    else: qtypes[q["question_type"]] = 1
                    # print(q["question_type"], q["question_id"], q["multiple_choice_answer"])
                # if q["multiple_choice_answer"] in ocr_list:
                #     ocr_correct_num += 1
                
    
    print("total imgs: ", total_num)
    print("ocr_total_num", ocr_total_num)
    print("ocr_correct_num: ", ocr_correct_num)
    print("model_success_num: ", model_success_num)
    print("ratio: ", (ocr_correct_num / ocr_total_num) * 100)
    with open("qtype_result_ocr.json", "w") as fp:
        json.dump(qtypes, fp, indent=4)
    
    '''
        100%|██████████████████████████████████████████████████████████████████████████████████████| 214354/214354 [05:20<00:00, 667.92it/s]
        total imgs:  214354             # 전체 question 수
        ocr_total_num 79249             # 전체 question 중 OCR 단어가 1개 이상 있는 경우
        ocr_correct_num:  2465          # OCR의 단어들 중 multiple_choice_answer가 "그대로" 있는 경우
        ratio:  3.1104493432093783      # 비율
    '''