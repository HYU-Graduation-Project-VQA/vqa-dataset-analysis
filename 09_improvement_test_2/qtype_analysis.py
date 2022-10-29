import json
import tqdm

QIDS_TYPE = '09_improvement_test_2/results/qids_question_type.json'
ANNOTATION_FILE = 'val2014_json/v2_mscoco_val2014_annotations.json'
EXPR1 = "07_ocr_combination/results_json(only model, ocrX)/annotation_OCR_result(thr={thr}).json"
EXPR2 = "07_ocr_combination/results_json(ocrO)/annotation_OCR_result(thr={thr}).json"
EXPR3 = "07_ocr_combination/results_json(ocrO, combination)/annotation_OCR_result(thr={thr}).json"
ENTROPY_FILE = "05_logit_entropy_analysis/val_banc1280_logit_epoch12.json"

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

    with open(QIDS_TYPE, 'r') as f1:
        qids_type_json = json.load(f1)
    with open(ANNOTATION_FILE, 'r') as f2:
        annotation_json = json.load(f2)
    with open(ENTROPY_FILE, 'r') as fs:
        entropy_json = json.load(fs)
        
    for i in range(len(threshold)):
        with open(EXPR1.format(thr=threshold[i]), 'r') as f3:
            expr1_json = json.load(f3)
        with open(EXPR2.format(thr=threshold[i]), 'r') as f4:
            expr2_json = json.load(f4)
        with open(EXPR3.format(thr=threshold[i]), 'r') as f5:
            expr3_json = json.load(f5)
        
        experiments = [expr1_json, expr2_json, expr3_json]
        # print(threshold[i], " ", end=' -> ')
        
        step = 1
        for ExPr in experiments:
            # print(step, end = ' ')
            step += 1
            qid_basket = new_dict()
            for qtype in tqdm.tqdm(QUESTION_TYPE):
                score_ = 0.0
                qs = qids_type_json[qtype]  # qids for a specific question type
                num = 0
                for q in qs:
                    if (find_entropy(entropy_json, q) >= threshold[i]):
                        score_ += (find_q(ExPr, q))['score']
                        num += 1
                if num == 0:
                    qid_basket[qtype] = 0.0
                else:
                    qid_basket[qtype] = score_ / num
            
            with open('09_improvement_test_2/results/expr{expr}_{thr}_result.json'.format(expr=step, thr=threshold[i]), 'w') as fp:
                json.dump(qid_basket, fp, indent=4)
                    