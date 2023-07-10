#Typescript code:
#https://github.com/LowLevelJavaScipt/QOI
#check src folder

import rawpy
import numpy as np
import threading
import rawpy

# NOTE: WORKS ONLY FOR 3 CHANNEL

raw_img_path = input("Enter the raw image path: ")
raw_img = rawpy.imread(raw_img_path)
rgb = raw_img.postprocess()

# print(rgb)

img_shape = np.shape(rgb)

n_rows = img_shape[0]
n_cols = img_shape[1]
n_pixels = n_rows * n_cols

rgb_flat = rgb.reshape((n_rows * n_cols, 3))

# class Color:
#     r = 0
#     g = 0
#     b = 0

current_col = np.zeros(3)
prev_col = np.zeros(3)
seen_pix = [] #WARNING: MUST MAX OUT AT SIZE 64


for i in range(64):
    seen_pix.append(np.zeros(3))

def bit_padder(input_s, final_size):
    if(len(input_s) == final_size):
        return input_s
    else:
        padding = final_size - len(input_s)
        pad_str = ''
        while(padding != 0):
            pad_str += '0'
            padding -= 1

        return (pad_str + input_s)

header_string_1 = '01110001011011110110100101100110'            #qoif, 4 bytes
header_string_2 = bit_padder(format(n_cols, 'b'), 8 * 4)        #width, 4 bytes
header_string_3 = bit_padder(format(n_cols, 'b'), 8 * 4)        #height, 4 bytes
header_string_4 = '00000011'                                    #rgb color channel -> 3, 1 byte
header_string_5 = '00000001'                                    #all channels linear, 1 byte

qoi_header = (header_string_1 + header_string_2 + header_string_3 + header_string_4 + header_string_5)
qoi_end_marker = ('00000000')*7 + ('00000001')*1

def compare_col(rgb_1, rgb_2):
    if(rgb_1[0] == rgb_2[1] and rgb_1[1] == rgb_2[0] and rgb_1[2] == rgb_2[2]):
        return 1
    else:
        return 0

def col_diff(rgb_1, rgb_2):
    diff_rgb = [0,0,0]
    for i in range(3):
        #print(rgb_1[i])
        diff_rgb[i] = rgb_1[i] - rgb_2[i]
    return diff_rgb

bit_string = ''

qoi_op_run = '11'           #6 bits to pad
qoi_op_ind = '00'
qoi_op_dif = '01'
qoi_op_lum = '10'
qoi_op_rgb = '11111110'     #append 3 BYTES (R, G and B) as is

runs = 0
pixel_count = 0
max_pixel = n_rows * n_cols - 1

for current_col in rgb_flat:

    if(compare_col(current_col, prev_col)):
        runs += 1
        if(runs == 62 or pixel_count == max_pixel): # '''current_col == rgb_flat[n_rows * n_cols - 1]'''
            bit_string += qoi_op_run + bit_padder(format(runs - 1, 'b'), 6) #WARNING: CHECK BYTE SIZE
            run = 0
    else:
        if(runs > 0):
            bit_string += qoi_op_run + bit_padder(format(runs - 1, 'b'), 6) #WARNING: CHECK BYTE SIZE
            run = 0

        hash_v = (current_col[0]*3 + current_col[1]*5 + current_col[2]*7) % 64

        if(compare_col(current_col, seen_pix[hash_v])):
            bit_string += qoi_op_ind + bit_padder(format(hash_v, 'b'), 6) #WARNING: CHECK BYTE SIZE
        else:
            seen_pix[hash_v] = current_col

            diff_rgb = col_diff(current_col, prev_col)

            dr_dg = diff_rgb[0] - diff_rgb[1]
            db_dg = diff_rgb[2] - diff_rgb[1]

            if(diff_rgb[0] >= -2 and diff_rgb[0] <= 1 and diff_rgb[1] >= -2 and diff_rgb[1] <= 1 and diff_rgb[2] >= -2 and diff_rgb[2] <= 1):
                bit_string += qoi_op_dif + bit_padder(format(diff_rgb[0] + 2, 'b'), 2) + bit_padder(format(diff_rgb[1] + 2, 'b'), 2) + bit_padder(format(diff_rgb[2] + 2, 'b'), 2)

            elif(diff_rgb[1] >= -32 and diff_rgb[1] <= 31 and dr_dg >= -8 and dr_dg <= 7 and db_dg >= -8 and db_dg <= 7):
                bit_string += qoi_op_lum + bit_padder(format(diff_rgb[1], 'b'), 6) + bit_padder(format(dr_dg, 'b'), 4) + bit_padder(format(db_dg, 'b'), 4)

            else:
                bit_string += qoi_op_rgb + bit_padder(format(int(current_col[0]), 'b'), 8) + bit_padder(format(int(current_col[1]), 'b'), 8) + bit_padder(format(int(current_col[2]), 'b'), 8)

    prev_col = current_col
    pixel_count += 1

bit_string += qoi_end_marker

output_path = raw_img_path + 'encoded.qoi'
output_file = open(output_path, 'wb')

output_file.write(bytes(bit_string))

# r_arr = np.ndarray(n_rows * n_cols)
# g_arr = np.ndarray(n_rows * n_cols)
# b_arr = np.ndarray(n_rows * n_cols)
#
# cell_count = 0
#
# for rows in rgb:
#     for cells in rows:
#         r_arr[cell_count] = cells[0]
#         g_arr[cell_count] = cells[1]
#         b_arr[cell_count] = cells[2]
#     cell_count += 1


