
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



inputmsg = "ajgjfjgjhgkfdkgjfjghjdjgkhjdhgkdhgjskghsjgkjsbhgfjshgfjg"
msgBits = binaryRepresentation(inputmsg)
# print(binaryRepresentation(inputmsg))
# x = inputmsg + '1'
# y, z = multipleOf512(x)
# print(y, z)

print(padding(msgBits, inputmsg))
print(len(padding(msgBits,inputmsg)))


# def mainCompressionFunction(F,G,H,I):
#     #PROBABLY HERE THE FUNCTIONS WILL COME 