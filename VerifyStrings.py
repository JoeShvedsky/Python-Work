# Checks if a single IP is valid. Must be four separate 8-bit values.


def singleStringCheck(address):
    if len(address) < 7:
        return False
    strlist = address.split('.')
    if len(strlist) != 4:
        return False
    else:
        for substr in strlist:
            if not substr.isdigit():
                return False
            if int(substr) > 255:
                return False

    return True

# Just for netmask.
def netMaskCheck(value):
    acceptable_values = [0, 128, 192, 224, 240, 248, 252, 254, 255]
    strlist = value.split('.')
    if len(strlist) == 4:
        foundSmallerValue = False
        for substr in strlist:
            if not (substr.isdigit() and int(substr) in acceptable_values):
                return False
            if int(substr) < 255:
                if int(substr) > 0 and foundSmallerValue == True:
                    return False
                foundSmallerValue = True
        return True
    if len(strlist) == 1 and value.isdigit() and  int(value) < 33 and int(value) > 7:
        return True
    return False

# Same as single string, just for multiple.
def multipleStringCheck(addresses):
    strlist = addresses.split()
    if len(strlist) == 0:
        return False
    for substr in strlist:
        if not singleStringCheck(substr):
            return False
    return True
