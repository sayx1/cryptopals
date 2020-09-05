
def strip_pdcks_7(data:bytes,bsize:int)->bytes:
    if len(data) % bsize != 0:
        return(0)

    padding_len = int(data[-1])

    for i in range(bsize-padding_len,len(data)):
        
        if data[i] != data[-1]:
            print('paddingError')
            return(0)

    return(data[:bsize-padding_len])


    
padded_data_1 = b'ICE ICE BABY\x04\x04\x04\x04'
padded_data_2 = b'ICE ICE BABY\x01\x02\x03\x04'
    
striped_1 = strip_pdcks_7(padded_data_1,16)
striped_2 = strip_pdcks_7(padded_data_2,16)

print(striped_1)
print(striped_2)

