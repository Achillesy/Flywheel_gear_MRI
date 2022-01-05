FROM tensorflow/tensorflow:2.4.1
ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get -qq update && \
    apt-get -qq -y upgrade && \
    apt-get -qq install -y --no-install-recommends \
    apt-utils python3-opencv && \
    pip install --upgrade pip && \
    pip install flywheel-sdk opencv-python pydicom pandas nibabel && \
    rm -rf /var/cache/apt/*

ENV FLYWHEEL=/flywheel/v0

RUN mkdir -p ${FLYWHEEL}
COPY run.py ${FLYWHEEL}/run.py

WORKDIR ${FLYWHEEL}
# ENTRYPOINT ["python run.py"]