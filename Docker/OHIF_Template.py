import logging

logging.basicConfig(level="INFO")
log = logging.getLogger("ROI")

class OHIF:
    def __init__(self, context):

        log.info("Initializing OHIF")

    def to_json(self):
        log.info("to_json()")