FROM alpine:3.7
COPY . /app
RUN make /app
CMD python /app/app.py

### gets Java
RUN apk update \
&& apk upgrade \
&& apk add --no-cache bash \
&& apk add --no-cache --virtual=build-dependencies unzip \
&& apk add --no-cache curl \
&& apk add --no-cache openjdk8-jre

### gets Python and pip
RUN apk add --no-cache python3 \
&& python3 -m ensurepip \
&& pip3 install --upgrade pip setuptools \
&& rm -r /usr/lib/python*/ensurepip && \
if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
rm -r /root/.cache

### flask
RUN pip install --trusted-host pypi.python.org flask

### environment variables
ENV JAVA_HOME = "/usr/lib/jvm/java-1.8-openjdk"

### testing purposes
EXPOSE 81
ADD test.py /
CMD ["python", "test.py"]

# https://stackoverflow.com/questions/51121875/how-to-run-docker-with-python-and-java
