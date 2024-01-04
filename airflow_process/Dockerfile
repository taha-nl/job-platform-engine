FROM apache/airflow:latest-python3.8

ARG CURRENT_USER=$USER

ARG CHROME_VERSION=119.0.6045.105-1
ARG CHROME_DRIVER_VERSION=119.0.6045.105

USER root
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y wget && \
    apt-get install -y unzip 


RUN mkdir -p /usr/local/tmp \
	&& cd /usr/local/tmp \
	&& wget http://dl.google.com/linux/deb/pool/main/g/google-chrome-stable/google-chrome-stable_"$CHROME_VERSION"_amd64.deb \
    && apt-get install -y ./google-chrome-stable_"$CHROME_VERSION"_amd64.deb \
 	&& wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/"$CHROME_DRIVER_VERSION"/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver
USER airflow
COPY requirements.txt /usr/local/tmp/

RUN pip install -r /usr/local/tmp/requirements.txt 



# FROM apache/airflow:latest-python3.8
# FROM apache/airflow:latest-python3.9
# FROM apache/airflow:2.7.3

# # WORKDIR /usr/local/airflow

# # COPY selenium-installation.sh .




# ARG CURRENT_USER=$USER

# USER root

# RUN apt-get -y update && \
#     apt-get -y upgrade && \
#     apt-get -y install curl && \
#     apt-get -y install unzip

# RUN chmod +x selenium-installation.sh

# RUN ./selenium-installation.sh



# USER airflow
# COPY requirements.txt /
# RUN pip install -r /requirements.txt
# USER ${CURRENT_USER}

# FROM apache/airflow:2.7.3