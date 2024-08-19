FROM python:3-slim
WORKDIR /app
COPY . /app
RUN pip install -r req.txt
EXPOSE 3000
CMD ["python", "./main.py"]