#!/usr/bin/env python
# tf 2.4.1
# Instructions:
# Annotate the clearst fetalbrain from a /tmp/DIMG/*.jpg
# Call by ahsoka/tensorflow-rush:0.3.0
#
# \author     Xuchu Liu (xuchu_liu@rush.edu)
# \date       1/11/2021

import os
import sys
import json
import flywheel

import numpy as np
import pandas as pd

import tensorflow as tf
from pylib import build_unet, gravitycenter

image_path  = "/tmp/DIMG"
flywheel_path  = "/flywheel/v0"
output_path = "/flywheel/v0/output"

img_size = 512

if __name__ == '__main__':
    context = flywheel.GearContext()
    config  = context.config
    measure = config['Measurement']

    info_csv = os.path.join(output_path, 'info.csv')
    df_instance = pd.read_csv(info_csv)

    input_shape = (img_size, img_size, 3)
    model_pred = build_unet(input_shape)

    jf = open(os.path.join(flywheel_path, "pyconfiguration.json"))
    jsondata = json.load(jf)
    jf.close()

    if measure.find("All") == 0 or measure.find("Pons") > 0:
        pons_model_1 = build_unet(input_shape)
        pons_model_1.load_weights(os.path.join(flywheel_path, "h5", jsondata['hdf5Pons'][0]))
        pons_model_2 = build_unet(input_shape)
        pons_model_2.load_weights(os.path.join(flywheel_path, "h5", jsondata['hdf5Pons'][1]))

    if measure.find("All") == 0 or measure.find("Vermis") > 0:
        vermis_model_1 = build_unet(input_shape)
        vermis_model_1.load_weights(os.path.join(flywheel_path, "h5", jsondata['hdf5Vermis'][0]))
        vermis_model_2 = build_unet(input_shape)
        vermis_model_2.load_weights(os.path.join(flywheel_path, "h5", jsondata['hdf5Vermis'][1]))
        hvermis_model_1 = build_unet(input_shape)
        hvermis_model_1.load_weights(os.path.join(flywheel_path, "h5", jsondata['hdf5Vermis'][2]))
        hvermis_model_2 = build_unet(input_shape)
        hvermis_model_2.load_weights(os.path.join(flywheel_path, "h5", jsondata['hdf5Vermis'][3]))

    if measure.find("All") == 0 or measure.find("Fronto") == 0:
        fronto_model_1 = build_unet(input_shape)
        fronto_model_1.load_weights(os.path.join(flywheel_path, "h5", jsondata['hdf5Fronto'][0]))
        fronto_model_2 = build_unet(input_shape)
        fronto_model_2.load_weights(os.path.join(flywheel_path, "h5", jsondata['hdf5Fronto'][1]))

    for idx, data in df_instance.iterrows():
        i_name = os.path.join(image_path, data.Id+".jpg")
        img_raw = tf.io.read_file(i_name)
        img = tf.image.decode_jpeg(img_raw, 3)
        img = tf.image.resize(img, [img_size, img_size])
        t_img = img / 255.0
        t_imgs = np.expand_dims(t_img, axis=0)

        if measure.find("All") == 0 or measure.find("Pons") > 0:
            ## Pons model 1
            pred = pons_model_1.predict(t_imgs)
            pred = tf.squeeze(pred)
            Pons1_max = np.max(pred)
            pred_axis_Y, pred_axis_X = np.where(pred == Pons1_max)
            df_instance.loc[idx, "Pons_1x"] = int(pred_axis_X)
            df_instance.loc[idx, "Pons_1y"] = int(pred_axis_Y)
            ## Pons model 2
            pred = pons_model_2.predict(t_imgs)
            pred = tf.squeeze(pred)
            Pons2_max = np.max(pred)
            pred_axis_Y, pred_axis_X = np.where(pred == Pons2_max)
            df_instance.loc[idx, "Pons_2x"] = int(pred_axis_X)
            df_instance.loc[idx, "Pons_2y"] = int(pred_axis_Y)
            df_instance.loc[idx, "deltaPons"] = Pons1_max + Pons2_max

        if measure.find("All") == 0 or measure.find("Vermis") > 0:
            ## Vermis model 1
            pred = vermis_model_1.predict(t_imgs)
            pred = tf.squeeze(pred)
            Vermis1_max = np.max(pred)
            pred_axis_Y, pred_axis_X = np.where(pred == Vermis1_max)
            df_instance.loc[idx, "Vermis_1x"] = int(pred_axis_X)
            df_instance.loc[idx, "Vermis_1y"] = int(pred_axis_Y)
            ## Vermis model 2
            pred = vermis_model_2.predict(t_imgs)
            pred = tf.squeeze(pred)
            Vermis2_max = np.max(pred)
            pred_axis_Y, pred_axis_X = np.where(pred == Vermis2_max)
            df_instance.loc[idx, "Vermis_2x"] = int(pred_axis_X)
            df_instance.loc[idx, "Vermis_2y"] = int(pred_axis_Y)
            ## HVermis model 1
            pred = hvermis_model_1.predict(t_imgs)
            pred = tf.squeeze(pred)
            HVermis1_max = np.max(pred)
            pred_axis_Y, pred_axis_X = np.where(pred == HVermis1_max)
            df_instance.loc[idx, "HVermis_1x"] = int(pred_axis_X)
            df_instance.loc[idx, "HVermis_1y"] = int(pred_axis_Y)
            ## HVermis model 2
            pred = hvermis_model_2.predict(t_imgs)
            pred = tf.squeeze(pred)
            HVermis2_max = np.max(pred)
            pred_axis_Y, pred_axis_X = np.where(pred == HVermis2_max)
            df_instance.loc[idx, "HVermis_2x"] = int(pred_axis_X)
            df_instance.loc[idx, "HVermis_2y"] = int(pred_axis_Y)
            df_instance.loc[idx, "deltaVermis"] = Vermis1_max + Vermis2_max + HVermis1_max + HVermis2_max

        if measure.find("All") == 0 or measure.find("Fronto") == 0:
            ## Fronto model 1
            pred = fronto_model_1.predict(t_imgs)
            pred = tf.squeeze(pred)
            Fronto1_max = np.max(pred)
            pred_axis_Y, pred_axis_X = np.where(pred == Fronto1_max)
            df_instance.loc[idx, "Fronto_1x"] = int(pred_axis_X)
            df_instance.loc[idx, "Fronto_1y"] = int(pred_axis_Y)
            ## Fronto model 2
            pred = fronto_model_2.predict(t_imgs)
            pred = tf.squeeze(pred)
            Fronto2_max = np.max(pred)
            pred_axis_Y, pred_axis_X = np.where(pred == Fronto2_max)
            df_instance.loc[idx, "Fronto_2x"] = int(pred_axis_X)
            df_instance.loc[idx, "Fronto_2y"] = int(pred_axis_Y)
            df_instance.loc[idx, "deltaFronto"] = Fronto1_max + Fronto2_max

df_instance = df_instance.sort_values(by="Id")
df_instance.to_csv(info_csv, header=True, index=False)
