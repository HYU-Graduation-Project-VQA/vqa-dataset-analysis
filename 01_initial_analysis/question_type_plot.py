import json
import matplotlib.pyplot as plt
import numpy as np

ACCURACY_JSON = 'accuracy_question_type_result.json'

if __name__ == '__main__':
    true_count = dict()
    false_count = dict()

    acc_list = dict()

    result_json = object()

    with open(ACCURACY_JSON) as f1:
        result_json = json.load(f1)
    
    ordered_dict = dict(sorted(result_json.items(), key=lambda item: item[1]))

    y_pos = np.arange(len(ordered_dict))

    plt.barh(y_pos, ordered_dict.values(), align='center')
    plt.tick_params(axis='both', which='major', labelsize=7)
    plt.tick_params(axis='both', which='minor', labelsize=6)
    plt.yticks(y_pos, labels=ordered_dict.keys())
    # plt.invert_yaxis()
    plt.xlabel('Accuracy(%)')
    plt.title("Accuracy of Each Question Type")

    y = list(ordered_dict.values())

    # for i in range(len(ordered_dict)):
    #     height = y[i]
    #     plt.text(y[i], height + 0.25, '%.01f' %height, ha='center', va='bottom', size = 12)

    plt.grid(True, axis='x')

    plt.show()
