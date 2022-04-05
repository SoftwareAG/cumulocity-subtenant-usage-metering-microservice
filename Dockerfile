FROM python:alpine3.8
COPY ./ /app
WORKDIR /app
RUN pip install requests
RUN pip install jsonify
RUN pip install flask
ENTRYPOINT ["python3"]
CMD ["run.py"]
