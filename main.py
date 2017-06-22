#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import csv
import re
import run_knp
import prepare_word

argvs = sys.argv
argc = len(argvs)

# 引数チェック
if (argc != 3):
    print ('prease type "python %s reviewfile keywordfile"'%argvs[0])
    sys.exit()

if __name__ == "__main__":

    # レビューファイルの読み込み
    f = open(argvs[1])
    Reader_review_data = csv.reader(f)
    
    # キャラクター・キャスト・映画スタッフの読み込み
    f = open(argvs[2])
    Reader_keyword_data = csv.reader(f)
    keyword_data = [row for row in Reader_keyword_data]
    
    for i,review_data in enumerate(Reader_review_data):

        print(i+1)
        
        review_text=review_data[3].split(",")  #レビューデータ(評価、本文等)から本文取り出し        

        for text in review_text:
            keyword_list = prepare_word.choose_keyword(text,keyword_data)

            if len(keyword_list) != 0:
                
                for keyword in keyword_list:
                    bnst_dic,keyword_id = run_knp.save_bnst(keyword,text)
                
                    # 文節ごとに、係り先順を取得
                    bnst_order_dic = run_knp.get_bnst_order(bnst_dic)

                    # ターゲット単語が受けるものを取得
                    bnst_left = run_knp.get_bnst_left(bnst_dic,bnst_order_dic,keyword_id)
            
                    # ターゲット単語が係るものを取得
                    bnst_right = run_knp.get_bnst_right(bnst_dic,bnst_order_dic,keyword_id)
    
                    # 出力
                    print("ターゲット単語: {0}".format(keyword))
                    print("入力文章: {0}".format(text))
                    print()
                    print("ターゲット単語が受けるもの(左)：{0}".format(bnst_left))
                    print("ターゲット単語が係るもの(右): {0}".format(bnst_right))
                    print("-----------------------")        
