#!/usr/bin/env python
# tf 2.4.1
# Instructions:
# save /tmp/DZIP/*.dicom to /tmp/DIMG/*.jpg
# Call by ahsoka/tensorflow-rush:0.3.0
#
# \author     Xuchu Liu (xuchu_liu@rush.edu)
# \date       1/11/2021

import os
import sys

import pydicom

import pandas as pd

from PIL import Image
from pylib import normalization

dicom_path  = "/tmp/DZIP"
image_path  = "/tmp/DIMG"
output_path = "/flywheel/v0/output"

img_size = 512

def saveImgAndInfo(name, ds):
    info = {}
    info['Id'] = "%s_%04d_%04d" % (ds.AccessionNumber, ds.SeriesNumber, ds.InstanceNumber)
    info['DicomPath'] = name
    try:
        info['PatientName'] = ds.PatientName
    except:
        info['PatientName'] = "Anonymous"
    try:
        info['AccessionNumber'] = int(ds.AccessionNumber)
    except:
        info['AccessionNumber'] = 0
    info['SeriesNumber'] = ds.SeriesNumber
    info['InstanceNumber'] = ds.InstanceNumber
    info['Rows'] = ds.Rows
    info['Columns'] = ds.Columns
    info['PixelSpacing1'] = ds.PixelSpacing[0]
    info['PixelSpacing2'] = ds.PixelSpacing[1]

    raw_img = Image.fromarray(normalization(ds.pixel_array)*255).convert('L')
    jpg_sag_name = os.path.join(image_path, info['Id'] + '.jpg')
    raw_img.save(jpg_sag_name, 'jpeg')

    info['Pons_1x'] = 1
    info['Pons_1y'] = 1
    info['Pons_2x'] = 1
    info['Pons_2y'] = 1
    info['mmPons'] = 0
    info['Vermis_1x'] = 1
    info['Vermis_1y'] = 1
    info['Vermis_2x'] = 1
    info['Vermis_2y'] = 1
    info['mmVermis'] = 0
    info['HVermis_1x'] = 1
    info['HVermis_1y'] = 1
    info['HVermis_2x'] = 1
    info['HVermis_2y'] = 1
    info['mmHVermis'] = 0
    info['Fronto_1x'] = 1
    info['Fronto_1y'] = 1
    info['Fronto_2x'] = 1
    info['Fronto_2y'] = 1
    info['mmFronto'] = 0
    info['Fronto_Size'] = 0
    info['deltaPons'] = 0
    info['deltaVermis'] = 0
    info['deltaFronto'] = 0
    return info

if __name__ == '__main__':
    each_dcms = []
    each_temp = []
    for root, dirs, files in os.walk(dicom_path):
        for fname in files:
            if fname.endswith(".dcm") and not fname.startswith("."):
                each_dcms.append(os.path.join(root, fname))
    for i_name in each_dcms:
        i_ds = pydicom.dcmread(i_name, force=True)
        if 'SAG' not in i_ds.SeriesDescription.upper():
            continue
        i_info = saveImgAndInfo(i_name, i_ds)
        each_temp.append(i_info)
    if len(each_temp) > 0:
        each_df = pd.DataFrame(each_temp)
        info_csv = os.path.join(output_path, 'info.csv')
        each_df.to_csv(info_csv, header=True, index=False)
    else:
        sys.exit(1)
