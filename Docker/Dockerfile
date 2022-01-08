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
#     pip install flywheel-sdk opencv-python \
#     pandas pydicom nibabel && \
#     rm -rf /var/cache/apt/*

## docker build -t ahsoka/tensorflow-rush:0.2.0 .
FROM ahsoka/tensorflow-rush:0.1.0
ENV FLYWHEEL=/flywheel/v0

RUN mkdir -p ${FLYWHEEL}
# COPY run.py ${FLYWHEEL}/run.py

# Configure entrypoint
# WORKDIR ${FLYWHEEL}
# ENTRYPOINT ["python run.py"]
ENTRYPOINT ["sh", "-c", "ls -al $FLYWHEEL"]