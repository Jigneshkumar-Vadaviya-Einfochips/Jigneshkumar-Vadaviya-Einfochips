#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Module contains support methods for csv files.
    Additional support methods can be added as needed.

"""
import os
import csv

CSV_SUFFIX = '.csv'


def write_dictionary_list_to_csv_file(header_list, dict_list, file_name, path=None, append=False):
    """
    write the header list and dictionary list to the specified csv file.
    If the file exists the contents will be over written.
    e.g.
    For the following header list and dictionary list:
        header_list = ['header1', 'header2', 'header3']
        dict_list = [{'header1': 'a', 'header2': 'b', 'header3': 'c'}, {'header1': 'd', 'header2': 'e', 'header3': 'f'}]
    The list contents will be written to the csv in the following format:
        header1, header2, header3
        a, b, c
        d, e, f

    :param header_list: the list of keys to be written to row 1 of the csv file
    :param dict_list: dictionary list to be written to the csv file.
            Verification of the format is required of the caller.
    :param file_name: file name for the csv file. The '.csv' extension will be added if not included
    :param path: path to the directory to write the file. The directory will be created if it doesn't exist
    :param append: True if want to append dictionary list data in existing csv file.
                    False if want to add dictionary list data with header.
    :return:    successful: status = True, err_str = ""
                unsuccessful: status = False, err_str = error string with failure details
    """

    status = False
    err_msg = ""

    # add .csv suffix if not included in the file name
    if file_name[-4:] != CSV_SUFFIX:
        file_name += CSV_SUFFIX

    try:
        # check if the directory exists and create one if it doesn't
        if path is not None:
            if not os.path.exists(path):
                os.makedirs(path)
            file_path = os.path.join(path, file_name)
        else:
            file_path = file_name

        # write the dictionary list to the csv file
        with open(file_path, 'a') as f:
            cout = csv.DictWriter(f, header_list)
            if cout:
                if not append:
                    cout.writeheader()
                cout.writerows(dict_list)
                status = True
            else:
                err_msg = "Error: failed to create cout file for: file: {}".format(file_name)
    except Exception as e:
        err_msg = "Error: failed to write to dictionary to csv file: exception: {}".format(e)

    return status, err_msg


def read_rows_as_dictionary_list_from_csv_file(file_name, path=None):
    """
    Read the contents of a csv file to a dictionary list.
    The first line of the csv file will be used as the keys for the contents of each of the preceding lines.
    e.g.
    For the following csv file contents:
        header1, header2, header3
        a, b, c
        d, e, f
    The following dictionary list will be returned:
        [{'header1': 'a', 'header2': 'b', 'header3': 'c'}, {'header1': 'd', 'header2': 'e', 'header3': 'f'}]

    The list is an ordered list from row 2 to row n
    An empty cell will return an empty string for the dictionary key.

    :param file_name: file name for the .csv file.
    :param path: path to the directory to read the file.
    :return:    successful: status = True, rtn_list = dictionary list of csv file, err_str = ""
                unsuccessful: status = False, rtn_list = [], err_str = error string with failure details
    """

    status = False
    err_msg = ""
    rtn_list = []

    # check if the file has a csv suffix
    if file_name[-4:] == CSV_SUFFIX:

        try:
            # check if the directory exists
            if path is not None:
                    file_path = os.path.join(path, file_name)
            else:
                file_path = file_name

            if os.path.exists(file_path):
                # return an empty dictionary if the file size is 0
                file_size = os.stat(file_path).st_size
                # read the dictionary from the csv file
                if file_size:
                    with open(file_path, 'rt') as f:
                        cin = csv.DictReader(f)
                        rtn_list = [row for row in cin]

                if len(rtn_list):
                    status = True
                else:
                    err_msg = "Error: the requested csv file is empty, file_name: {}".format(file_name)

            else:
                err_msg = "Error: the requested file path does not exist, file_path: {}".format(file_path)
        except Exception as e:
            err_msg = "Error: failed to read the list from the csv file: exception: {}".format(e)
    else:
        err_msg = "Error: the requested file type is not csv, file_name: {}".format(file_name)

    return status, rtn_list, err_msg
