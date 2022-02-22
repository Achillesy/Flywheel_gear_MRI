from pathlib import Path
import pathvalidate as pv
import sys
import logging
import json

import flywheel
import flywheel_gear_toolkit as gt

from utils import import_data as id, csv_utils as cu

log = logging.getLogger()


def main(json_file, api_key, dry_run, output_dir, destination):

    exit_status = 0

    try:
        # Initialize the flywheel client using an API-ket
        fw = flywheel.Client(api_key)

        destination = fw.get(destination['id'])
        group = fw.get_group(destination.parents.group)
        project = fw.get_project(destination.parents.project)
        log.debug(f'working in project {project.label}')

        # We now assume that this data is being uploaded to the group/project that the gear is being run on.

        # import the json file
        jf = open(json_file, 'r')
        jsondata = json.load(jf)
        jf.close
        log.debug(jsondata)

        # # Format the data for ROI's from the data headers and upload to flywheel
        # Format the data for ROI's from the data headers and upload to flywheel
        # df = id.import_data(fw, df, group, project, dry_run)

        # # Save a report
        # cu.save_df_to_json(df, output_dir)

    except Exception as e:
        log.exception(e)
        exit_status = 1

    return exit_status


def process_gear_inputs(context):

    # First extract the configuration options
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

    # Get the path of the json file provided by the user
    json_file = context.get_input_path("json_file")

    # The gear shouldn't run if this isn't provided but we check anyway.
    if json_file is None or not Path(json_file).exists():
        log.error("No file provided or file does not exist")
        raise Exception("No valid json file")

    # Pathify `json_file` as it is currently a string, and extract data parts.
    json_file = Path(json_file)
    name = json_file.stem
    valid_name = pv.sanitize_filename(name)

    if len(valid_name) == 0:
        log.error(
            "You made your filename entirely out of invalid characters."
            "Just go home and think about that."
            "You are a danger to computers."
        )
        raise Exception("Invalid json file name")

    # Extract the various config options from the gear's config.json file.
    # These options are created in the manifest and set by the user upon runtime.
    dry_run = config.get("dry-run", False)
    log.debug(f"dry_run is {dry_run}")

    # Check to make sure we have a valid destination container for this gear.
    destination_level = context.destination.get("type")
    if destination_level is None:
        log.error(f"invalid destination {destination_level}")
        raise Exception("Invalid gear destination")

    # Get the destination group/project
    destination = context.destination
    output_dir = context.output_dir

    return json_file, api_key, dry_run, output_dir, destination


if __name__ == "__main__":

    (json_file, api_key, dry_run, output_dir, destination) = process_gear_inputs(
        gt.GearToolkitContext()
    )

    result = main(json_file, api_key, dry_run, output_dir, destination)
    sys.exit(result)
