FROM python:3.7-stretch

ENV FLASK_APP flasky.py

RUN apt-get update && apt-get install -y pandoc
RUN useradd -ms /bin/bash flasky
RUN adduser flasky sudo

USER flasky

WORKDIR /home/flasky

COPY requirements.txt ./
RUN python -m venv venv && venv/bin/pip install -r requirements.txt

COPY app app
COPY flasky.py boot.sh ./

# runtime configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
