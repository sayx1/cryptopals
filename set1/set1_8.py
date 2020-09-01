import base64
#Initilization 
chunks = []
final = {}
max_val = 0
j = 0 

#Reading the file
fhandle = open('data.txt')

for line in fhandle:
    #counting the line number
    j = j + 1
    #hex to binary
    line = bytes.fromhex(line.strip())
    #selertitcts block of encrypted data
    blocksize = 16
    for i in range(0,len(line),blocksize):
        chunks.append(line[i:i+blocksize])
    #Finds the number of repeated chunks    
    repeat = len(chunks) - len(set(chunks))

    #For maximum chunks
    if (repeat >= max_val):
        final = {'line':line,'repeated':repeat, 'line_number':j}
        if (repeat == 3): break

print(final)
