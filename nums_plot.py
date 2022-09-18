import json
import matplotlib.pyplot as plt

with open('v2_OpenEnded_mscoco_train2014_questions.json') as f:
    jsonData = json.load(f)

    questions = jsonData["questions"]
    q_dict = {}
    for elem in questions:
        if( elem['question'] not in q_dict):
            q_dict[elem['question']] = {'nums': 1, 'images': []}
            q_dict[elem['question']]['images'] = [elem['image_id']]
        else:
            q_dict[elem['question']]['nums'] += 1
            q_dict[elem['question']]['images'].append(elem['image_id'])
    
    # for elem in q_dict:
    #     if q_dict[elem]["nums"] == 111:
    #         print(elem, q_dict[elem])


over_2_dict = dict(filter(lambda elem:elem[1]['nums']>=2, q_dict.items()))
nums_data = dict()
a = q_dict.values()

for elem in over_2_dict.values():
    if(elem['nums'] not in nums_data):
        nums_data[elem['nums']] = 1
    else:
        nums_data[elem['nums']] += 1

sorted_dict = sorted(nums_data.items())
x = []; y = []
for elem in sorted_dict:
    x.append(elem[0])
    y.append(elem[1])
plt.bar(x[1::], y[1::])
plt.show()