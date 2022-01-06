FROM spark:3.2.0 AS build

COPY requirements.txt /requirements.txt
RUN pip3 install --disable-pip-version-check -r /requirements.txt

WORKDIR /opt/spark-notebooks

EXPOSE 8888

ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=jupyter
ENV PYSPARK_DRIVER_PYTHON_OPTS='notebook'

ENTRYPOINT jupyter notebook --allow-root --ip 0.0.0.0  --no-browser
