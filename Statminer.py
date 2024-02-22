from process_frame_data import ld_scoreboard_check
from process_scoreboard import ScoreboardProcessor
import pickle
import csv
import cv2
import os

CSV_KEYS = ["player", "kills", "assists", "deaths", "damage", "healing", "mitigation"]


# TODO: make this not take args, it makes it so you can't really use it in the python3 console
class Statminer:
    """
    If pickle flag is detected, it writes the pickle like a csv, where first pickle.load() will return the keys
    and all of the next will be player data
    
    In both cases it loops from player1 to player10, for each scoreboard.
    """
    def __init__(self, infile, outfile, pickle=False, manual=False, verbose=False):
        # self._args = args # argparser.parse_args() output
        self.infile = infile
        self.outfile = outfile
        self.pickle = pickle
        self.manual = manual
        self.verbose = verbose

        self._output_file = None # set by _setup_outfile()
        self._csvwriter = None # set by _setup_outfile() if pickle flag is chosen, it is not set
        self._write_func = None # set by _setup_outfile() _csvwriter.writerow(), if pickle flag its pickle.dump()
        self.data = {}  
        self._output_file = self._setup_outfile()
         

    def write_array(self, file, array):
        if self.pickle:
            pickle.dump(array, file)
            pass
        else:
            self._write_func(array)
            pass
    
    def write(self, data):
        """
        gets self._write_func and uses it to write data.
        """
        print("writing: " + str(data))
        if self._csvwriter is not None:
            self._write_func(data)
        else:
            self._write_func(data, self._output_file)
        # return 1
    
    def _setup_outfile(self):
        if not self.pickle:
            self._output_file = open(self.outfile, 'w')
            self._csvwriter = csv.writer(self._output_file)
            self._write_func = self._csvwriter.writerow
        else:
            self._output_file = open(self.outfile, 'wb')
            self._write_func = pickle.dump
        self.write(CSV_KEYS)
        # return output_file
    
    def run(self):
        # amount of frames to skip
        nth_frame = 30 # round(60 / frames_per_second)
        vidcap = cv2.VideoCapture(self.infile)
        success,image = vidcap.read()
        count = 0
        while success:
            is_scoreboard = ld_scoreboard_check(image)
            if is_scoreboard:
                self._verbose_print("frame " + str(count) + " is a scoreboard, extracting data")
                count += 900 # NOTE: 900 frames is roughly 15 seconds
                vidcap.set(cv2.CAP_PROP_POS_FRAMES, count) # skip 15 seconds
                sp = ScoreboardProcessor(image, count, manual=self.manual, verbose=self.verbose)
                for player in sp.ocr_data:
                    self.write(player)
                # self.write(sp.ocr_data)
                self.data[str(count)] = sp
                # if self.save:
                #     save_path = os.path.
            count += nth_frame
            vidcap.set(cv2.CAP_PROP_POS_FRAMES, count) # fast forward 
            success,image = vidcap.read()


    def _verbose_print(self, string):
            if self.verbose:
                print(string)
