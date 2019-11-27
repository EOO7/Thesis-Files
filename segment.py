# adapted from https://stackoverflow.com/questions/20818121/save-csv-to-mat-or-binary

import csv  
import sys
import numpy
import scipy.io
import re
import os
import glob

from collections import Counter

neural_net_output = []
record_modes = []

files = [i for i in glob.glob('*.{}'.format('csv'))]
#print(files)
for file in files:
    if re.match(r"output_", file):
        for line in open(file):
            line = re.sub(r"\n", '', line)
            neural_net_output.append(int(float(line)))

        file_name = re.sub(r"\.csv", '', file)
        variable_name = re.sub(r"output_", 'ECG_', file_name)
        output_file_name = file_name + ".mat"

        data_file = re.sub(r"output_", '', file)

        data = []
        with open(data_file) as f:
            print(data_file, ": finding appropriate mode")
            reader_f = csv.reader(f)
            i = 0
            segment_lengths = []
            for row in reader_f:
                i += 1
                predicted_p_wave = neural_net_output[0]
                neural_net_output.pop(0)
                if predicted_p_wave == 1:
                    segment_lengths.append(i)
                    i = 0

        modes= [length for length, length_count in Counter(segment_lengths).most_common(10)]
        for mode in modes:
            #print(modes)
            if (mode > 2) and (mode <= 8):
                record_modes.append(mode)
                #print(mode)
                break

        neural_net_output = []
#print(len(record_modes))






neural_net_output = []
too_short = 0
too_long = 0
total = 0
max_length = 0
window_length = 44

files = [i for i in glob.glob('*.{}'.format('csv'))]
for file in files:
    if re.match(r"output_", file):
        for line in open(file):
            line = re.sub(r"\n", '', line)
            neural_net_output.append(int(float(line)))

        file_name = re.sub(r"\.csv", '', file)
        variable_name = re.sub(r"output_", 'ECG_', file_name)
        output_file_name = file_name + ".mat"

        data_file = re.sub(r"output_", '', file)

        data = []

        curr_mode = record_modes[0]
        record_modes.pop(0)
        upper_limit = curr_mode * 2
        #print('Upper:', upper_limit)
        lower_limit = 2
        counter = 0
        maxx = 0

        with open(data_file) as f:
            print(data_file, ': creating .mat file')
            reader_f = csv.reader(f)
            rowData = []
            for row in reader_f:
                i = 0
                for elem in row:
                    if i < window_length:
                        rowData.append(float(elem))
                        i += 1
                #print(i)
                counter += 1
                predicted_p_wave = neural_net_output[0]
                neural_net_output.pop(0)
                if (counter >= upper_limit):
                    data.append(rowData)
                    rowData = []
                    too_long += 1
                    total += 1
                    if counter > max_length:
                        max_length = counter
                        #print(max_length)
                    counter = 0
                elif (predicted_p_wave == 1) and (counter >= lower_limit):
                    data.append(rowData)
                    rowData = []
                    total += 1
                    if counter > max_length:
                        max_length = counter
                        #print(max_length)
                    counter = 0
                if (predicted_p_wave == 1) and (counter < lower_limit):
                    too_short += 1
        #print(len(data))
        matrix = numpy.array(data)
        scipy.io.savemat(output_file_name, {variable_name:matrix})
        print("Too long: ", too_long, "/", total, ": ", too_long/total, "\n")
        neural_net_output = []

#print("Too long: ", too_long, "/", total, ": ", too_long/total, "\n")
#print("Too short: ", too_short, "/", total, ": ", too_short/total, "\n")
#print(max_length)