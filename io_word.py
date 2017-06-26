#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import datetime

def write_csv(output_dic,name):
    file_name = name + str(datetime.datetime.today()) + ".csv"
    with open(file_name, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for key,value in output_dic.items():
            writer.writerow([key,value])
