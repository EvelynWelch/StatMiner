#Statminer is a program created to extract data from scoreboards displayed in video recordings of Overwatch 2 gameplay.

##Installation
statminer requires
python3
cv2
Tesseract OCR (it was developed using 5.3)
numpy

##Usage
python3 statminer.py -i {INPUT_VIDEO} -o {OUTPUT_FILE}

  -h, --help            show this help message and exit
  
  -i INFILE, --infile INFILE		 Path to the video file.
  
  -o OUTFILE, --outfile OUTFILE		 File to ouput data. (defaults to csv, if -p flag it will save as a pickle)
  
  -p, --pickle         			 Save output as a pickle
  
  -m, --manual         			 Makes it so if an error is detected with the OCR it will display the image, and have   you manually input the data
  
  -v, --verbose         		 Increase output verbosity.
  




