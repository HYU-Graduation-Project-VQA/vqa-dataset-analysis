import json
import tqdm
import matplotlib.pyplot as plt
import numpy as np

threshold = [3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0]

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

experiment = ['1', '2', '3']

colors = ['blue', 'dodgerblue', 'deepskyblue']
labels = ['Only Model', 'OCR', 'OCR + Combination']

for qtype in tqdm.tqdm(QUESTION_TYPE):
    results = list()
    for i in range(len(experiment)):
        results.append(list())
    for thr in threshold:
        exprs = []
        path = '09_improvement_test_2/results/expr{expr}_{thr}_result.json'
        for expe in experiment:
            with open(path.format(expr=expe, thr=thr), 'r') as fp:
                json_file = json.load(fp)
                exprs.append(json_file)
        for expe in range(len(experiment)):
            results[expe].append(exprs[expe][qtype])
    # print(results)
    
    for elem, c, l in zip(results, colors, labels):
        plt.plot(threshold, elem, color=c, label=l, marker='*')
    plt.xlabel('threshold')
    plt.ylabel('total score')
    plt.xticks(threshold)
    plt.legend(loc='upper left')
    plt.title("Performance Analysis: \"{qtype}\"".format(qtype=qtype))
    plt.gcf().set_size_inches(13, 8.3)
    plt.fill_between(threshold, results[0], results[2], color = 'orange', alpha = 0.3)
    # mng = plt.get_current_fig_manager()
    # mng.full_screen_toggle()

    # plt.show()
    plt.savefig("09_improvement_test_2/result_imgs/{qtype}_score_result.png".format(qtype=qtype), dpi=500)
    
    plt.cla()
    plt.clf()