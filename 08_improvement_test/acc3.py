import json
import tqdm

QUESTION_JSON = 'C:/Users/USER/Documents/vqa-dataset-analysis/val2014_json/v2_mscoco_val2014_annotations.json'
# RESULT_JSON = 'logit_entropy_analysis/val_banc1280_logit_epoch12.json'

RESULT_JSON = 'C:/Users/USER/Documents/vqa-dataset-analysis/logit_entropy_analysis/val_banc1280_weighted20_epoch12.json'


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
    result_json = object()

    with open(QUESTION_JSON) as f1:
        question_json = json.load(f1)
        question_json = question_json['annotations']
    with open(RESULT_JSON) as f2:
        result_json = json.load(f2)
    
    score_distribution = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0}

    for q in tqdm.tqdm(result_json):
        
        qid = q['question_id']; answer = q['answer']
        answer_candidate = getAnswers(question_json, qid)
        
        score = getScore(answer, answer_candidate)
        score_distribution[str(score)] += 1
    
    with open('C:/Users/USER/Documents/vqa-dataset-analysis/val_banc1280_weighted20_epoch12_result.json', 'w') as fp:
        json.dump(score_distribution, fp, indent=4)