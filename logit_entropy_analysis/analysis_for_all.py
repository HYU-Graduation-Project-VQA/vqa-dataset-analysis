import json
import matplotlib.pyplot as plt
import tqdm

QUESTION_JSON = 'val2014_json/v2_mscoco_val2014_annotations.json'
RESULT_JSON = 'logit_entropy_analysis/val_banc1280_logit_epoch12.json'

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
        return num; # 0, 1, 2

if __name__ == '__main__':
    question_json = object()
    mymodel_json = object()
    with open(QUESTION_JSON) as f1:
        question_json = json.load(f1)
    with open(RESULT_JSON) as f2:
        mymodel_json = json.load(f2)
        
    question_json = question_json['annotations']

    q_basket = []
    # eiei = 0
    for questions in tqdm.tqdm(question_json):
        # eiei += 1
        # if eiei > 500: break
        qdict = find_dict(mymodel_json, questions['question_id'])
        iscorrect = O_or_X(qdict['answer'], questions['multiple_choice_answer'])
        qdict['iscorrect'] = iscorrect
        qdict['score'] = score(qdict['answer'], questions['answers'])
        if qdict['score'] == 0:
            q_basket.append(qdict)
        # print(qdict)
        # exit(0)
    
    correct = 0
    djdj = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    # num1 = 0
    for q in q_basket:
        # num1 += 1
        # if (num1 > 500): break
        if q['iscorrect']:
            correct += 1
        djdj[q['score']] += 1
        plt.plot(q['entropy'], q['logit'], marker='x', color=color[q['score']], markersize=2, lw=0.1, mew=0.15)

    plt.xlabel('entropy')
    plt.ylabel('logit')
    result = 'accuracy: {acc}% \n' \
        'detail: {q}/{p}'.format(q=correct,p=len(q_basket),
        acc=round((correct/len(q_basket)) * 100, 3))
    
    plt.text(0, 0, result, fontsize=8)

    plt.savefig('logit_entropy_analysis/results_image/for_bad_result.png', dpi=500)

    plt.cla()
    plt.clf()

    metadata = {'question_type': 'all', 'correct': correct, 'all_num': len(q_basket),
    'accuracy': round((correct/len(q_basket)) * 100, 3)}

    save_dict = {'result': q_basket, 'statistics': djdj, 'metadata': metadata}

    with open('logit_entropy_analysis/results_json/for_bad_result.json', 'w') as fp:
        json.dump(save_dict, fp, indent=4)