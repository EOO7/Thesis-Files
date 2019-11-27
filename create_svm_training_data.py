import os
import glob
import pandas as pd
import random
import csv
import h5py
import numpy
import re
import scipy.io

file_numbers = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119, 121, 122, 123, 124, 200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219, 220, 221, 222, 223, 228, 230, 231, 232, 233, 234];
#file_numbers = [100]
#num_features = 2083;
num_features = 3;
output_mtrx = []

#feat_mtrx_file = h5py.File('Feature_Matrix.mat', 'r')
#feat_mtrx = numpy.transpose(list(feat_mtrx_file['feature_vector']))

with h5py.File('Everything_and_Segment_Lengths.mat', 'r') as file:

	# getting the arrhythmia notation for each file
	for curr_file in file_numbers:
		
		input_file = open((str(curr_file) + '.txt'), "r")
		output_file_name = str(curr_file) + ".mat"
		variable_name = "arr_flags_" + str(curr_file)

		# variable used to ignore the first line of the input file
		i = 0

		norm_rhy = [] 						# N
		left_bund_brnch_blk = [] 			# L
		right_bund_brnc_blk = [] 			# R
		atr_premature_contr = [] 			# A
		premature_ventri_contr = [] 		# V
		paced_beat = [] 					# /
		aberrated_atr_premature_beat = [] 	# a
		ventri_flutter_wave = [] 			# !
		fus_ventri_n_norm_beat = [] 		# F
		non_conduc_p_wave = [] 				# x
		nodal_esc_beat = [] 				# j
		fus_paced_n_norm_beat = [] 			# f
		ventri_esc_beat = [] 				# E
		nodal_premature_beat = [] 			# J
		atr_esc_beat = [] 					# e
		unclass_beat = [] 					# Q

		# for each line in the input .txt file
		for lines in input_file:
			# ignore the first line
			if (i != 0):
				fields = lines.split()
				sample_number = fields[1]
				arrhythmia_type = fields[2]

				# add the segment
				if re.match(r'N',arrhythmia_type):
					norm_rhy.append(sample_number);
							
				elif re.match(r'L',arrhythmia_type):
					left_bund_brnch_blk.append(sample_number);
							
				elif re.match(r'R',arrhythmia_type):
					right_bund_brnc_blk.append(sample_number);
							
				elif re.match(r'A',arrhythmia_type):
					atr_premature_contr.append(sample_number);
							
				elif re.match(r'V',arrhythmia_type):
					premature_ventri_contr.append(sample_number);
							
				elif re.match(r'/',arrhythmia_type):
					paced_beat.append(sample_number);
							
				elif re.match(r'a',arrhythmia_type):
					aberrated_atr_premature_beat.append(sample_number);
							
				elif re.match(r'!',arrhythmia_type):
					ventri_flutter_wave.append(sample_number);
							
				elif re.match(r'F',arrhythmia_type):
					fus_ventri_n_norm_beat.append(sample_number);
							
				elif re.match(r'x',arrhythmia_type):
					non_conduc_p_wave.append(sample_number);
							
				elif re.match(r'j',arrhythmia_type):
					nodal_esc_beat.append(sample_number);
							
				elif re.match(r'f',arrhythmia_type):
					fus_paced_n_norm_beat.append(sample_number);
							
				elif re.match(r'E',arrhythmia_type):
					ventri_esc_beat.append(sample_number);
							
				elif re.match(r'J',arrhythmia_type):
					nodal_premature_beat.append(sample_number);
							
				elif re.match(r'e',arrhythmia_type):
					atr_esc_beat.append(sample_number);
							
				elif re.match(r'Q',arrhythmia_type):
					unclass_beat.append(sample_number);	

			else:
				i += 1

		# get the number of segments in the current file and iterate through them
		segment_lengths = numpy.transpose(list(file['num_segments']))
		curr_num_segments = int(segment_lengths[0][curr_file-1])
		curr_duration = numpy.transpose(list(file['duration']))
		curr_duration = curr_duration[0:curr_num_segments-1][curr_file-1]
		curr_duration = curr_duration[0:curr_num_segments]
		rolling_sum = 0

		for segment_duration in curr_duration:
			flags = []
			
			if (len(norm_rhy) != 0):
				targetted_segment_number = norm_rhy[0]
				if (int(targetted_segment_number) <= int(rolling_sum)):
					flags.append(1)
					norm_rhy.pop(0)
				else:
					flags.append(0)
			else:
				flags.append(0)

			if (len(left_bund_brnch_blk) != 0):
				targetted_segment_number = left_bund_brnch_blk[0]
				if (int(targetted_segment_number) <= int(rolling_sum)):
					flags.append(1)
					left_bund_brnch_blk.pop(0)
				else:
					flags.append(0)
			else:
				flags.append(0)

			if (len(right_bund_brnc_blk) != 0):
				targetted_segment_number = right_bund_brnc_blk[0]
				if (int(targetted_segment_number) <= int(rolling_sum)):
					flags.append(1)
					right_bund_brnc_blk.pop(0)
				else:
					flags.append(0)
			else:
				flags.append(0)

			if (len(atr_premature_contr) != 0):
				targetted_segment_number = atr_premature_contr[0]
				if (int(targetted_segment_number) <= int(rolling_sum)):
					flags.append(1)
					atr_premature_contr.pop(0)
				else:
					flags.append(0)
			else:
				flags.append(0)

			if (len(premature_ventri_contr) != 0):
				targetted_segment_number = premature_ventri_contr[0]
				if (int(targetted_segment_number) <= int(rolling_sum)):
					flags.append(1)
					premature_ventri_contr.pop(0)
				else:
					flags.append(0)
			else:
				flags.append(0)

			if (len(paced_beat) != 0):
				targetted_segment_number = paced_beat[0]
				if (int(targetted_segment_number) <= int(rolling_sum)):
					flags.append(1)
					paced_beat.pop(0)
				else:
					flags.append(0)
			else:
				flags.append(0)

			if (len(aberrated_atr_premature_beat) != 0):
				targetted_segment_number = aberrated_atr_premature_beat[0]
				if (int(targetted_segment_number) <= int(rolling_sum)):
					flags.append(1)
					aberrated_atr_premature_beat.pop(0)
				else:
					flags.append(0)
			else:
				flags.append(0)

			if (len(ventri_flutter_wave) != 0):
				targetted_segment_number = ventri_flutter_wave[0]
				if (int(targetted_segment_number) <= int(rolling_sum)):
					flags.append(1)
					ventri_flutter_wave.pop(0)
				else:
					flags.append(0)
			else:
				flags.append(0)

			if (len(fus_ventri_n_norm_beat) != 0):
				targetted_segment_number = fus_ventri_n_norm_beat[0]
				if (int(targetted_segment_number) <= int(rolling_sum)):
					flags.append(1)
					fus_ventri_n_norm_beat.pop(0)
				else:
					flags.append(0)
			else:
				flags.append(0)

			if (len(non_conduc_p_wave) != 0):
				targetted_segment_number = non_conduc_p_wave[0]
				if (int(targetted_segment_number) <= int(rolling_sum)):
					flags.append(1)
					non_conduc_p_wave.pop(0)
				else:
					flags.append(0)
			else:
				flags.append(0)

			if (len(nodal_esc_beat) != 0):
				targetted_segment_number = nodal_esc_beat[0]
				if (int(targetted_segment_number) <= int(rolling_sum)):
					flags.append(1)
					nodal_esc_beat.pop(0)
				else:
					flags.append(0)
			else:
				flags.append(0)

			if (len(fus_paced_n_norm_beat) != 0):
				targetted_segment_number = fus_paced_n_norm_beat[0]
				if (int(targetted_segment_number) <= int(rolling_sum)):
					flags.append(1)
					fus_paced_n_norm_beat.pop(0)
				else:
					flags.append(0)
			else:
				flags.append(0)

			if (len(ventri_esc_beat) != 0):
				targetted_segment_number = ventri_esc_beat[0]
				if (int(targetted_segment_number) <= int(rolling_sum)):
					flags.append(1)
					ventri_esc_beat.pop(0)
				else:
					flags.append(0)
			else:
				flags.append(0)

			if (len(nodal_premature_beat) != 0):
				targetted_segment_number = nodal_premature_beat[0]
				if (int(targetted_segment_number) <= int(rolling_sum)):
					flags.append(1)
					nodal_premature_beat.pop(0)
				else:
					flags.append(0)
			else:
				flags.append(0)

			if (len(atr_esc_beat) != 0):
				targetted_segment_number = atr_esc_beat[0]
				if (int(targetted_segment_number) <= int(rolling_sum)):
					flags.append(1)
					atr_esc_beat.pop(0)
				else:
					flags.append(0)
			else:
				flags.append(0)

			if (len(unclass_beat) != 0):
				targetted_segment_number = unclass_beat[0]
				if (int(targetted_segment_number) <= int(rolling_sum)):
					flags.append(1)
					unclass_beat.pop(0)
				else:
					flags.append(0)
			else:
				flags.append(0)


			rolling_sum = rolling_sum + segment_duration
			output_mtrx.append(flags)
		matrix = numpy.array(output_mtrx)
		output_mtrx = []
		scipy.io.savemat(output_file_name, {variable_name:matrix})

##### create row to output to .csv file -> need to find script


#		for curr_file in file_numbers:

'''








files = [i for i in glob.glob('*.{}'.format('csv'))]

files_to_be_combined_list = []

files_combo_1 = []
files_combo_2 = []
files_combo_3 = []
files_combo_4 = []
files_combo_5 = []
files_combo_6 = []

files_combo_1.append(files[0])
files_combo_1.append(files[1])
files_combo_2.append(files[2])
files_combo_2.append(files[3])
files_combo_3.append(files[4])
files_combo_3.append(files[5])
files_combo_4.append(files[6])
files_combo_4.append(files[7])
files_combo_5.append(files[8])
files_combo_5.append(files[9])
files_combo_6.append(files[10])
files_combo_6.append(files[11])



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
output_file_prefix = "test_csv_"
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
'''