#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import csv
import run_knp 


if __name__ == "__main__":

    argvs = sys.argv
    argc = len(argvs)

    bnst_dic = {}
    bnst_order_dic = {}

    # 評価対象語リストの用意
    pn_word_list = []
    pn_id = 0
    
    bnst_left = []
    bnst_right = []
    
    # 引数チェック
    if (argc != 2):
        print ('prease type "python %s reviewfile"'%argvs[0])
        sys.exit()

    # レビューの読み込み
    f = open(argvs[1])
    dataReader_review = csv.reader(f)

    for review in dataReader_review:        
        li=review[3].split(",")
        for i in li:
            print(i)
        """
        # レビューデータに、評価対象語があるか判断
        

        # レビューデータに、評価対象語があったら実行
        if flag:
            # 評価対象語ごとに実行。
            # 構文解析格納・係り先順取得と評価対処語のid検索を別枠でやるようにする！
            for pn_word in pn_word_list:
                # KNPによる構文解析
                #bnst_dic,pn_id = run_knp.save_bnst(pn_word,text)

                # 文節ごとに、係り先順を取得
                #bnst_order_dic = run_knp.get_bnst_order(bnst_dic)

        
                # ターゲット単語が受けるものを取得
                #bnst_left = run_knp.get_bnst_left(bnst_dic,bnst_order_dic,pn_id)
    
                # ターゲット単語が係るものを取得
                #bnst_right = run_knp.get_bnst_right(bnst_dic,bnst_order_dic,pn_id)
    
                # 出力
                print("ターゲット単語: {0}".format(pn_word))
                print("入力文章: {0}".format(text))
                print()
                print("ターゲット単語が受けるもの(左)：{0}".format(bnst_left))
                print("ターゲット単語が係るもの(右): {0}".format(bnst_right))
                print("-----------------------")
    
        """
