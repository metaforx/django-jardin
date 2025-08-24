# django-jardin
A django web application for managing and visualizing data from various sensors in a garden environment and other IoT applications.

- [jardin.dymax.io](https://jardin.dymax.io)
- API uses django ninja for building the RESTful API.
- API secured by ninja static api key authentication.

## Deployment
- Each commit to main branch triggers a GitHub Action workflow that builds and tests the application using Docker.
- Source code is securely transferred to the DigitalOcean droplet, and docker containers are built and started.
- This procedure avoids using Docker Registry.

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