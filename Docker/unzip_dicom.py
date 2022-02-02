#!/usr/bin/env python
# tf 2.4.1
# Instructions:
# save /tmp/DZIP/*.dicom to /tmp/DIMG/*.jpg
# Call by ahsoka/tensorflow-rush:0.3.0
#
# \author     Xuchu Liu (xuchu_liu@rush.edu)
# \date       2/2/2021
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
        destination_level = context.destination.get("type")
        if destination_level is None:
            log.error(f"invalid destination {destination_level}")
            raise Exception("Invalid gear destination")

        # Get the destination group/project
        destination = context.destination
        output_dir = context.output_dir

        log.debug(destination)
        log.debug(output_dir)

    except Exception as e:
        log.exception(e)
        exit_status = 1
    
    sys.exit(exit_status)