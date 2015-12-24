import datetime
import hashlib
import string
import random

__all__=[
	"getCurrentTimeStamp",
	"generatePassword"
]

def getCurrentTimeStamp() :
    return datetime.datetime.utcnow()


#
#   Password Generation
#

def generatePassword() : 
    characters = string.ascii_uppercase + string.digits
    password = ''.join(random.SystemRandom().choice(characters) for _ in range(7))
    print password
    print encrypt(password)
    return encrypt(password)

def encrypt(value):
    m = hashlib.md5()
    m.update(value)
    return m.hexdigest()