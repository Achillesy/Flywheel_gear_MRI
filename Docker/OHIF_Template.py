import logging
import copy
import uuid

logging.basicConfig(level="INFO")
log = logging.getLogger("OHIF")

Length_Template = {
    "active": False,
    "color": "rgba(255,255,255,0.2)",
    "description": "description",
    "flywheelOrigin": {"id": "userid", "type": "user"},
    "frameIndex": 0,
    "handles": {
        "end": {"active": False, "highlight": True, "moving": False, "x": 0, "y": 0,},
        "start": {"active": False, "highlight": True, "x": 0, "y": 0,},
        "textBox": {
            "active": False,
            "allowedOutsideImage": True,
            "drawnIndependently": True,
            "hasBoundingBox": False,
            "hasMoved": False,
            "movesIndependently": False,
            "x": 0,
            "y": 0,
        },
    },
    "imagePath": "1.3.6",
    "invalidated": False,
    "length": 0,
    "lesionNamingNumber": 1,
    "location": "Brain",
    "measurementNumber": 1,
    "sliceNumber": 0,
    "timepointId": "TimepointId",
    "SeriesInstanceUID": "1.3.6",
    "SOPInstanceUID": "1.3.6",
    "StudyInstanceUID": "1.3.6",
    "toolType": "Length",
    "visible": True,
}


class OHIF:
    def __init__(self, current_session):

        log.info(f"Initializing OHIF by session: {current_session.label}")
        self.my_session = current_session
        if "info" not in self.my_session:
            self.my_session["info"] = {}
        self.my_metadata = self.my_session.info
        if "ohifViewer" not in self.my_metadata:
            self.my_metadata["ohifViewer"] = {}
        self.ohif_metadata = self.my_metadata["ohifViewer"]
        if "measurements" not in self.ohif_metadata:
            self.ohif_metadata["measurements"] = {}
        self.measure_metadata = self.ohif_metadata["measurements"]
        if "Length" not in self.measure_metadata:
            self.measure_metadata["Length"] = []
        self.length_metadata = self.measure_metadata["Length"]

    # context.update_container_metadata('session', {'info': ohifViewer.to_json()})
    def update(self):
        self.my_session.update_info(self.my_metadata)

    def addLengths(
        self,
        flywheel,
        file_id,
        inst_name,
        mmLens,
        lensText,
        lensColor,
        lens_1x,
        lens_1y,
        lens_2x,
        lens_2y,
        instanceNumber,
        desp
    ):
        log.info("Add %s to Length: %s", desp, file_id)
        Lens_Length = copy.deepcopy(Length_Template)
        Lens_Length["_id"] = str(uuid.uuid4())
        Lens_Length["description"] = f"{lensText} - {desp}"
        num_Length = len(self.length_metadata)
        Lens_Length["handles"]["end"]["x"] = lens_1x
        Lens_Length["handles"]["end"]["y"] = lens_1y
        Lens_Length["handles"]["start"]["x"] = lens_2x
        Lens_Length["handles"]["start"]["y"] = lens_2y
        Lens_Length["handles"]["textBox"]["x"] = lens_2x
        Lens_Length["handles"]["textBox"]["y"] = lens_2y
        Lens_Length["length"]=mmLens
        Lens_Length["lesionNamingNumber"] = num_Length + 1
        Lens_Length["location"]="Brain"
        Lens_Length["measurementNumber"] = num_Length + 1
        Lens_Length["sliceNumber"] = int(instanceNumber)
        Lens_Length["toolType"]="Length"

        user = flywheel.get_current_user()
        Lens_Length["flywheelOrigin"]["id"]  = user.id

        lens_file = flywheel.get_file(file_id)
        Lens_Length["SeriesInstanceUID"] = lens_file["info"]["SeriesInstanceUID"]
        Lens_Length["SOPInstanceUID"] = inst_name # lens_file["info"]["SOPInstanceUID"]
        Lens_Length["StudyInstanceUID"] = lens_file["info"]["StudyInstanceUID"]

        path_delimiter = "$$$"
        path_suffix = "0"
        imagePath = (
            f'{Lens_Length["StudyInstanceUID"]}'
            f'{path_delimiter}'
            f'{Lens_Length["SeriesInstanceUID"]}'
            f'{path_delimiter}'
            f'{Lens_Length["SOPInstanceUID"]}'
            f'{path_delimiter}'
            f'{path_suffix}'
        )
        Lens_Length["imagePath"] = imagePath
        Lens_Length["color"] = "rgba(%d,%d,%d,0.2)" % (lensColor[2], lensColor[1], lensColor[0])
        self.length_metadata.append(Lens_Length)
