FROM python:3.10.12-slim-bookworm
LABEL maintainer="tn781927@yahoo.com.tw"

WORKDIR /home/shungco

# update enviroment dependicies
RUN apt-get update -y && \
    apt-get upgrade -y && \
    useradd -m shungco

COPY . /home/shungco

RUN pip install -r /home/shungco/requirements.txt && \
    chown -R shungco:shungco /home/shungco

CMD ["python", "backend/app.py", "--reload"]

