import json
import re
from statistics import mode
from tqdm import tqdm

QUESTION_JSON = 'val2014/v2_OpenEnded_mscoco_val2014_questions.json'
ANSWER_JSON = 'val2014/v2_mscoco_val2014_annotations.json'
MYMODEL_JSON = 'val2014/val_banc1280_valtest_epoch12.json'

def get_question_sentence(qid):
    global question_json
    for elem in question_json['questions']:
        if elem['question_id'] == qid:
            return elem['question']

def get_real_answer(qid):
    global answer_json

    for elem in answer_json['annotations']:
        # criteria: question_id
        if elem['question_id'] == qid:
            return elem['multiple_choice_answer']

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
    
    qid = int(input("Enter QID: "))

    # question 문장 찾기
    question_sentence = get_question_sentence(qid)
    # for elem in question_json['questions']:
    #     if elem['question_id'] == qid:
    #         question_sentence = elem['question']
    
    # 실제 answer 찾기
    real_answer = get_real_answer(qid)
    # for elem in answer_json['annotations']:
    #     if elem['question_id'] == qid:
    #         real_answer = elem['multiple_choice_answer']
    
    # 내 모델의 answer 찾기
    mymodel_answer = get_mymodel_answer(qid)
    # for elem in mymodel_json:
    #     if elem['question_id'] == qid:
    #         mymodel_answer = elem['answer']
    
    print("Question: {q} \n\
    Real Answer: {ra} \n\
    My Model Answer: {ma}\n".format(q = question_sentence, ra = real_answer, ma = mymodel_answer))