FROM frolvlad/alpine-python2

COPY requirements.txt .
RUN pip install -rrequirements.txt

COPY get_metadata.py .

CMD ["./get_metadata.py"]

