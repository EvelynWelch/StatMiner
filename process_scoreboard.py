import cv2 as cv2
import pytesseract
import numpy as np

# This set is using 1920x1080 px images.
# This file is for valorant


# So it looks right now that the stuff shown here: https://stackoverflow.com/questions/62042172/how-to-remove-noise-in-image-opencv-python
# the binary output on an inverted image gives really readable text in white boxes.
# looking for the white boxes and just cutting out around htem, and using them for the input.

# The other thing to note is that I should be able to cut exact boxes around all of the text
# I just need to figure out how to get the bound correctly.
# just going through and cutting exact rectangles out around the data I need and then running
# Tesseract on each of the images.
# NOTE: as long as the aspect ratio doesn't change, all of the locations should stay consistent
#       when compared to %width and height of the image. This means I Just need to go through and
#       figure out all the boxes.
#       something like go get all of the rows, then break each row down into all the columns
#       then run each snippet through tesseract and save the text to the desired dict key


# Overwatch2 scoreboard rectagnles for 1080p
# NOTE: these are y, x tuples
blue_top_left = (313, 159)
blue_bottom_right = (313, 500)
blue_top_right = (1162, 159)
blue_bottom_left = (1162, 500)

# red team
red_top_right = (313, 612)
red_bottom_right = (313, 919)
red_top_left = (1162, 919)
red_bottom_left = (1162, 612)

# each column should be this size on 1080p images
column_yx_size = (60, 845)

# cuts each column out of a scoreboard display
# TODO: make this determine the regions based on img display ratio
# NOTE: current implimentation is only good for 1080p images
def cut_out_columns(img):
    # img = cv2.imread("test_videos/extracted_frames/ow_scoreboard.png")
    blue_cols = []
    red_cols = []
    blue_y = 195
    red_y = 612
    x = 315

    for i in range(5):
        # print("blue_y: " + str(blue_y))
        # blue_cols[i] = cut_out(img, x, blue_y)
        blue_cols.append(cut_out(img, x, blue_y))
        blue_y += 62
        # print("red_y: " + str(red_y))
        red_cols.append(cut_out(img, x, red_y))
        # red_cols[i] = cut_out(img, x, red_y)
        # red_cols[i] = img[red_y : red_y + 60, x : x + 850]
        red_y += 62
    return (blue_cols, red_cols)


def cut_out(img, x, y):
    """ 
    
    """
    return img[y:y+ 62, x:x + 850]


# NOTE: this doesn't extract names.
def get_rows_from_column(img):
    rows = []
    current_x = 365  # the start of th kda
    next = 60
    for i in range(6):
          # spacing for kda
        if i == 3: # after kda increase spacing 
            next = 100 
        rows.append(img[0 : 60, current_x:current_x + next])
        current_x += next
    return rows


def add_boarder(image, value=[0,0,0]):
    top = 5  # shape[0] = rows
    bottom = top
    left = 5  # shape[1] = cols
    right = left
    v = value
    boardered_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, None, v)
    return boardered_image

