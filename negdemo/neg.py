"""
在柏拉图立方体上模拟演化博弈
博弈模型为捐赠模型（b=5 c=2）
博弈策略为最优者替代策略
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random


def get_key(dict1, value):
    return [k for k, v in dict1.items() if v == value]


# 画图
def draw_graph(G, labels, labels1):
    all_nodelist = nx.nodes(G)
    # 合作者节点列表
    C_nodelist = get_key(labels, r'$C$')
    # list(labels.keys())[list(labels.values()).index(r'$C$')]
    # 背叛者节点列表
    D_nodelist = list(set(all_nodelist).difference(set(C_nodelist)))  # all_nodelist中有 C_nodelist没有
    # 固定位置    # pos = nx.spring_layout(G)  # positions for all nodes
    pos = {0: (0.53771846, 1),
           1: (-0.51918722,  0.80425603),
           2: (-0.13878156, -0.24656631),
           3: (0.95455036, 0.00920435),
           4: (0.1334797, 0.23976615),
           5: (0.52534358, -0.80369003),
           6: (-0.53673445, -0.99480466),
           7: (-0.95638888, -0.00816553)}
    pos1 = {0: (0.75771846, 1.0),
            1: (-0.51918722,  1.00425603),
            2: (-0.01878156, -0.06456631),
            3: (1.04855036, 0.20920435),
            4: (0.0934797, 0.43976615),
            5: (0.76534358, -0.80369003),
            6: (-0.75673445, -0.99480466),
            7: (-1.03938888, 0.19816553)}
    # nodes
    plt.xlim(-1.2, 1.2)  # set axis limits
    plt.ylim(-1.2, 1.2)

    nx.draw_networkx_nodes(G, pos,
                           nodelist=C_nodelist,
                           node_color='r',
                           node_size=500,
                           alpha=1.0)
    nx.draw_networkx_nodes(G, pos,
                           nodelist=D_nodelist,
                           node_color='b',
                           node_size=500,
                           alpha=1.0)
    # edges
    nx.draw_networkx_edges(G, pos, width=2.0, alpha=0.6)
    # nx.draw_networkx_edges(G, pos,
    #                        edgelist=[(0, 1), (1, 2), (2, 3), (3, 0)],
    #                        width=8, alpha=0.3, edge_color='g')
    # nx.draw_networkx_edges(G, pos,
    #                        edgelist=[(4, 5), (5, 6), (6, 7), (7, 4)],
    #                        width=8, alpha=0.3, edge_color='g')
    # labels
    nx.draw_networkx_labels(G, pos=pos, labels=labels, font_color='w', font_size=16)
    nx.draw_networkx_labels(G, pos=pos1, labels=labels1, font_color='b', font_size=15)
    plt.axis('off')
    plt.savefig('./Figs/3-neg/' + str(iter_times[0]) + '.png')
    plt.show()
    iter_times[0] += 1


# 进行演化博弈——选择“捐赠博弈”模式（T=b,R=b-c,P=0,S=-c）
def games(G, label_g):
    pay_list = [5, 3, 0, -2]  # 收益矩阵，赋初值 b=5 c=2
    payoff_dict = {}  # 定义收益付出字典
    for n in G:
        payoff_dict[n] = 0  # 初始默认收益都为0
    for n in G:
        pay_sum = 0
        for nbr in G[n]:
            if label_g[n] == label_g[nbr]:
                if label_g[n] == strategy_set[0]:
                    pay_sum += pay_list[1]
                else:
                    pay_sum += pay_list[2]
            elif label_g[n] == strategy_set[1]:
                pay_sum += pay_list[0]
            else:
                pay_sum += pay_list[3]
        payoff_dict[n] = pay_sum
    return payoff_dict


# 每一轮博弈中，所有个体都和其邻居进行一次捐赠博弈，根据“最优者替代”规则进行博弈
def strategy_update(G, label, pay):
    for n in G:
        nbr_pay_list = {}
        for nbr in G[n]:
            nbr_pay_list[nbr] = pay[nbr]

        max_pay_nbr = max(nbr_pay_list, key=nbr_pay_list.get)
        if pay[n] < pay[max_pay_nbr]:
            label[n] = label[max_pay_nbr]
            # 更新策略（如果比所有邻居收益高则维持原策略，否则采用收益最高的邻居的策略）

    return label   # 返回更新后的标签


# 随机挑选一个节点作为背叛者
def Defector_set(G, lables):
    node_num = nx.number_of_nodes(G)
    init_defector = random.randint(0, node_num-1)   # 闭区间
    labels[init_defector] = strategy_set[1]         # 修改节点的标签类型（改为背叛者）
    return lables    # 返回更新后的标签


if __name__ == '__main__':
    # 初值
    G = nx.cubical_graph()
    strategy_set = [r'$C$', r'$D$']  # 标签集
    # 构造两个labels字典，一个存角色信息，一个存序号和收益信息
    labels = {}
    labels1 = {}
    for i in range(nx.number_of_nodes(G)):
        labels[i] = strategy_set[0]  # 初始所有的节点都是合作者
        labels1[i] = "(" + str(i) + "," + str(0) + ")"

    iter_times = [1]
    draw_graph(G, labels, labels1)       # 画出初始图像
    labels = Defector_set(G, labels)     # 随机选择背叛者
    draw_graph(G, labels, labels1)       # 画出挑选出背叛者的图像
    for j in range(4):
        payoff = games(G, labels)        # 计算每个个体的收益
        labels1 = {k: "(" + str(k) + "," + str(v) + ")" for k, v in payoff.items()}
        draw_graph(G, labels, labels1)   # 显示每个个体的收益
        labels = strategy_update(G, labels, payoff)    # 更新大家的策略
        draw_graph(G, labels, labels1)   # 画出策略更新后的图像

    # 需要修改的地方：
    # 如果邻居中收益最高的有很多的，这个时候可以加入随机因素，随机选择
