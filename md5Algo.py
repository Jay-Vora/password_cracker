#imports
from ctypes import c_uint32



#to represent the msg in binary format
def binaryRepresentation(inputMsg) :
    binary_message = ''.join(format(ord(char), '08b') for char in inputMsg)

    return binary_message


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



inputmsg = "nghgwegfwjgngsghdvsbvdghdhfghdhvjdjhvbnhfdbhdbndhjvbbdfhchdsbvhdhcvbsvbvghsgvshvhdbvbdnhvbndbvb"
msgBits = binaryRepresentation(inputmsg)
# print(binaryRepresentation(inputmsg))
# x = inputmsg + '1'
# y, z = multipleOf512(x)
# print(y, z)

#print(padding(msgBits, inputmsg))
# print(len(padding(msgBits,inputmsg)))


# def mainCompressionFunction(F,G,H,I):
#     #PROBABLY HERE THE FUNCTIONS WILL COME

#now the task is to divide the msg into equal blocks of 512 bits
def split_into_blocks(paddedMessage):
    blockSize = 512
    numBlocks = len(paddedMessage) // blockSize

    #blocks = [paddedMessage[i * blockSize : (i + 1) * blockSize] for i in range(numBlocks)]
    blocks = []
    for i in range(numBlocks):
        blocks.append(paddedMessage[i * blockSize : (i + 1) * blockSize])

    return blocks

x = split_into_blocks(padding(msgBits, inputmsg))
y = x[0]
#print(split_into_blocks(padding(msgBits, inputmsg)))

# var1 = 0x00000000
# var2 = 0x00000000
# var3 = 0x00000000
# var4 = 0x00000000

# var1 = c_uint32(0)
# var2 = c_uint32(0)
# var3 = c_uint32(0)
# var4 = c_uint32(0)


# Initialize the four buffers A, B, C, D with their respective initial values
A = 0x67452301 
B = 0xefcdab89 
C = 0x98badcfe
D = 0x10325476 

# aBitLength = A.bit_length
# print(aBitLength)

#message schedul process
def mesageSchedule(inputBlock):
    blockSize = 512
    subBlockSize = 32
    limit = int(blockSize / subBlockSize)
    subblocks = []
    for i in range(limit):
        subblocks.append(inputBlock[i * subBlockSize : (i + 1) * subBlockSize])
    
    return subblocks 
# y =int(512 / 32)
# print(y)
print(mesageSchedule(y))
