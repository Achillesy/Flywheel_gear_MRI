#!/usr/bin/env python
# tf 2.4.1
# Instructions:
# save /tmp/DZIP/*.dicom to /tmp/DIMG/*.jpg
# Call by ahsoka/tensorflow-rush:0.3.0
#
# \author     Xuchu Liu (xuchu_liu@rush.edu)
# \date       2/2/2021
import os
import sys
import logging
import zipfile
# import json

import flywheel_gear_toolkit as gt

log = logging.getLogger()

if __name__ == '__main__':
    exit_status = 0

    try:
        context = gt.GearToolkitContext()
        config = context.config

        # Setup basic logging and log the configuration for this job
        if config["gear_log_level"] == "INFO":
            context.init_logging("info")
        else:
            context.init_logging("debug")
        context.log_config()

        cur_session = context.get_destination_parent()
        log.debug(f'working in session {cur_session.label}')
        # with open("/flywheel/v0/output/cur_session.josn", "w") as f:
        #     json.dump(cur_session, f)

        acquisitions = cur_session.acquisitions()
        # work_dir = context.work_dir
        work_dir = "/tmp/DZIP"
        for acquisition in acquisitions:
            # Assume only one file per acquisition, could filter for dicom files if needed
            file_ = acquisition.files[0]
            file_name_upper = file_.name.upper()
            if ("SAG" in file_name_upper) and (file_name_upper.endswith(".ZIP")):
                # Create a destinatino directory for this acqusitions file
                # acq_dir = os.path.join(work_dir, acquisition.label)
                acq_dir = os.path.join(work_dir, file_.file_id)
                os.makedirs(acq_dir)
                # Download file
                acq_file = os.path.join(acq_dir, file_.name)
                file_.download(acq_file)
                # Unzip if necessary
                with zipfile.ZipFile(acq_file, 'r') as zip_ref:
                    zip_ref.extractall(acq_dir)
    except Exception as e:
        log.exception(e)
        exit_status = 1
    
    sys.exit(exit_status)