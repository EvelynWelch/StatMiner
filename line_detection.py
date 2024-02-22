# opencv line detection

# Python program to illustrate HoughLine
# method for line detection
import cv2
import numpy as np
  

# # filepath to the test file
fp = "test_videos/extracted_frames/ow_scoreboard.png"

# # Reading the required image in
# # which operations are to be done.
# # Make sure that the image is in the same
# # directory in which this python program is
img = cv2.imread(fp)
  
# # Convert the img to grayscale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
# # Apply edge detection method on the image
# edges = cv2.Canny(gray, 50, 150, apertureSize=3)
  
# # This returns an array of r and theta values
# lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
  
# # The below for loop runs till r and theta values
# # are in the range of the 2d array
# for r_theta in lines:
#     arr = np.array(r_theta[0], dtype=np.float64)
#     r, theta = arr
#     # Stores the value of cos(theta) in a
#     a = np.cos(theta)
  
#     # Stores the value of sin(theta) in b
#     b = np.sin(theta)
  
#     # x0 stores the value rcos(theta)
#     x0 = a*r
  
#     # y0 stores the value rsin(theta)
#     y0 = b*r
  
#     # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
#     x1 = int(x0 + 1000*(-b))
  
#     # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
#     y1 = int(y0 + 1000*(a))
  
#     # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
#     x2 = int(x0 - 1000*(-b))
  
#     # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
#     y2 = int(y0 - 1000*(a))
  
#     # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
#     # (0,0,255) denotes the colour of the line to be
#     # drawn. In this case, it is red.
#     cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
  
# # # All the changes made in the input image are finally
# # # written on a new image houghlines.jpg
# cv2.imwrite('linesDetected.jpg', img)


# # Read image
# image = cv2.imread(fp)
  
# # Convert image to grayscale
# gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  
# # Use canny edge detection
# edges = cv2.Canny(gray,50,150,apertureSize=3)
  
# # Apply HoughLinesP method to 
# # to directly obtain line end points
# lines_list =[]
# # this gives a single line at the top of frame if the scoreboard is showing (hopefully)
# # NOTE: i'm going to look more into edge canny edge detection and see how it can change
# #       the lines i'm getting. I'd like it to outline the scoreboards but it's not
# #       to do this i'll need make np show the images at both stages.
# lines = cv2.HoughLinesP(
#             edges, # Input edge image
#             1, # Distance resolution in pixels
#             np.pi/180, # Angle resolution in radians
#             threshold=250, # Min number of votes for valid line
#             minLineLength=500, # Min allowed length of line
#             maxLineGap=0 # Max allowed gap between line for joining them
#             )
  
# # Iterate over points
# for points in lines:
#       # Extracted points nested in the list
#     x1,y1,x2,y2=points[0]
#     # Draw the lines joing the points
#     # On the original image
#     cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
#     # Maintain a simples lookup list for points
#     lines_list.append([(x1,y1),(x2,y2)])
      
# # Save the result image
# cv2.imwrite('detectedLines.png',image)


# change this so it cuts out where the "VS" is showed in the middle and only line detect for 
# that line, make sure the line is equal to a test line.


# a function that takes a frame and uses line detection to see if it is a scoreboard
# It is looking for a single long line across the op of the screen.
# If it finds that line the tab menu should be open, so it returns true.
# It can potentially return true even if there is no scoreboard
# NOTE: this method doesn't work, when you die it creates the line that it is looking for
#       without the scoreboard showing, and then will skip over the scoreboard if they open it while
#       they are dead.
def is_scoreboard(frame):
  # Convert image to grayscale
  gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
  
  # Use canny edge detection
  edges = cv2.Canny(gray,50,150,apertureSize=3)
  
  # Apply HoughLinesP method to 
  # to directly obtain line end points
  lines_list =[]
  # this gives a single line at the top of frame if the scoreboard is showing (hopefully)
  # NOTE: i'm going to look more into edge canny edge detection and see how it can change
  #       the lines i'm getting. I'd like it to outline the scoreboards but it's not
  #       to do this i'll need make np show the images at both stages.
  lines = cv2.HoughLinesP(
            edges, # Input edge image
            1, # Distance resolution in pixels
            np.pi/180, # Angle resolution in radians
            threshold=150, # Min number of votes for valid line
            minLineLength=250, # Min allowed length of line
            maxLineGap=0 # Max allowed gap between line for joining them
            )
  # print("lines: ")
  # print(str(lines))
  # print("")
  # if lines has a length return true otherwise return false.
  # if lines is not None:
  #    return True
  # return False
  return lines

# sb = is_scoreboard(img)
# print(str(sb))