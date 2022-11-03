import matplotlib.pyplot as plt
import json

if __name__ == "__main__":
    qtype_list = object()
    with open("04_dictionary_words/ocr_words/qtype_result_ocr.json") as f:
        qtype_list = json.load(f)
    
    qtype_list = dict(sorted(qtype_list.items(), key=lambda item: item[1]))
    colors = ['lightskyblue'] * 18 + ['deepskyblue'] * 10 + ['dodgerblue'] * 6
    graph = plt.barh(list(qtype_list.keys()), qtype_list.values(), align='center', color=colors)
    plt.bar_label(graph)
    
    plt.title("The advantage of OCR in terms of question types")
    plt.xlabel('# of questions')
    plt.ylabel('question types')
    plt.show()