FROM python:3-alpine3.11
WORKDIR /app
COPY . /app
RUN pip install -r req.txt
EXPOSE 5000
CMD python ./main.py