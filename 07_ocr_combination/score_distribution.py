import json
import tqdm

QUESTION_JSON = 'val2014_json/v2_mscoco_val2014_annotations.json'
ENTROPY_JSON = '08_improvement_test/val_banc1280_logit_epoch12_result.json'

threshold = [3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0]

def getScore(answerStr, answerList):
    num = 0
    for elem in answerList:
        if elem['answer'] == answerStr:
            num += 1
    if (num >= 4): return 4
    else:
        return num; # 0, 1, 2, 3

def getAnswers(jsonFile, questionId):
    for elem in jsonFile:
        if questionId == elem['question_id']:
            return elem['answers']

if __name__ == '__main__':
    # open JSON files
    question_json = object()
    entropy_json = object()

    with open(QUESTION_JSON) as f1:
        question_json = json.load(f1)
        question_json = question_json['annotations']
    with open(ENTROPY_JSON) as f2:
        entropy_json = json.load(f2)
    
    for i in range(len(threshold)):
        print("threshold = {thr}".format(thr = threshold[i]))
        score_distribution = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0}

        for q in tqdm.tqdm(entropy_json):
            if not (q['entropy'] >= threshold[i]):
                continue
            
            qid = q['question_id']; answer = q['answer']
            answer_candidate = getAnswers(question_json, qid)
            
            score = getScore(answer, answer_candidate)
            score_distribution[str(score)] += 1
        
        print(score_distribution)