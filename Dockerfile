FROM python:3

WORKDIR /app

COPY requirements.txt ./

# RUN apk add git
RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD [ "python", "-u", "main.py" ]
