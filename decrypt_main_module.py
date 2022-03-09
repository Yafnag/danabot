#!/usr/bin/env python3
import sys
import hashlib
from wincrypto import CryptCreateHash, CryptHashData, CryptDeriveKey, CryptEncrypt, CryptImportKey, CryptExportKey
from wincrypto.constants import CALG_MD5, CALG_AES_256, bType_SIMPLEBLOB

def main(embeddedHash, magicInt, mainModuleFileName):
    # Concat embedded hash and the "key"
    embeddedHashKey = (embeddedHash + magicInt).encode()
    # Get the uppercase hex digest
    m = hashlib.md5(embeddedHashKey)
    md5KeyData = m.hexdigest().upper()
    # MD5 Hash the uppercase hex digest result, then use CryptDeriveKey 
    md5_hasher = CryptCreateHash(CALG_MD5)
    CryptHashData(md5_hasher, md5KeyData.encode())
    AESkey = CryptDeriveKey(md5_hasher, CALG_AES_256)
    print(f"[+] The AES key : {AESkey.key}")

    try: 
        encryptedData = open(mainModuleFileName, 'rb').read()
        decryptedData = AESkey.decrypt(encryptedData)
        if decryptedData[0:2] == b"PK":
            open("decryptedMainModule.zip", 'wb').write(decryptedData)
            print("[+] Main module successfully decrypted ! The file decryptedMainModule.zip is compressed, it can be easily decompressed using 7zip")
    except: 
        print("Error while reading encrypted main module")
    

if __name__ == "__main__":
    if len(sys.argv) == 4:
        embeddedHash = sys.argv[1]
        magicInt = sys.argv[2]
        encryptedMainModule = sys.argv[3]
        # main("53A62D36E50FDF73AB591B6B2B27BCAB", "25")
        main(embeddedHash, magicInt, encryptedMainModule)
    else:
        print("[!] This script takes 3 arguments : the embedded hash, the int value to concat with the hash and the encrypted main module filename. E.g : python decrypt_main_moodule.py 53A62D36E50FDF73AB591B6B2B27BCAB 25 encryptedMainModule.bin")
        exit()
    