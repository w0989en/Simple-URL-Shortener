FROM python:3.7
LABEL description="Simple URL Shortener"


WORKDIR /web
COPY . /web/

RUN pip install -r requirements.txt


WORKDIR /web/B2E

VOLUME /web
EXPOSE 8000

# ENTRYPOINT [ "/bin/bash", "/web/docker-entrypoint.sh" ]
CMD python manage.py runserver 0.0.0.0:8000
