import pickle


def data_to_bin(input):
    fh = open('C:\\Users\\gunner\\Documents\\git\\personal-tv-guide\\saved_data.bin', 'wb')
    pickle.dump(input, fh) # converts array to binary and writes to output
    fh.close()


def bin_to_data():
    fh = open('C:\\Users\\gunner\\Documents\\git\\personal-tv-guide\\saved_data.bin', 'rb')
    output =  pickle.load(fh) # Reads the binary and converts back to list
    fh.close()
    return output
