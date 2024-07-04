FROM python:3.9-slim
WORKDIR /usr/src/app
COPY --chwon=1000:root . ./
RUN pip3 install -r requirements.txt
USER 1000
CMD [ "python", "main.py" ]