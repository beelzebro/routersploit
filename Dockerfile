FROM python:3.6
RUN apt-get update && \
    apt-get upgrade -y

COPY requirements.txt /tmp/requirements.txt
RUN pip install pip --upgrade
RUN pip install -r /tmp/requirements.txt

WORKDIR /routersploit
COPY . .

#CMD ["python3", "/routersploit/rsf.py"]
