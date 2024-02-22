# This file takes a video and looks its frames and tries to determine if the frame has a scoreboard showing

import cv2
import numpy as np
import line_detection 


# returns the section of an image to be checked for a line 
# it is the rectangle containing the line to the right of "VS" in the middle of a scoreboard
def get_detection_area(img):
  return img[545:575, 775:1050]


# detects scoreboard using line detection on a specifi portion of the image
def ld_scoreboard_check(image):
  area_to_check = get_detection_area(image)
  check_lines = line_detection.is_scoreboard(area_to_check)
  # if it finds any line return true, else return false
  # NOTE: this does give false positives occasionaly
  if check_lines is not None:
    return True
  else:
    return False


# NOTE: add the ability to only read x frames a second.
# video_file_path: the file path to the video
# frames_per_second: the number of frames to analyze each second
def read_video(video_file_path, frames_per_second):
  """
  video_file_path: the video to analyze
  frames_per_second: the amnount of frames to check every second of the video. i.e. 2 will look at 2 frames every second

  return: a dict of {string, scoreboard_image} where string is the frame the scoreboard was found
  """
  nth_frame = round(60 / frames_per_second)
  vidcap = cv2.VideoCapture(video_file_path)
  success,image = vidcap.read()
  count = 0
  data = {}
  # print("nth_frame: ", nth_frame)
  # data["filepath"] = video_file_path
  while success:
    # if a scoreboard has been detected recently just skip frames
    # NOTE: i'm not sure how long 3600 seconds is
    # NOTE: I think there is a way to just skip forward frames.
    # if last_scoreboard > 0 and (last_scoreboard > count + 900):
    is_scoreboard = ld_scoreboard_check(image)
    if is_scoreboard:
      # use OCR to get data
      # data['frame' + str(count)] = image
      # video_tag = video_file_path.split("/")[1].split(".")[0] # delete this later.
      # print(video_tag)
      # write_path = "test_images/" + video_tag + "_frame"+ str(count) + ".jpg" 
      # cv2.imwrite(write_path, image)     # save frame as JPEG file      
      # print("scoreboard found image wrote to: " + write_path)
      count += 900 # NOTE: 900 frames is roughly 15 seconds
      vidcap.set(cv2.CAP_PROP_POS_FRAMES, count) # skip 15 seconds
      data[str(count)] = image
    
    # print('Read a new frame: ', count)
    count += nth_frame
    # print("frame: ", count)
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, count) # fast forward 
    success,image = vidcap.read()
  return data

# read_video(file_path, 2)