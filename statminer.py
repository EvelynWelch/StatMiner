#!/usr/bin/python3

import process_frame_data
import process_scoreboard
import sys, getopt
import os
import ntpath
# import csv_writer
import cv2
# import pickle_handler

import argparse
from Statminer import Statminer

def get_parser(h):
    parser = argparse.ArgumentParser(add_help=h)
    parser.add_argument("-i", "--infile", help="Path to the video file.", required=True)
    parser.add_argument("-o", "--outfile", help="File to ouput data. (defaults to csv, if -p flag it will save as a pickle)", required=True)
    parser.add_argument("-p", "--pickle", help="Save output as a pickle", action="store_true")
    parser.add_argument("-m", "--manual", help="Makes it so if an error is detected with the OCR it will display the image, and have you manually input the data", action="store_true")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity.", action="store_true")
    # parser.add_argument("-s", "--save_scoreboards", help="Save extracted scoreboard images to location.")
    return parser


def get_test_images():
    test_image_dir = "test_videos/sb_test/"
    images = {}
    file_list = os.listdir(test_image_dir)
    for f in file_list:
        try:
            images[f] = cv2.imread(test_image_dir + f)
        except:
            pass
    return images

def main1(argv):
    inputfile = ''
    outputfile = ''
    # get the command line options
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    # check if input file exists
    if not os.path.exists(inputfile):
        print("file " + inputfile + " does not exist")
        sys.exit(2)
    
    # extract scoreboards from video
    print ('processing: ', inputfile)
    # scoreboards = process_frame_data.read_video(inputfile, 2)
    scoreboards = get_test_images()
    # extract data from scoreboards
    print("getting data from scoreboards.")
    # a dict with k=extracted_frame_number v=array of arrays of scoreboard data 
    scoreboard_data = process_scoreboard.process_scoreboards(scoreboards)
    # scoreboard_data = pickle_handler.get_pickled_data("test_data.pickle")
    print("saving to pickle: test_data.pickle")
    pickle_handler.save_pickle(scoreboard_data, "test_data.pickle")

    # output scoreboard data as csv
    # print ('Output file is "', outputfile)
    print("writing csv file to: " + outputfile)
    if outputfile == "":
        directory, infile_name = ntpath.split(inputfile)
        outputfile = infile_name.split('.')[0] + "_scoreboards.csv"
    
    
    
    csv_writer.write_data_to_csv(scoreboard_data, outputfile)


if __name__ == "__main__":
    parser = get_parser(h=True)
    args = parser.parse_args()
    i = args.infile
    o = args.outfile
    m = args.manual
    v = args.verbose
    p = args.pickle

    sm = Statminer(infile=i, outfile=o, manual=m, verbose=v, pickle=p)
    sm.run()
    # print(str(args.input))

#    main1(sys.argv[1:])
