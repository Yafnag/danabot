#!/usr/bin/env python3

import sys
from string import *

def main(functionName):
    lenStr      = len(functionName)
    counter     = 1
    fNameLen    = lenStr

    hashValue = 0

    while(fNameLen):
        reverseCounter     = lenStr - counter
        if lenStr == counter:
            reverseCounter = 1
        # Get char from the begining | bChar means chars from the begining
        bChar           = functionName[counter - 1]
        bUpperChar      = bChar.upper()
        bCharXOR        = ord(bChar) ^ lenStr
        bUpperCharXOR   = ord(bUpperChar) ^ lenStr
        
        # Get chars from the end | eChar means chars from the end
        eChar           = functionName[reverseCounter - 1]
        eCharUpper      = eChar.upper()
        eCharXOR        = ord(eChar) ^ lenStr
        eCharUpperXOR   = ord(eCharUpper) ^ lenStr

        hashValue       = eCharUpperXOR ^ (hashValue + (bUpperCharXOR * eCharXOR * bCharXOR))
        counter += 1
        fNameLen -= 1
    
    return hex(hashValue)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        functionName = sys.argv[1]
        hashVal = main(functionName)
        print(f"Function name : {functionName} -> Hash : {hashVal}")
    else:
        print("[!] This script should be used with one argument : the function name")
        exit(1)