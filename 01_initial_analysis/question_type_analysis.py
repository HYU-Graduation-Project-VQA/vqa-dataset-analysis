import json
from tqdm import tqdm

RESULT_JSON = 'accuracy_per_questions_result.json'
QUESTION_JSON = 'val2014_json/v2_mscoco_val2014_annotations.json'

if __name__ == '__main__':
    true_count = dict()
    false_count = dict()

    acc_list = dict()

    result_json = object()

    with open(RESULT_JSON) as f1:
        result_json = json.load(f1)
    with open(QUESTION_JSON) as f1:
        question_json = json.load(f1)
    
    question_keys = result_json.keys()

    for elem in tqdm(question_keys):
        candidate_id = result_json[elem]['qids'][0]

        question_type = str()
        for elem2 in question_json['annotations']:
            if candidate_id == elem2['question_id']:
                question_type = elem2['question_type']

        if question_type not in true_count:
            true_count[question_type] = 0
            false_count[question_type] = 0
        
        true_count[question_type] += int(result_json[elem]['correct'])
        false_count[question_type] += int(result_json[elem]['incorrect'])

    for elem in true_count.keys():
        acc_list[elem] = (true_count[elem] / (true_count[elem] + false_count[elem])) * 100
    
    with open("accuracy_question_type_result.json", "w") as fp:
        json.dump(acc_list, fp) 