#!/usr/bin/env python3

import sys
from string import *
import pefile

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
    
    return hashValue

if __name__ == "__main__":
    if len(sys.argv) == 3:
        libPath = sys.argv[1]
        searchedHash = sys.argv[2]
        # Parse export table
        pe = pefile.PE(libPath)
        pe.parse_data_directories()
        for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            if exp.name is not None:
                hashVal = main((exp.name).decode())
                if hashVal == int(searchedHash, 16):
                    print(f"Function name : {exp.name} -> Hash : {hex(hashVal)}")
    else:
        print("[!] This script must be used with two arguments : Library path (ntdll / kernel32 ...) and hash")
        exit(1)