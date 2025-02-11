def simpleChecksum(data):
    checksum = 0;
 
    # Iterate through each character in the data
    for c in list(data):
        checksum += ord(c)
   
    return checksum % 256
