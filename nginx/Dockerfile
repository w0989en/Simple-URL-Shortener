FROM nginx:latest
LABEL description="Simple URL Shortener"


COPY nginx.conf /etc/nginx/nginx.conf
COPY docker-nginx-b2e.conf /etc/nginx/sites-available/

RUN mkdir -p /etc/nginx/sites-enabled/ && \
    ln -s /etc/nginx/sites-available/docker-nginx-b2e.conf /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]