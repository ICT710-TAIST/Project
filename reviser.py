# Check if the values of the message are in a possible range
def in_range(val, min, max):
    if min <= val <= max:
        return True
    else :   
        return False

# Check if the values can parse to integer        
def is_integer(val):
    try:
        num = int(val)
    except ValueError:
        return False
        
    return True

# Check messag of plausibility
def check_msg(X):
    for msg in X:
        if is_integer(msg):
            pass
        else:
            # Instead of print log the the message
            print("Message contains not parse able values!")
            return False
    
    if in_range(int(X[0]), -360, 360):
        pass
    else:
        # Instead of print log the the message
        print("Message contains not parse able values!")
        return False
        
    if in_range(int(X[1]), -360, 360):
        pass
    else:
        # Instead of print log the the message
        print("Message contains not parse able values!")
        return False
        
    if in_range(int(X[2]), -360, 360):
        pass
    else:
        # Instead of print log the the message
        print("Message contains not parse able values!")
        return False
        
    if in_range(int(X[3]), -100, 100):
        pass
    else:
        # Instead of print log the the message
        print("Message contains not parse able values!")
        return False
        
    if in_range(int(X[4]), -100, 100):
        pass
    else:
        # Instead of print log the the message
        print("Message contains not parse able values!")
        return False
        
    if in_range(int(X[5]), -100, 100):
        pass
    else:
        # Instead of print log the the message
        print("Message contains not parse able values!")
        return False
        
    if in_range(int(X[6]), 0, 1):
        pass
    else:
        # Instead of print log the the message
        print("Message contains not parse able values!")
        return False
    
    return True