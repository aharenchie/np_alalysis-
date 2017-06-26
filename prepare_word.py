#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

def choose_keyword(text, keyword_data):

    keyword_list = []
    for keywords in keyword_data:
        for keyword in keywords:
            list= re.split("・|\s",keyword)            
            for t in list:
                if t in text:
                    keyword_list.append(t)
                    
    return keyword_list

