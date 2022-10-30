import json
import tqdm
import time
QIDS_TYPE = '09_improvement_test_2/results/qids_question_type.json'
ANNOTATION_FILE = 'val2014_json/v2_mscoco_val2014_annotations.json'
EXPR1 = "07_ocr_combination/results_json(only model, ocrX)/annotation_OCR_result(thr={thr}).json"
EXPR2 = "07_ocr_combination/results_json(ocrO)/annotation_OCR_result(thr={thr}).json"
EXPR3 = "07_ocr_combination/results_json(ocrO, combination)/annotation_OCR_result(thr={thr}).json"
ENTROPY_FILE = "05_logit_entropy_analysis/val_banc1280_logit_epoch12.json"
QID_JSON = "09_improvement_test_2/results/qid_qtype.json"

threshold = [5.0, 4.9, 4.8, 4.7, 4.6, 4.5, 4.4, 4.3, 4.2, 4.1, 4.0, 3.9, 3.8, 3.7, 3.6, 3.5, 3.4, 3.3, 3.2, 3.1, 3.0]

score_list = [0.0, 0.3, 0.6, 0.9, 1.0]

QUESTION_TYPE = [
    'what number is',
    'what is the name',
    'what time',
    'why',
    'why is the',
    'what does the',
    'where is the',
    'how',
    'where are the',
    'what brand',
    'who is',
    'which',
    'what',
    'what is on the',
    'what is the',
    'what type of',
    'what is',
    'what are the',
    'what kind of',
    'what is in the',
    'how many'
]

def find_q(jsonFile, question_id):
    for elem in jsonFile:
        if (elem['qid'] == question_id):
            return elem

def find_entropy(jsonFile, question_id):
    for elem in jsonFile:
        if (elem['question_id']) == question_id:
            return elem['entropy']

def new_dict():
    return dict({
            'what number is': 0.0,
            'what is the name': 0.0,
            'what time': 0.0,
            'why': 0.0,
            'why is the': 0.0,
            'what does the': 0.0,
            'where is the': 0.0,
            'how': 0.0,
            'where are the': 0.0,
            'what brand': 0.0,
            'who is': 0.0,
            'which': 0.0,
            'what': 0.0,
            'what is on the': 0.0,
            'what is the': 0.0,
            'what type of': 0.0,
            'what is': 0.0,
            'what are the': 0.0,
            'what kind of': 0.0,
            'what is in the': 0.0,
            'how many': 0.0
        })

if __name__ == '__main__':

    # open JSON files
    qids_type_json = object()
    annotation_json = object()
    expr1_json = object()
    expr2_json = object()
    expr3_json = object()
    entropy_json = object()
    qid_json = object()
    
    with open(QIDS_TYPE, 'r') as f1:
        qids_type_json = json.load(f1)
    with open(ANNOTATION_FILE, 'r') as f2:
        annotation_json = json.load(f2)
    with open(ENTROPY_FILE, 'r') as fs:
        entropy_json = json.load(fs)
    with open(QID_JSON, 'r') as ff:
        qid_json = json.load(ff)
        
    for i in range(len(threshold)):
        with open(EXPR1.format(thr=threshold[i]), 'r') as f3:
            expr1_json = json.load(f3)
        with open(EXPR2.format(thr=threshold[i]), 'r') as f4:
            expr2_json = json.load(f4)
        with open(EXPR3.format(thr=threshold[i]), 'r') as f5:
            expr3_json = json.load(f5)
        
        experiments = [expr1_json, expr2_json, expr3_json]
        
        
        step = 1
        for ExPr in experiments:
            qid_basket = new_dict()
            num_basket = new_dict()
            result_basket = new_dict()
            for q in tqdm.tqdm(ExPr):
                score = 0.0
                length = 0.0
                if str(q['qid']) in qid_json:
                    qid_basket[qid_json[str(q['qid'])]] += q['score']
                    num_basket[qid_json[str(q['qid'])]] += 1.0

            for k in result_basket:
                if num_basket[k] != 0.0:
                    result_basket[k] = qid_basket[k] / num_basket[k]
                else:
                    result_basket[k] = qid_basket[k]
                # print(k, result_basket[k])
            
            print('09_improvement_test_2/results/expr{expr}_{thr}_result.json'.format(expr=step, thr=threshold[i]))
            with open('09_improvement_test_2/results/expr{expr}_{thr}_result.json'.format(expr=step, thr=threshold[i]), 'w') as fp:
                json.dump(result_basket, fp, indent=4)
            
            step += 1
                    