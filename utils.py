def isNotValidId(id):
    return id < 0 or id > 80

def makeValid(id):
    if id < 0:
        id += 81

