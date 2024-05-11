#imports


#CONSTANTS
# Define the K constants for the four rounds
K = [
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
    0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
    0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,

    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
    0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
    0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,

    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
    0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
    0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,

    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
    0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
    0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
]

# Define the s[i] values for left rotation
s = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
    4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
    6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21 ]


# Initialize the four buffers A, B, C, D with their respective initial values
A = 0x67452301 
B = 0xefcdab89 
C = 0x98badcfe
D = 0x10325476 

#to represent the msg in binary format
def binaryRepresentation(inputMsg) :
    binary_message = ''.join(format(ord(char), '08b') for char in inputMsg)

    return binary_message

#converts hex into binary nums
def hex_to_binary_32(hex_num):
    # Convert hexadecimal to binary
    binary = format(int(hex_num, 16), '0b')
    # Pad with leading zeros to make it 32 bits long
    binary_padded = binary.zfill(32)
    return binary_padded

def multipleOf512(inputMsgBits):
    res = len(inputMsgBits) % 512
    finalRes = 512 - res if res != 0 else 0

    if finalRes < 64:
        inputMsgFinal = inputMsgBits[:-64]

    else:
        finalRes = finalRes - 64
        inputMsgFinal = inputMsgBits

    return (finalRes, inputMsgFinal)


def zeroesAddedInput(paddingInput, zeroesToBeAdded):
    
    stringfin = ''
    for i in range(zeroesToBeAdded):
        stringfin = stringfin + '0'
    

    paddingInput += stringfin

    return paddingInput

def addLengthBits(msgLen):
    outputBits = msgLen * 8
    binary_length = bin(outputBits)[2:].zfill(64)

    return binary_length 

#once the msg has been presented in binary format, we can proceed with the algorithm by padding the msg

def padding(inputBits, inputMsg) :
    addedOneBit = inputBits + '1'
    zeroesToBeAdded, msgBits = multipleOf512(addedOneBit)
    paddedResultFinal = zeroesAddedInput(msgBits, zeroesToBeAdded)
    lengthIn64Bits = addLengthBits(len(inputMsg))
    paddedResultFinal += lengthIn64Bits

    return paddedResultFinal

#now the task is to divide the msg into equal blocks of 512 bits
def split_into_blocks(paddedMessage):
    blockSize = 512
    numBlocks = len(paddedMessage) // blockSize

    #blocks = [paddedMessage[i * blockSize : (i + 1) * blockSize] for i in range(numBlocks)]
    blocks = []
    for i in range(numBlocks):
        blocks.append(paddedMessage[i * blockSize : (i + 1) * blockSize])

    return blocks






#message schedul process breaks 512 bits block further down into sixteen 32 bits subblocks
def messageSchedule(inputBlock):
    blockSize = 512
    subBlockSize = 32
    limit = int(blockSize / subBlockSize)
    subblocks = []
    for i in range(limit):
        subblocks.append(inputBlock[i * subBlockSize : (i + 1) * subBlockSize])
    
    return subblocks



def compressionFunction(blocks, A, B, C, D):
    # Define the four auxiliary functions for the rounds
    def firstRoundFunction(valueB, valueC, valueD):
        # Implement first round function
        if isinstance(valueB, str):
            valueB = int(valueB, 16)
        if isinstance(valueC, str):
            valueC = int(valueC, 16)
        if isinstance(valueD, str):
            valueD = int(valueD, 16)
        firstResult = valueB & valueC
        secondResult = (( ~valueB) & valueD)
        finalResult = firstResult | secondResult
        finalResult = hex(finalResult)
        final = hex_to_binary_32(finalResult)

        return final

    def secondRoundFunction(valueB, valueC, valueD):
        # Implement second round function
        if isinstance(valueB, str):
            valueB = int(valueB, 16)
        if isinstance(valueC, str):
            valueC = int(valueC, 16)
        if isinstance(valueD, str):
            valueD = int(valueD, 16)
        firstResult = valueB & valueC
        secondResult = (valueC & (~valueD))
        finalResult = firstResult | secondResult
        finalResult = hex(finalResult)
        final = hex_to_binary_32(finalResult)

        return final

    def thirdRoundFunction(valueB, valueC, valueD):
        # Implement third round function
        if isinstance(valueB, str):
            valueB = int(valueB, 16)
        if isinstance(valueC, str):
            valueC = int(valueC, 16)
        if isinstance(valueD, str):
            valueD = int(valueD, 16)
        firstResult = valueB ^ valueC
        finalResult = firstResult ^ valueD
        finalResult = hex(finalResult)
        final = hex_to_binary_32(finalResult)

        return final
    def fourthRoundFunction(valueB, valueC, valueD):
        # Implement fourth round function
        if isinstance(valueB, str):
            valueB = int(valueB, 16)
        if isinstance(valueC, str):
            valueC = int(valueC, 16)
        if isinstance(valueD, str):
            valueD = int(valueD, 16)
        firstResult = (valueB | (~ valueD))
        finalResult = valueC ^ firstResult
        finalResult = hex(finalResult)
        final = hex_to_binary_32(finalResult)

        return final
    
    def leftrotate(x, c):
        return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF


    # Loop through each block
    for block in blocks:
        # Break the block into 32-bit subblocks
        subblocks = messageSchedule(block)

        # Initialize the four working variables
        AA = A
        BB = B
        CC = C
        DD = D

        # Main round loop
        for i in range(64):
            if 0 <= i <= 15:
                # Perform operations for the first round
                F = firstRoundFunction(BB, CC, DD)
                g = i
            elif 16 <= i <= 31:
                # Perform operations for the second round
                F = secondRoundFunction(BB, CC, DD)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                # Perform operations for the third round
                F = thirdRoundFunction(BB, CC, DD)
                g = (3 * i + 5) % 16
            elif 48 <= i <= 63:
                # Perform operations for the fourth round
                F = fourthRoundFunction(BB, CC, DD)
                g = (7 * i) % 16

            # Temporarily save DD
            temp = DD
            # Update DD
            DD = CC
            CC = BB
            s_index = i % len(s)
            BB = BB + leftrotate((AA + int(F) + K[i] + int(subblocks[g])), s[s_index]) & 0xFFFFFFFF

            AA = temp

        # Update the values of A, B, C, and D with the results of this block
        A = A + AA
        B = B + BB
        C = C + CC
        D = D + DD
        # A = int(A)
        # B = int(B)
        # C = int(C)
        # D = int(D)

        # A = hex(A)
        # B = hex(B)
        # C = hex(C)
        # D = hex(D)
        # A = hex(A)[2:].zfill(8)
        # B = hex(B)[2:].zfill(8)
        # C = hex(C)[2:].zfill(8)
        # D = hex(D)[2:].zfill(8)


    # Return the hash value
    return A, B, C, D

inputmsg = "password"
msgBits = binaryRepresentation(inputmsg)
padded_msg = padding(msgBits, inputmsg)
blocks = split_into_blocks(padded_msg)
hash_result = compressionFunction(blocks, A, B, C, D)

print(hash_result)

#convert the decimal values back to hexadecimals
A = hex(A)[2:].zfill(8)
B = hex(B)[2:].zfill(8)
C = hex(C)[2:].zfill(8)
D = hex(D)[2:].zfill(8)

print(A,B,C,D)


#concatenate the resuly altogether to get the final hash value of the string
final_hash = A + B + C + D
print(final_hash)