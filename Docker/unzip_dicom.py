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

import flywheel
import flywheel_gear_toolkit as gt

log = logging.getLogger()

if __name__ == '__main__':
    exit_status = 0

    try:
        context = gt.GearToolkitContext()
        config = context.config

        # Examine the inputs for the "api-key" token and extract it
        for inp in context.config_json["inputs"].values():
            if inp["base"] == "api-key" and inp["key"]:
                api_key = inp["key"]

        # Setup basic logging and log the configuration for this job
        if config["gear_log_level"] == "INFO":
            context.init_logging("info")
        else:
            context.init_logging("debug")
        context.log_config()

        # Check to make sure we have a valid destination container for this gear.
        cur_dest = context.destination
        cur_dest_level = cur_dest.get("type")
        if cur_dest_level is None:
            log.error(f"invalid destination {cur_dest_level}")
            raise Exception("Invalid gear destination")

        # Get the destination group/project
        fw = flywheel.Client(api_key)
        dest_handle = fw.get(cur_dest['id'])
        # log.debug(dest_handle)
        # session_id = fw.get_project(dest_handle.parents.session)
        cur_session = fw.get_session(dest_handle.parents.session)
        log.debug(f'working in session {cur_session.label}')

        # destination = context.get_destination_parent() # Will be session if analysis is run at session as is default
        acquisitions = cur_session.acquisitions()
        # work_dir = context.work_dir
        work_dir = "/tmp/DZIP"
        for acquisition in acquisitions:
            # Assume only one file per acquisition, could filter for dicom files if needed
            file_ = acquisition.files[0]
            # Create a destinatino directory for this acqusitions file
            acq_dir = os.path.join(work_dir, acquisition.label)
            os.makedirs(acq_dir)
            # Download file
            acq_file = os.path.join(acq_dir, file_.name)
            log.debug(acq_file)
            #file_.download(acq_file)
            # Unzip if necessary
    except Exception as e:
        log.exception(e)
        exit_status = 1
    
    sys.exit(exit_status)