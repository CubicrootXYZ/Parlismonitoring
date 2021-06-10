FROM golang:1.14.0-stretch

RUN apt update && apt upgrade -y && \
    apt install -y git \
    make openssh-client

RUN git clone https://github.com/CubicrootXYZ/Parlismonitoring.git /tmp/app
RUN cd /tmp/app/api && go get -d ./...
RUN go build -o /opt/app /tmp/app/api/cmd/parlismonitoring-api/*.go
RUN rm -R /tmp/app

WORKDIR /opt

ENTRYPOINT ["/bin/bash", "-l", "-c"]
CMD ["/opt/app"]