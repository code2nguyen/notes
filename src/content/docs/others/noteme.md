---
title: Noteme
---


## Portainer
[Portainer](https://www.portainer.io/) est une interface graphique de Docker Open Source, qui tourne dans un container. Sa prise en main est assez intuitive et son lancement est plutôt simple:

```sh title="start portainer"
docker volume create portainer_data
docker run -d -p 8000:8000 -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce
```


## Open sources

- Redash - Open Source Alternative to Power BI, tableau, MicroStrategy, Qlik
- n8n - Open Source Alternative to Zapier, Make
- Supabase — The open source Firebase alternative