def scale_image(image, scale_percent=150):
    s = scale_percent # percent of original size
    width = int(image.shape[1] * s / 100)
    height = int(image.shape[0] * s / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return resized


def erode(image):
    # Creating kernel
    kernel = np.ones((2, 2), np.uint8)
    # Using cv2.erode() method 
    img = cv2.erode(image, kernel, iterations=1) 
    return img


def clean_image(image1):
    out_img = cv2.bitwise_not(image1)
    image=cv2.cvtColor(out_img,cv2.COLOR_BGR2GRAY)
    
    se=cv2.getStructuringElement(cv2.MORPH_RECT , (4,4))
    # se=cv2.getStructuringElement(cv2.MORPH_RECT , (8,8))
    bg=cv2.morphologyEx(image, cv2.MORPH_DILATE, se)
    out_gray=cv2.divide(image, bg, scale=255)
    out_binary=cv2.threshold(out_gray, 0, 255, cv2.THRESH_OTSU )[1] 
    return out_binary


def show_image(image):
    cv2.imshow("image",  image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_user_input_data():
    kills = input("kills: ")
    assists = input("assists: ")
    deaths = input("deaths: ")
    damage = input("damage: ")
    healing = input("healing: ")
    mitigation = input("mitigation: ")
    return [kills, assists, deaths, damage, healing, mitigation]

def get_user_input_for_image(image):
    cv2.imshow("scoreboard column", image)
    data = get_user_input_data()
    cv2.destroyAllWindows()
    return data

def preprocess_image(image, preprocessing_functions):
    """
    image: image to be modified
    preprocessing_functions: a list of functions to run the image through, NOTE: it starts at 0 and works its way thorugh
    """
    img = image
    for i in range(len(preprocessing_functions)):
        img = preprocessing_functions[i](img)
    return img


def process_column(column):
    # TODO: make this add playerX
    """
    column: a cut out horizontal column from a scoreboard

    returns: an array with [kills, assists, deaths, damage, healing, mitigation, full_column]
    the final element is the full column that has been analyzed.
    """
    rows = get_rows_from_column(column)
    # rows.append(cut_off_player_name(column))
    data = []
    preprocessing_funcs = [
        # clean_image,
        scale_image,
        add_boarder,
    ]
    for i in range(len(rows)):
        image = preprocess_image(rows[i], preprocessing_functions=preprocessing_funcs)
        output = run_ocr(image, config="--psm 11 --oem 3 digits")
        # print(output)
        # if it finds an empty string 0 it out
        if output == "": 
            output = '0'
        # cv2.imshow("r", image)
        # cv2.waitKey(0)
        output = clean_string(output)
        data.append(output)
    return data


def cut_off_player_name(image):
    return image[0:60, 375: 840]

def run_ocr(image, config="--psm 3"):
    return pytesseract.image_to_string(image, config=config)


# returns an len 10 array with each array being [player, kills, assists, deaths, damage, healing, mitigation]
def process_scoreboard(scoreboard_image):
    if scoreboard_image is None:
        return
    blue_team, red_team = cut_out_columns(scoreboard_image)
    both_teams = blue_team + red_team
    d = []
    # print("processing image")
    for i in range(len(both_teams)):
        p = both_teams[i]
        if p is not None:
            cut = cut_off_player_name(p)
            x = clean_image(cut)
            s = scale_image(x, scale_percent=300)
            try:
                ocr_output = run_ocr(s, config="--psm 7 --oem 3 digits")
                checked_output = check_ocr_output(ocr_output, p)
                player_name = "player" + str(i+1)
                checked_output.insert(0, player_name)
                d.append(checked_output)
            except:
                d.append(None)
    return d

# a dict with where key is a string of what frame the scoreboard was found
# and value = len 10 arrays, each nested array has [player, kills, assists, deaths, damage, healing, mitigation]
def process_scoreboards(scoreboard_images):
    data = {}
    for k, v in scoreboard_images.items():
        scoreboard_data = process_scoreboard(v)
        data[k] = scoreboard_data
    return data

def clean_string(string):
    s = string.strip()
    s = s.replace(".", "")
    s = s.replace("\n", "")
    return s

def check_ocr_output(ocr_output, image):
    # this gets passed the unprocessed image of the col so it can be passed to the split rows and stuff
    cleaned_ocr_output = clean_string(ocr_output)
    split_output = cleaned_ocr_output.split(" ")
    # for i in range(len(split_output)):
    # print("split_output: " + str(split_output))
    if len(split_output) == 6:
        # NOTE: there could still be errors here
        # print("no problem found")
        return split_output
    else:
        # TODO: make this tell you what frame
        # print("found a problem with a frame...")
        d = process_column(image)
        return d


# sets an index as 1 if they match 0 if not, and -1 if sb_column didn't have an index there
def get_matching_indecies(row_data, sb_column):
    matching_indecies = []
    for j in range(len(row_data)):
        col_d = None
        if j < len(sb_column) -1:
            col_d = sb_column[j]
        row = row_data[j]
        if col_d is not None:
            if col_d == row:
                matching_indecies.insert(j, 1)
            else:
                matching_indecies.insert(j, 0)
        else:
            matching_indecies.insert(j, -1)


def check_whole_scoreboard(full_scoreboard_ocr_data, scoreboard_cols):
    # TOOD: figure out how to make this work well....
    for i in range(len(full_scoreboard_ocr_data)): # full_scoreboard_ocr_data's indecies should be the ocr'd output of scoreboard_cols indecies
        sb_column = full_scoreboard_ocr_data[i]
        sanitized_data = []
        if len(sb_column) != 6: # this should change if the playerX hasn't been added or if the frame is added
            row_data = process_column(scoreboard_cols[i])
            offset = len(row_data) - len(sb_column) # the -1 is because the player data
            matching_indecies = get_matching_indecies(row_data, sb_column)
            for j in range(len(matching_indecies)):
                m = matching_indecies[j]
                if m == 1:
                    # they match
                    sanitized_data.insert(j, row_data[j])
                    pass
                elif m == 0:
                        # they both have something there
                    pass
                elif m == -1:
                        # this index doesn't exist in sb_column
                    pass
                else:
                    print("something went horribley wrong checking data validity")


class ScoreboardProcessor:
    """
    args: argparse.get_args()
    image: cv2 image of a scoreboard


    """
    def __init__(self, image, frame, verbose, manual,):
        self.frame = frame
        self.image = image
        self.manual = manual
        self.verbose = verbose
        self.alt_data = {}
        self.preprocess_funcs = [
            cut_off_player_name,
            # erode,
            # clean_image,
            scale_image,
        ]
        self.ocr_data = self._process_scoreboard(image)
        
        

    def _process_scoreboard(self, scoreboard_image):
        if scoreboard_image is None:
            return
        blue_team, red_team = cut_out_columns(scoreboard_image)
        both_teams = blue_team + red_team
        d = []
        # print("processing image")
        for i in range(len(both_teams)):
            p = both_teams[i]
            if p is not None:
                # cut = cut_off_player_name(p)
                # x = clean_image(cut)
                # s = scale_image(x)
                preprocessed_image = preprocess_image(p, preprocessing_functions=self.preprocess_funcs)
                
                # try:
                ocr_output = self._run_ocr(preprocessed_image, config="--psm 7 --oem 3 digits")
                # print("ocr_output: " + str(ocr_output))
                checked_output = self._check_ocr_output(ocr_output, p)
                player_name = "player" + str(i+1)
                self.alt_data[player_name] = [ocr_output, checked_output] # add both unchecked data, and checked data to a dict
                checked_output.insert(0, player_name)
                # print("checked_output: " + str(checked_output))

                d.append(checked_output)

                # cv2.imshow("s", preprocessed_image)
                # cv2.waitKey(0)
                # except:
                #     d.append("")
        # print("ScoreboardProcessor.d: " + str(d))
        return d
    
    def _run_ocr(self, image, config="--psm 3"):
        return pytesseract.image_to_string(image, config=config)
    
    def _check_ocr_output(self, ocr_output, image):
        # this gets passed the unprocessed image of the col so it can be passed to the split rows and stuff
        cleaned_ocr_output = self._clean_string(ocr_output)
        split_output = cleaned_ocr_output.split(" ")
        # for i in range(len(split_output)):
        # print("split_output: " + str(split_output))
        if len(split_output) == 6:
            # NOTE: there could still be errors here
            self._verbose_print("frame: " + str(self.frame) + " successfully processed")
            return split_output
        else:
            if len(split_output) == 5:
                # assume it didn't catch the 0 mitigation
                if int(split_output[2]) > 100:
                    # it probably missed a 0 in the kda so we put a 0 in assists
                    split_output.insert(1, '0') 
                else:
                    split_output.append("0")
                return split_output
            self._verbose_print("error processing frame: " + str(self.frame))
            self._verbose_print("ocr values: " + str(split_output))
            if self.manual:
                d = self._get_user_input_for_image(image)
            # TODO: make this tell you what frame
            else:
                self._verbose_print("trying alternative method to get sane values.")
                d = process_column(image)
                self._verbose_print("sane values: " + str(d))

            return d
        
    def _clean_string(self, string):
        s = string.strip()
        s = s.replace(".", "")
        s = s.replace("\n", "")
        return s
    
    def _get_user_input_data():
        print("manual input mode entered.")
        kills = input("kills: ")
        assists = input("assists: ")
        deaths = input("deaths: ")
        damage = input("damage: ")
        healing = input("healing: ")
        mitigation = input("mitigation: ")
        return [kills, assists, deaths, damage, healing, mitigation]

    def _get_user_input_for_image(self, image):
        cv2.imshow(str(self.frame), image)
        data = get_user_input_data()
        cv2.destroyAllWindows()
        return data
    
    def _verbose_print(self, string):
        if self.verbose:
            print(string)
