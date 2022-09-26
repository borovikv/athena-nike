FROM public.ecr.aws/amazonlinux/amazonlinux
LABEL maintainer="amazon"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create directory for the app user
RUN mkdir -p /home/app
ENV HOME=/home/app
ENV APP_HOME=$HOME/workdir
ENV PYTHONPATH=$APP_HOME/plugins/
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN yum update -y
RUN yum install -y python37 gcc gcc-g++ python3-devel
RUN yum install -y java-1.8.0-openjdk unixODBC-devel
RUN yum install -y zip unzip bzip2 gzip
RUN yum install -y gcc-c++ cyrus-sasl-devel libcurl-devel openssl-devel shadow-utils
RUN yum clean all

RUN python3 -m pip install --upgrade pip

# Install wheel to avoid legacy setup.py install
RUN pip3 install wheel

# On RHL and Centos based linux, openssl needs to be set as Python Curl SSL library
ENV PYCURL_SSL_LIBRARY=openssl
RUN pip3 install --upgrade pip
RUN pip3 install --compile pycurl
RUN pip3 install celery[sqs]

# setuptools dropped support for use_2to3 in v58+ and psycopg2 will install the latest v59+ version
RUN pip3 install "setuptools<=57.*"

COPY requirements.txt $HOME/requirements.txt
RUN pip3 install -r $HOME/requirements.txt

RUN yum install -y make
ENV TRINO_URL="trino://user@trino:8080/memory"
