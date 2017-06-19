#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
from pyknp import KNP


"""
構文解析結果を保存

in：評価極性語,評価極性語のある文章
out:構文解析結果の辞書

"""
def save_bnst(pn_word,text):        

    bnst_dic ={}    
    pn_id = 0
 
    child_list=[]
    parent_list=[]

    # 1. 構文結果を保存 (1.親id辞書,2.単語id辞書) 
    knp = KNP()
    result = knp.parse(text)

    for bnst in result.bnst_list():
        word = ""
        dic_value ={}

        # 1-1.単語の結合、評価極性語のidの調査
        for mrph in bnst.mrph_list():            

            if mrph.midasi == pn_word: 
                pn_id = bnst.bnst_id
                
            word += mrph.midasi 

        # 1-2.辞書追加
        dic_value["parent_id"] = bnst.parent_id
        dic_value["word"]= word

        bnst_dic[bnst.bnst_id] = dic_value

    return bnst_dic,pn_id


"""
係り受け関係のid順を取得する

"""                            
def get_bnst_order(bnst_dic):

    bnst_order_dic = {}

    for my_id in bnst_dic.keys():

        flag = True
        my_list=[my_id]
        serch_id = my_id

        while flag:
            parent_id = bnst_dic[serch_id]["parent_id"]

            if parent_id != -1:                
                my_list.append(bnst_dic[serch_id]["parent_id"])
            else:
                flag = False
                
            serch_id = parent_id
            
        bnst_order_dic[my_id]  = my_list
    

    return bnst_order_dic

"""
最後の係り元idを取得する
"""
def get_bnst_end(bnst_dic):
    
    end_list = []

    for my_id in bnst_dic.keys():
        for value in bnst_dic.values():
            if my_id == value["parent_id"]:
                flag = False
                break
            else:
                flag = True

        if flag:
            end_list.append(my_id)
            
    return end_list

"""
"""    
def get_bnst_left(bnst_dic,bnst_order_dic,pn_id):
    
    bnst_left = []
    end_list = get_bnst_end(bnst_dic)
    
    for i in end_list:
        serch_list = bnst_order_dic[i]
        
        if pn_id in serch_list:
            p = serch_list.index(pn_id)
            if p != 0:
                tmp_list = []
                for j in range(p):
                    left_id = serch_list[j]
                    tmp_list.append(bnst_dic[left_id]["word"])
                bnst_left.append(tmp_list)
        
    return bnst_left

if __name__ == '__main__' :

    bnst_dic = {}
    pn_id = 0
    bnst_order_dic = {}

    
    #text = "ミャハの不思議なカリスマ性が上田さん声で表現されていて素晴らしいです"
    #pn_word = "ミャハ"
    text="アニメ映画としては何がいいのかわからない作品でした"
    pn_word = "いい"
    
    bnst_dic,pn_id = save_bnst(pn_word,text)
    bnst_order_dic = get_bnst_order(bnst_dic)
    print("ターゲット単語: {0}".format(pn_word))
    print("入力文章: {0}".format(text))
    print("-----------------------")
    #print("ターゲット単語の係り先: {0}".format(bnst_dic_parent[pn_id]))
    print("ターゲット単語に係るもの(左)：{0}".format(get_bnst_left(bnst_dic,bnst_order_dic,pn_id)))

