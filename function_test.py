import os
import numpy as np
#Own python module
import reviser
#import app

def test_check_msg():
#Function test of in_range to check right behavoiour 
   msg_1 = np.array(['a','100','-300','50','32','5','0'])
   msg_2 = np.array(['63','400','-300','50','32','5','1'])
   msg_3 = np.array(['63','100','50,2','50','32','5','0'])
   msg_4 = np.array(['63','100','-300','-105','32','5','0'])
   msg_5 = np.array(['63','100','-300','50','asd','5','0'])
   msg_6 = np.array(['63','100','-300','50','32','*','0'])
   msg_7 = np.array(['63','100','-300','50','32','5','2'])
   msg_8 = np.array(['63','100','-300','50','32','5','0'])
   msg_9 = np.array(['63','100','-300','50','32','5','1'])
   
   i = 0
   
   #Incorrect behavoiour predicted
     
   
   if not reviser.check_msg(msg_1):
       pass 
   else :
       print("Test 1 in check_msg failed")
       i+=1
        
   if not reviser.check_msg(msg_2):
        pass
   else :
        print("Test 2 in check_msg failed")
        i+=1
   if not reviser.check_msg(msg_3):
        pass
   else :
        print("Test 3 in check_msg failed")
        i+=1
   if not reviser.check_msg(msg_4):
        pass
   else :
        print("Test 4 in check_msg failed")
        i+=1
   if not reviser.check_msg(msg_5):
        pass
   else :
        print("Test 5 in check_msg failed")
        i+=1
   if not reviser.check_msg(msg_6):
        pass
   else :
        print("Test 6 in check_msg failed")
        i+=1       
   if not reviser.check_msg(msg_7):
        pass
   else :
        print("Test 7 in check_msg failed")
        i+=1       
        
     #Correct behavoiour predicted
   if reviser.check_msg(msg_8):
        pass
   else :
        print("Test 8 in check_msg failed")
        i+=1
   if reviser.check_msg(msg_9):
        pass
   else :
        print("Test 9 in check_msg failed")
        i+=1
    
   if not i == 0:
        return False
    
   return True



def test_is_integer():
#Function test of in_range to check right behavoiour 
    val = ('!','a', '10.5','-10','10')
    i = 0
     #Incorrect behavoiour predicted
    if not reviser.is_integer(val[0]):
        pass
    else :
        print("Test 1 in test_inter failed")
        i+=1
    if not reviser.is_integer(val[1]):
        pass
    else :
        print("Test 2 in test_inter failed")
        i+=1
    if not reviser.is_integer(val[2]):
        pass
    else :
        print("Test 3 in test_inter failed")
        i+=1
    
     #Correct behavoiour predicted
    if reviser.is_integer(val[3]):
        pass
    else :
        print("Test 4 in test_inter failed")
        i+=1
    if reviser.is_integer(val[4]):
        pass
    else :
        print("Test 5 in test_inter failed")
        i+=1
    
    if not i == 0:
        return False
    
    return True


def test_in_range():
#Function test of in_range to check right behavoiour 
    val = (-10,20,5)
    min = 0
    max = 10
    i = 0
    
    #Incorrect behavoiour predicted
    if not reviser.in_range(val[0],min,max):
        pass
    else :       
        print("Test 5 in test_inter failed")
        i+=1
    if not reviser.in_range(val[1],min,max):
        pass
    else : 
        print("Test 5 in test_inter failed")
        i+=1
    
    #Correct behavoiour predicted
    if reviser.in_range(val[2],min,max):
        pass
    else :        
        print("Test 5 in test_inter failed")
        i+=1
    
    if not i == 0:
        return False
    
    return True
    
    
    
if __name__ == '__main__':
    if test_in_range():
        print("Test of in_range function success!")
    else : 
        print("Test of in_range function failed!")
        
    if test_is_integer():
        print("Test of is_integer function success!")
    else : 
        print("Test of is_integer function failed!")
        
    if test_check_msg():
        print("Test of check_msg function success!")
    else : 
        print("Test of check_msg function failed!")
