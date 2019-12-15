FROM python:3.6

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

# Bundle app source
COPY . /usr/src/app/

EXPOSE 8080
CMD [ "flask", "run" ]
