"""
@author : Luka Secilmis
@date : 2022 August 10
"""

import argparse
import numpy as np

def ternary2int(t):
    i = 0
    for c in map(int, t):
        i = 3 * i + c
    return i

def encode(data_PATH, dna_PATH, alphabet=["A", "T", "C", "G"]):
        """Function that encodes data into DNA using Goldman coder

        :param inp: Signal to be encoded
        :type inp: str
        :return: Encoded signal
        :rtype: str
        """
        with open(data_PATH, 'rb') as f:
            data = f.read() # read bytes of data
        y = [np.base_repr(i,base=3) for i in data] # convert each byte to base-3
        z = [((6 - len(s)) * '0') + s for s in y] # append '0' to make usre each byte is 6 digits
        inp = ''.join(z) # to be encoded
        
        # Encode it using rotating alphabet of Goldman encoding
        d = alphabet.copy()
        encoded = d[int(inp[0])]
        for i in range(1, len(inp)):
            d = alphabet.copy()
            d.remove(encoded[i-1])
            encoded += d[int(inp[i])]
            
        # Write DNA 
        with open(dna_PATH, 'w+') as f:
            f.write(encoded)
        return
    
def decode(dna_PATH, data_PATH, alphabet=["A", "T", "C", "G"]):
        """Function that decodes DNA data using Goldman coder

        :param code: Signal to be decoded
        :type code: str
        :return: Decoded signal
        :rtype: str
        """
        with open(dna_PATH, 'r') as f:
            code = f.read() # read DNA
        flag = -1
        decoded = ""
        if code[0] not in alphabet[:-1]:
            print('ERROR: input string not decodable (must be ternary string)')
        decoded += str(alphabet.index(code[0]))

        for i in range(1, len(code)):
            b = alphabet.copy()
            b.remove(code[i-1])
            try:
                flag = b.index(code[i])
            except:
                flag = -1
            if flag != -1:
                decoded += str(flag)
        
        # split back into bytes
        bytes_ = [decoded[i:i+6] for i in range(0, len(decoded), 6)] 
        bytes_ = [ternary2int(b) for b in bytes_]
        data = bytes(bytes_)
        
        # Write data
        with open(data_PATH, 'wb+') as f:
            f.write(data)
        return
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('COMMAND',
                        type=str,
                        help='Command: encode or decode')
    parser.add_argument('PATH1',
                        type=str,
                        help='PATH 1')
    parser.add_argument('PATH2',
                        type=str,
                        help='PATH 2')
    args = parser.parse_args()
    
    command = args.COMMAND
    path1 = args.PATH1
    path2 = args.PATH2
    
    if command == 'encode':
        encode(path1, path2)
    elif command == 'decode':
        decode(path1, path2)
    else: print('command must be \'encode\' or \'decode\'')
    
if __name__ == '__main__':
    main()
    