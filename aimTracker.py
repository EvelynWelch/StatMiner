import cv2
import numpy as np
import matplotlib.pyplot as plt


# fp = "./testImages/ow_outline_img.png" # this image is not a full size image
fp = "./testImages/from_recording.png"


def openImage(filepath: str):
    image = cv2.imread(filepath)
    return image

# takes a frame of a video cuts out a small area and checks for hero outlines.
output = None

def getViewArea():
    # Calculate a center square based of image resolution
    # a square 1/4 of the size of the screen?
    # NOTE: the larger this is the more expensive it is to calculate (I don't know how big is to big, but my guess is it can be pretty big considering similar stuff gets run on arduinos)
    pass

def traceOutlines(image):
    # check pixels for the outline color, if found crawl along the pixels and trace the outline
    # to do this:
    # start at one side in the middle, and check to the other side looking for pixels
    # if a hitbox color is found use an object that tracks its direction and walks along the outline
    # something like facing direction [up, down, left, right] 
    # from there you could use a direction preference, so you don't trace the whole outline. just to a few pixels
    # or just map out the whole outline.



    # cv2 might have something that makes this super trivial like
    # filter all colors that aren't the outline color in a single function. \

   
    pass

def filterOutlines(image): 
    """
    Take an image and use cv2.inRange to leave enemy outlines.
    """
    # Blue Red Green tupples
    lowRange = (50, 50, 100)
    highRange = (75, 75, 255)
    mask = cv2.inRange(image, lowRange, highRange)
    return mask

def getDirectionAndDistanceToOutlines(outline):
    # check to see if the crosshair is in a hit box.
    # if not and there is a hitbox(es) gives you the direction and distance to the outlines
    pass

def processFrame():
    # takes a frame and outputs the extracted data.
    areaToProcess = getViewArea()
    outlineData = traceOutlines()
    out = []
    for outline in outlineData:
        out.append(getDirectionAndDistanceToOutlines(outline))
        pass

    pass


def test():
    image = openImage(fp)
    outline = traceOutlines(image)
    # cv2.imshow("img", outline)
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows() 

    
    plt.imshow(outline, cmap='gray')   # this colormap will display in black / white
    plt.show()

    pass




if __name__ == "__main__":
    test()