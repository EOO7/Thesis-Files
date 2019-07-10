# adapted from:
	# https://www.freecodecamp.org/news/how-to-combine-multiple-csv-files-with-8-lines-of-code-265183e0854/

import os
import glob
import pandas as pd
import random
import csv

files = [i for i in glob.glob('*.{}'.format('csv'))]

files_to_be_combined_list = []

files_combo_1 = files.copy()
files_combo_2 = files.copy()
files_combo_3 = files.copy()
files_combo_4 = files.copy()
files_combo_5 = files.copy()
files_combo_6 = files.copy()

files_combo_1.pop(0)
files_combo_1.pop(0)
files_combo_2.pop(2)
files_combo_2.pop(2)
files_combo_3.pop(4)
files_combo_3.pop(4)
files_combo_4.pop(6)
files_combo_4.pop(6)
files_combo_5.pop(8)
files_combo_5.pop(8)
files_combo_6.pop(10)
files_combo_6.pop(10)


random.shuffle(files_combo_1)
files_to_be_combined_list.append(files_combo_1)
random.shuffle(files_combo_2)
files_to_be_combined_list.append(files_combo_2)
random.shuffle(files_combo_3)
files_to_be_combined_list.append(files_combo_3)
random.shuffle(files_combo_4)
files_to_be_combined_list.append(files_combo_4)
random.shuffle(files_combo_5)
files_to_be_combined_list.append(files_combo_5)
random.shuffle(files_combo_6)
files_to_be_combined_list.append(files_combo_6)

output_file_name_list = []
output_file_prefix = "combined_csv_"
for i in range(6):
	output_file_name_list.append(str(output_file_prefix + str(i+1) + '.csv'))
	file_list = files_to_be_combined_list.pop(0)

	output_file = open(output_file_name_list.pop(0), "w", newline='')
	#writer = csv.writer(output_file)

	for files in file_list:
		input_file = open(files, "r")
		lines = input_file.readlines()

		for line in lines:
			output_file.write(line)