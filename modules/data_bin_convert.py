import pickle


def data_to_bin(input, filename):
    fh = open(filename, 'wb')
    pickle.dump(input, fh) # converts array to binary and writes to output
    fh.close()


def bin_to_data(filename):
    fh = open(filename, 'rb')
    output =  pickle.load(fh) # Reads the binary and converts back to list
    fh.close()
    return output
