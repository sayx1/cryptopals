from set3_21 import *

def undo_right_shift(final_y:int,shift_val:int)->int:
    '''
    param1: final_y given
    param2: value of shift
    '''
    
    #turn it into 32 bit binary number
    final_y = format(final_y,'032b')
    
    #xored with shifted 0 so is the final value
    y = final_y[:shift_val]

    for i in range(shift_val,w,shift_val):
        #string of bits that have changed after xored equal 
        #to shift
        y_changed = final_y[i:shift_val+i]
        #take coresponding bits of unchanged
        y_unchanged = y[i-shift_val:i][:len(y_changed)]
        
        #xor
        x = int(y_unchanged,2) ^ int(y_changed,2)
        
        y += format(x, f'0{len(y_changed)}b')

    return int(y, 2)

def undo_left_shift(final_y:int,shift_val:int,add_val:int)->int:
    '''
    parm1: final_y which is left shifted by left shift 
    param2: shift val
    param3: value to which requied value is AND
    '''
    final_y = format(final_y,'032b')
    add_val = format(add_val,'032b')
    
    #(<shifted> 0 & anything == 0 ^ x == x so is the final value
    y = final_y[-shift_val:]
    
    for i in range(shift_val,w,shift_val):
        #string of bits that have changed after xored equal 
        #to shift

        y_changed = final_y[-shift_val-i:-i]
        #bits we have already figured out 

        y_unchanged = y[:shift_val]
        #bits that needs to be and with shifted bits

        a_val = add_val[-shift_val-i:-i]
        #first and between magic number and then xor with changed

        x = int(y_changed,2) ^ (int(y_unchanged,2) & int(a_val,2))
        y = format(x, f'0{len(y_changed)}b') + y
    
    return int(y,2)

def untemper(x:int)->int :
    #untamper the tampering function         
        pre_L_shift_num = undo_right_shift(x, l)
        pre_T_shift_num = undo_left_shift(pre_L_shift_num, t, c)
        pre_S_shift_num = undo_left_shift(pre_T_shift_num, s, b)
        rng_state = undo_right_shift(pre_S_shift_num, u)
        return rng_state
        

if __name__ == '__main__':
    (w, n, m, r) = (32, 624, 397, 31)
    a = 0x9908B0DF
    (u, d) = (11, 0xFFFFFFFF)
    (s, b) = (7, 0x9D2C5680)
    (t, c) = (15, 0xEFC60000)
    l = 18
    f = 1812433253
    j = 0
    
    state = get_state()
    
    for i in MT19937_32():
        y = untemper(i)
        print('untempered',y)    
        j = j + 1  
        if j == 624:
            break
    
