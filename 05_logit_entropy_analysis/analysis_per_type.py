import json
import matplotlib.pyplot as plt
import tqdm

QUESTION_JSON = 'val2014_json/v2_mscoco_val2014_annotations.json'
RESULT_JSON = 'logit_entropy_analysis/val_banc1280_logit_epoch12.json'

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

INDEX = 0

color = [(1.0, 0, 0), (0.75, 0, 0.25), (0.5, 0, 0.5), (0.25, 0, 0.75), (0, 0, 1.0)]

def find_dict(json_list, question_id):
    for elem in json_list:
        if elem['question_id'] == question_id:
            return elem

def O_or_X(str1, str2):
    str1_ = str(str1); str2_ = str(str2)
    if str1_ == str2_:
        return True
    return False

def getColor(bool):
    if bool:
        return 'b'
    return 'r'

def score(answerStr, answerList):
    num = 0
    for elem in answerList:
        if elem['answer'] == answerStr:
            num += 1
    if (num >= 4): return 4
    else:
        return num; # 0, 1, 2, 3

if __name__ == '__main__':
    question_json = object()
    mymodel_json = object()
    with open(QUESTION_JSON) as f1:
        question_json = json.load(f1)
    with open(RESULT_JSON) as f2:
        mymodel_json = json.load(f2)
        
    question_json = question_json['annotations']

    for i in range(len(QUESTION_TYPE)):
        print(QUESTION_TYPE[i])
        q_basket = []

        for questions in tqdm.tqdm(question_json):
            # per-question analysis
            if questions['question_type'] == QUESTION_TYPE[i]:
                qdict = find_dict(mymodel_json, questions['question_id'])
                iscorrect = O_or_X(qdict['answer'], questions['multiple_choice_answer'])
                qdict['iscorrect'] = iscorrect
                qdict['score'] = score(qdict['answer'], questions['answers'])
                q_basket.append(qdict)
                # print(qdict)
                # exit(0)
        
        correct = 0
        djdj = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        for q in q_basket:
            if q['iscorrect']:
                correct += 1
            djdj[q['score']] += 1
            plt.plot(q['entropy'], q['logit'], marker='x', color=color[q['score']], markersize=2, lw=0.1, mew=0.15)

        plt.xlabel('entropy')
        plt.ylabel('logit')
        result = 'question type: {qtype} \n' \
            'accuracy: {acc}% \n' \
            'detail: {q}/{p}'.format(qtype=QUESTION_TYPE[i],q=correct,p=len(q_basket),
            acc=round((correct/len(q_basket)) * 100, 3))
        
        plt.text(0, 0, result, fontsize=8)

        plt.savefig('logit_entropy_analysis/results_image/{qtype}_result.png'.format(qtype=QUESTION_TYPE[i]), dpi=600)

        plt.cla()
        plt.clf()

        metadata = {'question_type': QUESTION_TYPE[i], 'correct': correct, 'all_num': len(q_basket),
        'accuracy': round((correct/len(q_basket)) * 100, 3)}

        save_dict = {'result': q_basket, 'statistics': djdj, 'metadata': metadata}

        with open('logit_entropy_analysis/results_json/{qtype}_result.json'.format(qtype=QUESTION_TYPE[i]), 'w') as fp:
            json.dump(save_dict, fp, indent=4)