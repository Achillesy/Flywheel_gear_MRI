#!/usr/bin/env python
# tf 2.4.1
# Instructions:
# Annotate the clearst fetalbrain from a /tmp/DIMG/*.jpg
# Call by ahsoka/tensorflow-rush:0.3.0
#
# \author     Xuchu Liu (xuchu_liu@rush.edu)
# \date       1/11/2021

import os
import flywheel

import numpy as np
import pandas as pd

import cv2
import json

import flywheel_gear_toolkit as gt

image_path = "/tmp/DIMG"
flywheel_path = "/flywheel/v0"
output_path = "/flywheel/v0/output"

img_size = 512

def checkPons(sizePons, weeks):
    b_Pons = False
    normalPonsText = "Unknown"
    if weeks == 22:
        normalPonsText = "7 ~ 9 mm"
        if sizePons > 7 and sizePons < 9:
            b_Pons = True
    if weeks == 23 or weeks == 24:
        normalPonsText = "8 ~ 10 mm"
        if sizePons > 8 and sizePons < 10:
            b_Pons = True
    if weeks == 25 or weeks == 26:
        normalPonsText = "10 ~ 12 mm"
        if sizePons > 10 and sizePons < 12:
            b_Pons = True
    if weeks == 27 or weeks == 28:
        normalPonsText = "11 ~ 13 mm"
        if sizePons > 11 and sizePons < 13:
            b_Pons = True
    if weeks == 29 or weeks == 30:
        normalPonsText = "11 ~ 13 mm"
        if sizePons > 11 and sizePons < 13:
            b_Pons = True
    if weeks == 31 or weeks == 32:
        normalPonsText = "13 ~ 15 mm"
        if sizePons > 13 and sizePons < 15:
            b_Pons = True
    if weeks == 33 or weeks == 34:
        normalPonsText = "15 ~ 17 mm"
        if sizePons > 15 and sizePons < 17:
            b_Pons = True
    if weeks == 35 or weeks == 36:
        normalPonsText = "16 ~ 18 mm"
        if sizePons > 16 and sizePons < 18:
            b_Pons = True
    if weeks == 37 or weeks == 38:
        normalPonsText = "18 ~ 20 mm"
        if sizePons > 18 and sizePons < 20:
            b_Pons = True
    return b_Pons, normalPonsText

def checkVermis(sizeVermis, weeks):
    b_Vermis = False
    normalVermisText = "Unknown"
    if weeks == 22 or weeks == 23:
        normalVermisText = "8 ~ 9 mm"
        if sizeVermis > 8 and sizeVermis < 9:
            b_Vermis = True
    if weeks == 24 or weeks == 25:
        normalVermisText = "6 ~ 10 mm"
        if sizeVermis > 6 and sizeVermis < 10:
            b_Vermis = True
    if weeks == 26:
        normalVermisText = "9 ~ 10 mm"
        if sizeVermis > 9 and sizeVermis < 10:
            b_Vermis = True
    if weeks == 27:
        normalVermisText = "7 ~ 13 mm"
        if sizeVermis > 7 and sizeVermis < 13:
            b_Vermis = True
    if weeks == 28:
        normalVermisText = "8 ~ 11 mm"
        if sizeVermis > 8 and sizeVermis < 11:
            b_Vermis = True
    if weeks == 29:
        normalVermisText = "8 ~ 13 mm"
        if sizeVermis > 8 and sizeVermis < 13:
            b_Vermis = True
    if weeks == 30:
        normalVermisText = "9 ~ 15 mm"
        if sizeVermis > 9 and sizeVermis < 15:
            b_Vermis = True
    if weeks == 31:
        normalVermisText = "10 ~ 16 mm"
        if sizeVermis > 10 and sizeVermis < 16:
            b_Vermis = True
    if weeks == 32:
        normalVermisText = "8 ~ 17 mm"
        if sizeVermis > 8 and sizeVermis < 17:
            b_Vermis = True
    if weeks == 33:
        normalVermisText = "10 ~ 20 mm"
        if sizeVermis > 10 and sizeVermis < 20:
            b_Vermis = True
    if weeks == 34:
        normalVermisText = "11 ~ 20 mm"
        if sizeVermis > 11 and sizeVermis < 20:
            b_Vermis = True
    if weeks == 35 or weeks == 36:
        normalVermisText = "10 ~ 18 mm"
        if sizeVermis > 10 and sizeVermis < 18:
            b_Vermis = True
    if weeks == 37 or weeks == 38:
        normalVermisText = "10 ~ 20 mm"
        if sizeVermis > 10 and sizeVermis < 20:
            b_Vermis = True
    return b_Vermis, normalVermisText

