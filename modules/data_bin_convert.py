import logging
import pickle


def data_to_bin(input, filename):
    logging.debug(f'Writing to file: {filename=}')
    # Store some data in a binary file
    fh = open(filename, 'wb')
    pickle.dump(input, fh) # converts array to binary and writes to output
    fh.close()


def bin_to_data(filename):
    # Read the data from a binary file
    logging.debug(f'Reading from file: {filename=}')
    fh = open(filename, 'rb')
    output =  pickle.load(fh) # Reads the binary and converts back to list
    fh.close()
    return output
