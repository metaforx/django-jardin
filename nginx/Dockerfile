FROM nginx:1.25.2

RUN apt-get update && apt-get install -y --no-install-recommends dumb-init

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy our config
COPY ./nginx.conf /etc/nginx/nginx.conf

# Create nginx user with same UID as the app user in the web service
RUN adduser --system --uid 1000 --no-create-home --disabled-login --group nginxuser

# Create required directories
RUN mkdir -p /tmp/client_temp \
    /tmp/proxy_temp_path \
    /tmp/fastcgi_temp \
    /tmp/uwsgi_temp \
    /tmp/scgi_temp \
    /home/app/web/staticfiles

# Set proper permissions
RUN chown -R nginxuser:nginxuser /var/cache/nginx \
    && chown -R nginxuser:nginxuser /var/log/nginx \
    && chown -R nginxuser:nginxuser /etc/nginx/conf.d \
    && chown -R nginxuser:nginxuser /tmp/client_temp \
    && chown -R nginxuser:nginxuser /tmp/proxy_temp_path \
    && chown -R nginxuser:nginxuser /tmp/fastcgi_temp \
    && chown -R nginxuser:nginxuser /tmp/uwsgi_temp \
    && chown -R nginxuser:nginxuser /tmp/scgi_temp \
    && chown -R nginxuser:nginxuser /home/app/web/staticfiles \
    && touch /var/run/nginx.pid \
    && chown -R nginxuser:nginxuser /var/run/nginx.pid

USER nginxuser

EXPOSE 80

ENTRYPOINT ["dumb-init", "nginx", "-g", "daemon off;"]
