import os


def getToken():
    with open('TOKEN.txt','rt') as tokenFile:
        return tokenFile.read()
