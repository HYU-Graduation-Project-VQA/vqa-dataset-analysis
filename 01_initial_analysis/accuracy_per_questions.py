import json
import re
from statistics import mode
from tqdm import tqdm

QUESTION_JSON = 'val2014_json/v2_OpenEnded_mscoco_val2014_questions.json'
ANSWER_JSON = 'val2014_json/v2_mscoco_val2014_annotations.json'
MYMODEL_JSON = 'val2014_json/val_answer.json'

def get_real_answer(qid):
    global answer_json

    answer = object()

    for elem in answer_json['annotations']:
        # criteria: question_id
        if elem['question_id'] == qid:
            answer = elem
    
    return answer['multiple_choice_answer']

def get_mymodel_answer(qid):
    global mymodel_json

    for elem in mymodel_json:
        if elem['question_id'] == qid:
            return elem['answer']

if __name__ == '__main__':
    question_json = object()
    answer_json = object()
    mymodel_json = object()
    with open(QUESTION_JSON) as f1:
        question_json = json.load(f1)
    with open(ANSWER_JSON) as f2:
        answer_json = json.load(f2)
    with open(MYMODEL_JSON) as f3:
        mymodel_json = json.load(f3)
    
    statistics = dict()

    questions = question_json['questions']
    for elem in tqdm(questions):
        if elem['question'] not in statistics:
            statistics[elem['question']] = { 'qids': [], 'correct': 0, 'incorrect': 0}
        
        # append qid into qids
        statistics[elem['question']]['qids'].append(elem['question_id'])

        real_answer = get_real_answer(elem['question_id'])
        mymodel_answer = get_mymodel_answer(elem['question_id'])
        
        if real_answer == mymodel_answer:
            statistics[elem['question']]['correct'] += 1
        else:
            statistics[elem['question']]['incorrect'] += 1
    

    with open("accuracy_per_questions_result.json", "w") as fp:
        json.dump(statistics,fp) 