def checkHVermis(sizeHVermis, weeks):
    b_HVermis = False
    normalHVermisText = "Unknown"
    if weeks == 22 or weeks == 23:
        normalHVermisText = "10 ~ 12 mm"
        if sizeHVermis > 10 and sizeHVermis < 12:
            b_HVermis = True
    if weeks == 24 or weeks == 25:
        normalHVermisText = "10 ~ 15 mm"
        if sizeHVermis > 10 and sizeHVermis < 15:
            b_HVermis = True
    if weeks == 26:
        normalHVermisText = "13 ~ 15 mm"
        if sizeHVermis > 13 and sizeHVermis < 15:
            b_HVermis = True
    if weeks == 27:
        normalHVermisText = "12 ~ 18 mm"
        if sizeHVermis > 12 and sizeHVermis < 18:
            b_HVermis = True
    if weeks == 28:
        normalHVermisText = "13 ~ 18 mm"
        if sizeHVermis > 13 and sizeHVermis < 18:
            b_HVermis = True
    if weeks == 29:
        normalHVermisText = "14 ~ 18 mm"
        if sizeHVermis > 14 and sizeHVermis < 18:
            b_HVermis = True
    if weeks == 30:
        normalHVermisText = "13 ~ 20 mm"
        if sizeHVermis > 13 and sizeHVermis < 20:
            b_HVermis = True
    if weeks == 31:
        normalHVermisText = "15 ~ 20 mm"
        if sizeHVermis > 15 and sizeHVermis < 20:
            b_HVermis = True
    if weeks == 32:
        normalHVermisText = "15 ~ 22 mm"
        if sizeHVermis > 15 and sizeHVermis < 22:
            b_HVermis = True
    if weeks == 33:
        normalHVermisText = "15 ~ 22 mm"
        if sizeHVermis > 15 and sizeHVermis < 22:
            b_HVermis = True
    if weeks == 34:
        normalHVermisText = "16 ~ 26 mm"
        if sizeHVermis > 11 and sizeHVermis < 20:
            b_HVermis = True
    if weeks == 35 or weeks == 36:
        normalHVermisText = "18 ~ 25 mm"
        if sizeHVermis > 18 and sizeHVermis < 25:
            b_HVermis = True
    if weeks == 37 or weeks == 38:
        normalHVermisText = "16 ~ 29 mm"
        if sizeHVermis > 16 and sizeHVermis < 29:
            b_HVermis = True
    return b_HVermis, normalHVermisText

def checkFronto(sizeFronto, weeks):
    b_Fronto = False
    normalFrontoText = "Unknown"
    if weeks == 22 or weeks == 23:
        normalFrontoText = "60 ~ 73 mm"
        if sizeFronto > 60 and sizeFronto < 73:
            b_Fronto = True
    if weeks == 24 or weeks == 25:
        normalFrontoText = "60 ~ 81 mm"
        if sizeFronto > 60 and sizeFronto < 81:
            b_Fronto = True
    if weeks == 26:
        normalFrontoText = "71 ~ 90 mm"
        if sizeFronto > 71 and sizeFronto < 90:
            b_Fronto = True
    if weeks == 27:
        normalFrontoText = "73 ~ 90 mm"
        if sizeFronto > 73 and sizeFronto < 90:
            b_Fronto = True
    if weeks == 28:
        normalFrontoText = "70 ~ 90 mm"
        if sizeFronto > 70 and sizeFronto < 90:
            b_Fronto = True
    if weeks == 29:
        normalFrontoText = "75 ~ 95 mm"
        if sizeFronto > 75 and sizeFronto < 95:
            b_Fronto = True
    if weeks == 30:
        normalFrontoText = "77 ~ 108 mm"
        if sizeFronto > 77 and sizeFronto < 108:
            b_Fronto = True
    if weeks == 31:
        normalFrontoText = "82 ~ 97 mm"
        if sizeFronto > 82 and sizeFronto < 97:
            b_Fronto = True
    if weeks == 32:
        normalFrontoText = "82 ~ 106 mm"
        if sizeFronto > 82 and sizeFronto < 106:
            b_Fronto = True
    if weeks == 33:
        normalFrontoText = "90 ~ 105 mm"
        if sizeFronto > 90 and sizeFronto < 105:
            b_Fronto = True
    if weeks == 34:
        normalFrontoText = "90 ~ 114 mm"
        if sizeFronto > 90 and sizeFronto < 114:
            b_Fronto = True
    if weeks == 35 or weeks == 36:
        normalFrontoText = "97 ~ 113 mm"
        if sizeFronto > 97 and sizeFronto < 113:
            b_Fronto = True
    if weeks == 37 or weeks == 38:
        normalFrontoText = "90 ~ 112 mm"
        if sizeFronto > 90 and sizeFronto < 112:
            b_Fronto = True
    return b_Fronto, normalFrontoText

