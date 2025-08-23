# django-jardin

## Renew certificate on digital ocean droplet
1. Connect to your droplet via SSH using web console or terminal.
2. Switch to docker directory:
   ```
   cd /opt/django-jardin
   ```
3. Stop the nginx docker container:
   ```
   docker compose -f docker-compose.prod.yml stop nginx
   ```
4. Run the following command to renew the certificate:
   ```
   certbot certonly --standalone -d jardin.dymax.io
   ```
5. If the renewal is successful, restart the web server to apply the new certificate:
    ```
    docker compose -f docker-compose.prod.yml start nginx
    ```