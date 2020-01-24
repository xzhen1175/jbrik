import commands
from utils import log_utils

PICPATH = "/tmp/jbrik/"
PICNAME = "rubiks-side-"
PICTYPE = "png"
PICCMD = "raspistill -v -w 400 -h 400  -e " + PICTYPE + " -t 1 -sh 100 -br 50 -mm spot -o "

def convert_face_pics_to_rgb_facemap(facenum, picrotcount):
    facemap = {}
    for j in range(0, picrotcount + 1):
        # imgfile = "./tracker_core/tracker/resource/jbrik_img/rubiks-side-" + i.__str__() + j.__str__() + ".png"
        imgfile = PICPATH + PICNAME + facenum.__str__() + j.__str__() + "." + PICTYPE
        str = "python ./tracker_core/tracker/rubiks-cube-tracker.py -f " + imgfile
        log_utils.log("Converting image file: " + imgfile + " to rgb values.")
        raw_result = commands.getstatusoutput(str)[1]
        # attempt to skip a face that didn't get resolved correctly
        if raw_result.__contains__("AssertionError"):
            facemap[j] = ""
            continue
        raw_result = raw_result.split("\n")
        raw_result = raw_result[-1]
        log_utils.log("Result: " + raw_result)
        facemap[j] = raw_result

    return facemap

# TODO raise an exception here based on command output
def photo_face(facenum, rotnum):
    # raspistill -q 100 -e png -t 1 -sh 100 -br 60 -o /tmp/rubiks-side-U.png
    # raspistill -v -w 400 -h 400  -e png -t 1 -sh 100 -br 50 -mm spot -o /tmp/jbrik/rubiks-side-10.png

    log_utils.log("Taking rotation pic: " + i.__str__() + " of face: " + facenum.__str__())
    picstr = PICCMD + PICPATH + PICNAME + facenum.__str__() + rotnum.__str__() + "." + PICTYPE
    log_utils.log("Cmd: " + picstr)
    commands.getstatusoutput(picstr)
    log_utils.log("Rotate 90 CW")
