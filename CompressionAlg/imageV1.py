import heapq
import os
import numpy as np
import cv2

class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.imgArray = cv2.imread(path, cv2.IMREAD_UNCHANGED) #RETURNS AN NDARRAY IN BGR MODE
        # if(img.all() == None):
        #     print('Image not found')
        #     exit()
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

#======================================================================================#

    class HeapNode:
        def __init__(self, bgr, freq):
            self.bgr = bgr
            self.freq = freq
            self.left = None
            self.right = None

        # defining comparators less_than and equals
        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if(other == None):
                return False
            if(not isinstance(other, HeapNode)):
                return False
            return self.freq == other.freq

#======================================================================================#
    # functions for compression:

    def make_frequency_dict(self):
        frequency = {}
        nRows, nCols, depth = np.shape(self.npArray)
        for i in range(nRows):
            for j in range(nCols):
                if not self.npArray[i][j] in frequency:
                    frequency[character] = 0
                frequency[character] += 1

        return frequency

    def make_heap(self, frequency):
        for bgr in frequency:
            node = self.HeapNode(bgr, frequency[bgr])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while(len(self.heap)>1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)


    def make_codes_helper(self, root, current_code):
        if(root == None):
            return

        if(root.bgr != None):
            self.codes[root.bgr] = current_code
            self.reverse_mapping[current_code] = root.bgr
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")


    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)


    def get_encoded_array(self):
        # encoded_text = ""
        nRows, nCols, depth = np.shape(self.imgArray)
        encoded_array = np.ndarray((nRows, nCols))
        encoded_array.reshape(nRows, nCols)                                 #WARNING: CHANGE THE DIMENSIONS
        for i in range(nRows):
            for j in range(nCols):
                # encoded_array[i][j] =  int(self.codes[self.heap.bgr[i][j])  #NOTE: ERROR HERE
                bgr  = list(self.imgArray[i][j])
                encoded_array[i][j] = int(self.codes[bgr])
        return encoded_array


    # def pad_encoded_text(self, encoded_text):
    #     extra_padding = 8 - len(encoded_text) % 8
    #     for i in range(extra_padding):
    #         encoded_text += "0"

    #     padded_info = "{0:08b}".format(extra_padding)
    #     encoded_text = padded_info + encoded_text
    #     return encoded_text


    # def get_byte_array(self, encoded_):
        # if(len(padded_encoded_text) % 8 != 0):
        #     print("Encoded text not padded properly")
        #     exit(0)

        # b = bytearray()
        # for i in range(0, len(padded_encoded_text), 8):
        #     byte = padded_encoded_text[i:i+8]
        #     b.append(int(byte, 2))
        # return b


    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"

        # with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            # text = file.read()
            # text = text.rstrip()

        frequency = self.make_frequency_dict(self.imgArray)
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()

        encoded_array = self.get_encoded_array(self.imgArray)
        nRows, nCols = np.shape(encoded_array)

        f = open(imgName+"cmprs_png.bin", "wb")
        for i in range(nRows):
            f.write(encoded_array[i])
        f.close()
       # cv2.imwrite(imgName+"_cmprs.png", encoded_array)
            # padded_encoded_text = self.pad_encoded_text(encoded_text)

            # b = self.get_byte_array(padded_encoded_text)
            # output.write(bytes(b))

        print("Compressed")
        return output_path


    """ functions for decompression: """


#     def remove_padding(self, padded_encoded_text):
#         padded_info = padded_encoded_text[:8]
#         extra_padding = int(padded_info, 2)
#
#         padded_encoded_text = padded_encoded_text[8:]
#         encoded_text = padded_encoded_text[:-1*extra_padding]
#
#         return encoded_text
#
#     def decode_text(self, encoded_text):
#         current_code = ""
#         decoded_text = ""
#
#         for bit in encoded_text:
#             current_code += bit
#             if(current_code in self.reverse_mapping):
#                 character = self.reverse_mapping[current_code]
#                 decoded_text += character
#                 current_code = ""
#
#         return decoded_text
#
#
    # def decompress(self, input_path):
    #     filename, file_extension = os.path.splitext(self.path)
    #     output_path = filename + "_decompressed" + ".txt"
    #
    #     with open(input_path, 'rb') as file, open(output_path, 'w') as output:
    #         bit_string = ""
    #
    #         byte = file.read(1)
    #         while(len(byte) > 0):
    #             byte = ord(byte)
    #             bits = bin(byte)[2:].rjust(8, '0')
    #             bit_string += bits
    #             byte = file.read(1)
    #
    #         encoded_text = self.remove_padding(bit_string)
    #
    #         decompressed_text = self.decode_text(encoded_text)
    #
    #         output.write(decompressed_text)
    #
    #     print("Decompressed")
    #     return output_path
