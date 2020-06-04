import numpy as np
import pandas as pd
import pickle
import pydotplus

# python tree.py で実行可能

# 不要か
# csvデータをdfで取得
df_foods = pd.read_csv('data.csv', header=0)
# 説明変数
X = df_foods.loc[:,'Japanese food':'dessert']
# 目的変数
y = df_foods['Dish name']

# モデル呼び出し
with open('clf.pickle', mode='rb') as f:
    clf = pickle.load(f)

# ノード数
n_nodes = clf.tree_.node_count
tree_ = clf.tree_ # treeオブジェクト
threshold = clf.tree_.threshold # 各ノードの閾値
children_left = tree_.children_left # 各ノードからTrueへの分岐先ノード番号
children_right = tree_.children_right # 各ノードからFalseへの分岐先ノード番号（list）
feature = tree_.feature # 各変数の番号
classes = clf.classes_ # 分類
value = tree_.value # 各ノードに所属するクラス(料理), list, 0なら対応するインデックスの料理は含まない 1なら含む

is_leaves = np.zeros(shape=n_nodes, dtype=bool)
stack = [(0, -1)]  # seed is the root node id and its parent depth
while len(stack) > 0:
    node_id, parent_depth = stack.pop()
    # If we have a test node
    if (children_left[node_id] != children_right[node_id]):
        stack.append((children_left[node_id], parent_depth + 1))
        stack.append((children_right[node_id], parent_depth + 1))
    else:
        is_leaves[node_id] = True


def change_str_ans_to_int(str_ans):
    if str_ans == "Yes":
        ans = 1
        return ans
    elif str_ans == "No":
        ans = 0
        return ans
    else:
        print("YesかNoで答えてください")
        str_ans = str(input())
        return change_str_ans_to_int(str_ans)

# 質問の数
n_questions = 4

class QuestionsClass():

    def __init__(self):
        self.current_node = 0

    def cal_current_node(self):
        print(X.columns[feature[self.current_node]], 'が食べたいですか？ YesかNoで答えてください。')
        str_ans = str(input())
        ans = change_str_ans_to_int(str_ans)
        if ans <= threshold[self.current_node]:
            self.current_node = children_left[self.current_node]
        else:
            self.current_node = children_right[self.current_node]

    def set_ranking(self, ranking):
        self.ranking = ranking
        self.current_food = 0

    def detect_meal(self):
        # self.current_foodが食べたい料理を示すindexか？　違うなら+1する
        line = y[self.ranking[self.current_food]] + u"を作りたいですか？ YesかNoで答えてください。"
        print(line)
        str_ans = str(input())
        if str_ans == 'Yes':
            return True
        else:
            self.current_food += 1
            return False


question = QuestionsClass()

for _ in range(n_questions):
    if is_leaves[question.current_node]:
        break
    question.cal_current_node()
print(value[question.current_node])
ind = np.argsort(value[question.current_node].reshape(-1))[::-1] # indices that would be promising
question.set_ranking(ind)
for i in ind:
    if question.detect_meal():
        break
print(y[question.current_food])