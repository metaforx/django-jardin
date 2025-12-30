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

## Private Jellyfin Backbone (frp Tunnel)

Not really related to this project, but useful to run on a VPS alongside it.

Expose your home Jellyfin securely over a VPS without opening any home firewall ports.
All traffic flows through an encrypted frp backbone tunnel.

```
Client (Phone / TV / Web)
        │
        ▼
music.dymax.io  (HTTPS, VPS Nginx)
        │
        │  frp encrypted tunnel
        ▼
Volumio Jellyfin (LAN only, no external access)
```

``` bash
# On your VPS (Digital Ocean Droplet)
sudo systemctl start frps
sudo systemctl stop frps
sudo systemctl restart frps
```

### Configuration file path on VPS and Client
``` bash
/etc/frp/frps.toml
```