FROM apache/airflow:2.2.3-python3.9

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
 	  build-essential tzdata \
 	  apt-transport-https \
	  ca-certificates \
	  curl \
	  gnupg \
	  lsb-release\
	  python3-dev \
	  libpq-dev \
  && apt-get clean  \
  && apt-get autoremove -yqq --purge \
  && rm -rf /var/lib/apt/lists/*


ENV TZ=Asia/Tehran

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt /requirements.txt

USER airflow

ENV PIP_USER=true

RUN pip3 install -U pip wheel setuptools \
	&& pip3 install -U --disable-pip-version-check -r /requirements.txt


#RUN python3 -m venv /codes/daily_emotion/.venv

#RUN . /codes/daily_emotion/.venv/bin/activate \
#	&& pip install -U pip wheel setuptools \
#	&& pip install -r /codes/daily_emotion/requirements.txt

# RUN /usr/local/bin/python -m pip install --upgrade pip   \
#  && pip install --disable-pip-version-check --no-cache-dir \
#	 jdatetime
		  
#RUN pip install /codes/daily_emotion/  --use-feature=in-tree-build 

