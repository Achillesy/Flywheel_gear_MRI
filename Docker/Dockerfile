## docker build -t ahsoka/tensorflow-rush:0.1.0 .
# FROM tensorflow/tensorflow:2.4.1
# ARG DEBIAN_FRONTEND=noninteractive
# ENV TZ=America/Chicago
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# RUN apt-get -qq update && \
#     apt-get -qq -y upgrade && \
#     apt-get -qq install -y --no-install-recommends \
#     apt-utils python3-opencv \
#     unzip jq tree && \
#     pip install --upgrade pip && \
#     pip install flywheel-sdk flywheel_gear_toolkit \
#     rtstatlib pathvalidate dataclasses \
#     opencv-python pandas pydicom pillow nibabel && \
#     rm -rf /var/cache/apt/*

## docker build -t ahsoka/tensorflow-rush:0.2.0 .
# FROM ahsoka/tensorflow-rush:0.1.0
# ENV FLYWHEEL=/flywheel/v0

# RUN mkdir -p ${FLYWHEEL}
# COPY h5 $FLYWHEEL/h5
# COPY pylib $FLYWHEEL/pylib

## docker build -t ahsoka/tensorflow-rush:0.3.0 .
FROM ahsoka/tensorflow-rush:0.2.0
ENV FLYWHEEL=/flywheel/v0

COPY analyze_infocsv.py ${FLYWHEEL}/analyze_infocsv.py
COPY dicom_img.py ${FLYWHEEL}/dicom_img.py
COPY fetal_brain_predict.py ${FLYWHEEL}/fetal_brain_predict.py
COPY manifest.json ${FLYWHEEL}/manifest.json
COPY ohifimport.py ${FLYWHEEL}/ohifimport.py
COPY pyconfiguration.json ${FLYWHEEL}/pyconfiguration.json
COPY run ${FLYWHEEL}/run
RUN  chmod +x ${FLYWHEEL}/run
COPY unzip_dicom.py ${FLYWHEEL}/unzip_dicom.py

# WORKDIR ${FLYWHEEL}
# ENTRYPOINT ["sh", "-c", "ls -al $FLYWHEEL"]