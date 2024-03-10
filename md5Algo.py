
#to represent the msg in binary format
def binaryRepresentation(inputMsg) :
    binary_message = ''.join(format(ord(char), '08b') for char in inputMsg)

    return binary_message


def multipleOf512(lenMsg):
    res = lenMsg % 512
    finalRes = 512 - res if res != 0 else 0

    return finalRes

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
    zeroesToBeAdded = multipleOf512(len(addedOneBit))

    if zeroesToBeAdded < 64:
        paddedResult = addedOneBit[:-64]  # Remove last 64 bits
    else:
        paddedResult = addedOneBit

    paddedResultFinal = zeroesAddedInput(paddedResult, zeroesToBeAdded)
    lengthIn64Bits = addLengthBits(len(inputMsg))
    paddedResultFinal += lengthIn64Bits

    return paddedResultFinal



inputmsg = "a"
msgBits = binaryRepresentation(inputmsg)


print(padding(msgBits, inputmsg))
print(len(padding(msgBits,inputmsg)))


# def mainCompressionFunction(F,G,H,I):
#     #PROBABLY HERE THE FUNCTIONS WILL COME 