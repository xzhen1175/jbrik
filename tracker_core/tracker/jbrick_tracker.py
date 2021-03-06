import commands
from utils import log_utils
from trackerlib import RubiksImage
import logging
import json

BASEPATH = "./tracker_core/tracker/"
#BASEPATH = "./"
PICPATH = "/tmp/jbrik/"
#PICPATH = BASEPATH + "resource/jbrik_img/"
CMDPATH = BASEPATH + "rubiks-cube-tracker.py -f "
PICNAME = "rubiks-side-"
PICTYPE = "png"
PICCMD = "raspistill -v -w 400 -h 400  -e " + PICTYPE + " -t 1 -sh 100 -br 50 -mm spot -o "


# Logging for direct tracker
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(filename)22s %(levelname)8s: %(message)s"
)
log = logging.getLogger(__name__)

# Color the errors and warnings in red
logging.addLevelName(
    logging.ERROR, "\033[91m   %s\033[0m" % logging.getLevelName(logging.ERROR)
)
logging.addLevelName(
    logging.WARNING, "\033[91m %s\033[0m" % logging.getLevelName(logging.WARNING)
)

def convert_face_pics_to_rgb_facemap(facenum, picrotcount):
    facemap = {}
    for j in range(0, picrotcount + 1):
        imgfile = PICPATH + PICNAME + facenum.__str__() + j.__str__() + "." + PICTYPE
        str = "python " + CMDPATH + imgfile
        log_utils.log("Converting image file: " + imgfile + " to rgb values.")
        raw_result = commands.getstatusoutput(str)[1]
        #raw_result = track_direct(imgfile)

        raw_result = raw_result.split("\n")
        raw_result = raw_result[-1]

        # attempt to skip a face that didn't get resolved correctly
        if not raw_result.startswith("{\""):
            facemap[j] = ""
            continue
        log_utils.log("Result: " + raw_result)
        facemap[j] = raw_result

    return facemap

def track_direct(imgfile):
    log.setLevel(logging.DEBUG)
    rimg = RubiksImage(0, "name", True)
    rimg.analyze_file(imgfile)

    return json.dumps(rimg.data, sort_keys=True)

# TODO raise an exception here based on command output
def photo_face(facenum, rotnum):
    # raspistill -q 100 -e png -t 1 -sh 100 -br 60 -o /tmp/rubiks-side-U.png
    # raspistill -v -w 400 -h 400  -e png -t 1 -sh 100 -br 50 -mm spot -o /tmp/jbrik/rubiks-side-10.png

    log_utils.log("Taking rotation pic: " + rotnum.__str__() + " of face: " + facenum.__str__())
    picstr = PICCMD + PICPATH + PICNAME + facenum.__str__() + rotnum.__str__() + "." + PICTYPE
    log_utils.log("Cmd: " + picstr)
    commands.getstatusoutput(picstr)
    log_utils.log("Rotate 90 CW")
