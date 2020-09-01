def pkcs_padding(cipher,blocksize):
    padding_len = blocksize - len(cipher)
    print(bytes([padding_len]))
    for i in range(padding_len):
        cipher = cipher + bytes([padding_len])
    return(cipher)


chunks = []
text = input("Enter the data: ")
blocksize = int(input("Enter the block size: "))
cipher = str.encode(text)
print(pkcs_padding(cipher,blocksize))
