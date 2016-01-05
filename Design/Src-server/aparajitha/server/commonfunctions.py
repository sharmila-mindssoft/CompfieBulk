import datetime
import hashlib
import string
import random

__all__=[
	"getCurrentTimeStamp",
	"generatePassword",
    "generateRandom"
]

def getCurrentTimeStamp() :
    return datetime.datetime.utcnow()


#
#   Password Generation
#

def generateRandom():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.SystemRandom().choice(characters) for _ in range(7))

def generatePassword() : 
    password = generateRandom()
    return encrypt(password)

def encrypt(value):
    m = hashlib.md5()
    m.update(value)
    return m.hexdigest()