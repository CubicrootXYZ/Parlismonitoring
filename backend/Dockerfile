FROM debian:latest
RUN apt update && apt install -y python3 python3-pip git unzip wget
RUN apt upgrade -y
RUN pip3 install --upgrade pip
RUN pip3 install pony pymysql pdfplumber requests beautifulsoup4 torch
RUN mkdir /opt/app
RUN wget "https://www.cis.uni-muenchen.de/~schmid/tools/RNNTagger/data/RNNTagger-1.2.zip" -P /opt/app
RUN mkdir /opt/app/RNNTagger
RUN unzip /opt/app/RNNTagger-1.2.zip -d /opt/app
RUN git clone https://github.com/CubicrootXYZ/Parlismonitoring.git /tmp/app
RUN mv /tmp/app/backend/* /opt/app/RNNTagger/
RUN rm -R /tmp/app
RUN rm /opt/app/RNNTagger-1.2.zip

WORKDIR /opt/app/RNNTagger
CMD [ "python3", "-u", "/opt/app/RNNTagger/backend.py"]