if __name__ == "__main__":
    context = flywheel.GearContext()
    config = context.config
    measure = config["Measurement"]
    weeks = config["GE"]

    info_csv = os.path.join(output_path, "info.csv")
    df_instance = pd.read_csv(info_csv)

    normalColor = (250, 250, 250)
    abnormalColor = (60, 60, 250)
    reportList = []
    jsonOHIF = {
        "ohifViewer": {
            "measurements": {
                "Length": []
            }
        }
    }

    data = df_instance.iloc[0]
    txtLine = "PatientName: %s\n" % (data["PatientName"])
    reportList.append(txtLine)
    txtLine = "  Gestation: %d weeks\n\n" % (weeks)
    reportList.append(txtLine)
    txtLine = "      Height: %d pixels\n" % (data["Rows"])
    reportList.append(txtLine)
    txtLine = "       Width: %d pixels\n" % (data["Columns"])
    reportList.append(txtLine)
    txtLine = "PixelSpacing: [%f, %f]\n\n" % (data["PixelSpacing1"], data["PixelSpacing2"])
    reportList.append(txtLine)

    if measure.find("All") == 0 or measure.find("Pons") > 0:
        df_instance = df_instance.sort_values(by="deltaPons", ascending=False)
        data = df_instance.iloc[0]
        Pons_img = data.Id + ".jpg"
        Pons_dcm = data.Id + ".dcm"
        Pons_conf = round(data.deltaPons * 50, 1)
        Pons_1x = int(data.Pons_1x * data.Columns / img_size)
        Pons_1y = int(data.Pons_1y * data.Rows / img_size)
        Pons_2x = int(data.Pons_2x * data.Columns / img_size)
        Pons_2y = int(data.Pons_2y * data.Rows / img_size)
        dist_mm = np.sqrt(np.square(Pons_1y - Pons_2y) + np.square(Pons_1x - Pons_2x))
        mmPons = round(dist_mm * data.PixelSpacing1, 2)
        b_Pons, normalPonsText = checkPons(mmPons, weeks)

        if b_Pons:
            resultPonsText = "normal"
            resultPonsColor = normalColor
        else:
            resultPonsText = "abnormal"
            resultPonsColor = abnormalColor

        resultPonsLine = "A-P Diameter of Pons: %.2fmm %s" % (mmPons, resultPonsText)
        reportList.append(resultPonsLine)
        txtLine      = "\n        normal range: (%s)\n" % (normalPonsText)
        reportList.append(txtLine)
        txtLine      = "            coordinate: [%3d %3d] [%3d %3d]\n" % (Pons_1x, Pons_1y, Pons_2x, Pons_2y)
        reportList.append(txtLine)
        txtLine = "%s - confidence:%.1f%%\n" % (Pons_dcm, Pons_conf)
        reportList.append(txtLine)
        txtLine = "SeriesNumber: %s \t" % (data["SeriesNumber"])
        reportList.append(txtLine)
        txtLine = "InstanceNumber: %s\n\n" % (data["InstanceNumber"])
        reportList.append(txtLine)
    
        # Pons_dcm_name = os.path.join(output_path, Pons_dcm)
        # if not os.path.exists(Pons_dcm_name):
        #     os.system('cp ' + data.DicomPath + ' ' + Pons_dcm_name)
        Pons_name = os.path.join(output_path, Pons_img)
        if not os.path.exists(Pons_name):
            os.system('cp /tmp/DIMG/' + Pons_img + ' ' + Pons_name)
        img = cv2.imread(Pons_name)
        cv2.line(img, (Pons_1x,Pons_1y), (Pons_2x,Pons_2y), color=resultPonsColor, thickness = 2)
        cv2.putText(img, resultPonsLine, (10,25), cv2.FONT_HERSHEY_COMPLEX, 0.6, resultPonsColor, 1)
        cv2.imwrite(Pons_name, img)

    if measure.find("All") == 0 or measure.find("Vermis") > 0:
        df_instance = df_instance.sort_values(by="deltaVermis", ascending=False)
        data = df_instance.iloc[0]
        Vermis_img = data.Id + ".jpg"
        Vermis_dcm = data.Id + ".dcm"
        Vermis_conf = round(data.deltaVermis * 25, 1)
        Vermis_1x = int(data.Vermis_1x * data.Columns / img_size)
        Vermis_1y = int(data.Vermis_1y * data.Rows / img_size)
        Vermis_2x = int(data.Vermis_2x * data.Columns / img_size)
        Vermis_2y = int(data.Vermis_2y * data.Rows / img_size)
        dist_mm = np.sqrt(
            np.square(Vermis_1y - Vermis_2y) + np.square(Vermis_1x - Vermis_2x)
        )
        mmVermis = round(dist_mm * data.PixelSpacing1, 2)
        b_Vermis, normalVermisText = checkVermis(mmVermis, weeks)

        if b_Vermis:
            resultVermisText = "normal"
            resultVermisColor = normalColor
        else:
            resultVermisText = "abnormal"
            resultVermisColor = abnormalColor
        resultVermisLine = "A-P Diameter of Vermis: %.2fmm %s" % (mmVermis, resultVermisText)
        reportList.append(resultVermisLine)
        txtLine        = "\n          normal range: (%s)\n" % (normalVermisText)
        reportList.append(txtLine)
        txtLine        = "            coordinate: [%3d %3d] \t [%3d %3d]\n" % (Vermis_1x, Vermis_1y, Vermis_2x, Vermis_2y)
        reportList.append(txtLine)

        HVermis_1x = int(data.HVermis_1x * data.Columns / img_size)
        HVermis_1y = int(data.HVermis_1y * data.Rows / img_size)
        HVermis_2x = int(data.HVermis_2x * data.Columns / img_size)
        HVermis_2y = int(data.HVermis_2y * data.Rows / img_size)
        dist_mm = np.sqrt(
            np.square(HVermis_1y - HVermis_2y) + np.square(HVermis_1x - HVermis_2x)
        )
        mmHVermis = round(dist_mm * data.PixelSpacing1, 2)
        b_HVermis, normalHVermisText = checkHVermis(mmHVermis, weeks)

        if b_HVermis:
            resultHVermisText = "normal"
            resultHVermisColor = normalColor
        else:
            resultHVermisText = "abnormal"
            resultHVermisColor = abnormalColor
        resultHVermisLine = "Height of Vermis: %.2fmm %s" % (mmHVermis, resultHVermisText)
        reportList.append(resultHVermisLine)
        txtLine         = "\n    normal range: (%s)\n" % (normalHVermisText)
        reportList.append(txtLine)
        txtLine         = "        coordinate: [%3d %3d] [%3d %3d]\n" % (HVermis_1x, HVermis_1y, HVermis_2x, HVermis_2y)
        reportList.append(txtLine)
        txtLine = "%s - confidence:%.1f%%\n" % (Vermis_dcm, Vermis_conf)
        reportList.append(txtLine)
        txtLine = "SeriesNumber: %s \t" % (data["SeriesNumber"])
        reportList.append(txtLine)
        txtLine = "InstanceNumber: %s\n\n" % (data["InstanceNumber"])
        reportList.append(txtLine)
    
        # Vermis_dcm_name = os.path.join(output_path, Vermis_dcm)
        # if not os.path.exists(Vermis_dcm_name):
        #     os.system('cp ' + data.DicomPath + ' ' + Vermis_dcm_name)
        Vermis_name = os.path.join(output_path, Vermis_img)
        if not os.path.exists(Vermis_name):
            os.system('cp /tmp/DIMG/' + Vermis_img + ' ' + Vermis_name)
        img = cv2.imread(Vermis_name)
        cv2.line(img, (Vermis_1x,Vermis_1y), (Vermis_2x,Vermis_2y), color=resultVermisColor, thickness = 2)
        cv2.putText(img, resultVermisLine, (10,50), cv2.FONT_HERSHEY_COMPLEX, 0.6, resultVermisColor, 1)
        cv2.line(img, (HVermis_1x,HVermis_1y), (HVermis_2x,HVermis_2y), color=resultHVermisColor, thickness = 2)
        cv2.putText(img, resultHVermisLine, (10,75), cv2.FONT_HERSHEY_COMPLEX, 0.6, resultHVermisColor, 1)
        cv2.imwrite(Vermis_name, img)

    if measure.find("All") == 0 or measure.find("Fronto") == 0:
        df_instance = df_instance.sort_values(by="deltaFronto", ascending=False)
        data = df_instance.iloc[0]
        Fronto_img = data.Id + ".jpg"
        Fronto_dcm = data.Id + ".dcm"
        Fronto_conf = round(data.deltaFronto * 50, 1)
        Fronto_1x = int(data.Fronto_1x * data.Columns / img_size)
        Fronto_1y = int(data.Fronto_1y * data.Rows / img_size)
        Fronto_2x = int(data.Fronto_2x * data.Columns / img_size)
        Fronto_2y = int(data.Fronto_2y * data.Rows / img_size)
        dist_mm = np.sqrt(
            np.square(Fronto_1y - Fronto_2y) + np.square(Fronto_1x - Fronto_2x)
        )
        mmFronto = round(dist_mm * data.PixelSpacing1, 2)
        b_Fronto, normalFrontoText = checkFronto(mmFronto, weeks)
        if b_Fronto:
            resultFrontoText = "normal"
            resultFrontoColor = normalColor
        else:
            resultFrontoText = "abnormal"
            resultFrontoColor = abnormalColor

        resultFrontoLine = "Fronto-Occpitial: %.2fmm %s" % (mmFronto, resultFrontoText)
        reportList.append(resultFrontoLine)
        txtLine        = "\n    normal range: (%s)\n" % (normalFrontoText)
        reportList.append(txtLine)
        txtLine        = "        coordinate: [%3d %3d] [%3d %3d]\n" % (Fronto_1x, Fronto_1y, Fronto_2x, Fronto_2y)
        reportList.append(txtLine)
        txtLine = "%s - confidence:%.1f%%\n" % (Fronto_img, Fronto_conf)
        reportList.append(txtLine)
        txtLine = "SeriesNumber: %s \t" % (data["SeriesNumber"])
        reportList.append(txtLine)
        txtLine = "InstanceNumber: %s\n\n" % (data["InstanceNumber"])
        reportList.append(txtLine)
    
        # Fronto_dcm_name = os.path.join(output_path, Fronto_dcm)
        # if not os.path.exists(Fronto_dcm_name):
        #     os.system('cp ' + data.DicomPath + ' ' + Fronto_dcm_name)
        Fronto_name = os.path.join(output_path, Fronto_img)
        if not os.path.exists(Fronto_name):
            os.system('cp /tmp/DIMG/' + Fronto_img + ' ' + Fronto_name)
        img = cv2.imread(Fronto_name)
        cv2.line(img, (Fronto_1x,Fronto_1y), (Fronto_2x,Fronto_2y), color=resultFrontoColor, thickness = 2)
        cv2.putText(img, resultFrontoLine, (10,100), cv2.FONT_HERSHEY_COMPLEX, 0.6, resultFrontoColor, 1)
        cv2.imwrite(Fronto_name, img)

    for line in reportList:
        print(line)
    if measure.find("All") == 0:
        reportName = os.path.join(output_path, "AI_all_report.txt")
    if measure.find("Pons") > 0:
        reportName = os.path.join(output_path, "AI_pons_report.txt")
    if measure.find("Vermis") > 0:
        reportName = os.path.join(output_path, "AI_vermis_report.txt")
    if measure.find("Fronto") == 0:
        reportName = os.path.join(output_path, "AI_fronto_report.txt")
    f = open(reportName, "w")
    f.writelines(reportList)
    f.close()

    with gt.GearToolkitContext() as context:
        context.update_container_metadata('session', {'info': jsonOHIF})
