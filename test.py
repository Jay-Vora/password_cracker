#from hashlib import md5

#print(md5(b'password').hexdigest())
def binaryRepresentation(inputMsg) :
    binary_message = ''.join(format(ord(char), '08b') for char in inputMsg)

    return binary_message

# result = binaryRepresentation('abcd')
# print(result)
# print(len(result))

# paddingInput = result + '1'
# print(paddingInput)
# print(len(paddingInput))


def addLengthBits(msgLen):
    outputBits = msgLen * 8
    binary_length = bin(outputBits)[2:].zfill(64)

    return binary_length 

# print(addLengthBits(4))
# print(len(addLengthBits(4)))


def multipleOf512(lenMsg):
    res = lenMsg % 512
    finalRes = 512 - res

    #if finalRes < 0:
        #finalRes = 0 - (finalRes)
    return finalRes

def zeroesAddedInput(paddingInput, zeroesToBeAdded):
    
    stringfin = ''
    for i in range(zeroesToBeAdded):
        stringfin = stringfin + '0'
    

    paddingInput += stringfin

    return paddingInput


msg = 'abcdefghi'
binarymsg = binaryRepresentation(msg)
oneadded = binarymsg + '1'
x = multipleOf512(len(oneadded))
print(binarymsg, oneadded, x)
y = zeroesAddedInput(oneadded, x)
print(len(y))

#once i have the zeroes needed, i need to add that many zeroes to the input bits


# paddingInput_final = zeroesAddedInput(paddingInput, multipleOf512(len(paddingInput) ))
# print(paddingInput_final)
# print(len(paddingInput_final))

def padding(lengthBits, paddingInput_final):
    paddingInput_final += lengthBits

    return paddingInput_final

# print(padding(addLengthBits(4), paddingInput_final))