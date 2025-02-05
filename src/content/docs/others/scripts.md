---
title: Scripts
---

## Docker

```sh title="Start docker service"
sudo service docker start
```

```sh title="Container"
# Run a command in a new container
docker container run hello-world

# Run in iteraction mode
docker container run -it ubuntu:latest # alias docker run
docker container run -it ubuntu:latest bash
docker container run -it --detach ubuntu:latest bash # Run command on mode detach
docker container run -it --rm --detach --name my_ubuntu ubuntu:latest bash # it will remove container after container stopped.
docker container run -it --rm --name my_ubuntu -e "ma_variable='bonjour le monde'" ubuntu:latest bash # add environnement variable.
docker container run -d --rm -e "discovery.type=single-node" -p 9201:9200 -p 9301:9300 --name my_es_container elasticsearch:7.2.0 # Define the communication port.

docker container ls # alias docker ps
docker container ls -a # List all container including containers stopped

docker container start CONTAINER_NAME/ID # Start one or more stopped containers
docker container start -a CONTAINER_NAME/ID # Attach output to console
docker container stop CONTAINER_NAME/ID

docker container rm CONTAINER_NAME/ID # Alias docker rm, docker rm -f 


docker container inspect my_ubuntu
docker container inspect my_es_container | grep IPAddress

```

```sh title="Network"
docker network ls # IPAM: IP Address Management
docker network create --subnet 172.50.0.0/16 --gateway 172.50.0.1 my_network
docker network inspect my_network
docker network inspect host

# Run docker container with a specific network
docker container run -d --rm -e "discovery.type=single-node" --network my_network --name my_es_container3 elasticsearch:7.2.0

# Use the same network of local machine
docker container run -d --rm -e "discovery.type=single-node" --network host --name my_es_container3 elasticsearch:7.2.0

```

```sh title="Volume"
docker volume create --name my_volume
# Then mount this volumn to container
docker container run -it --name my_ubuntu --mount type=volume,src=my_volume,dst=/home/my_folder --rm ubuntu:latest bash

# Mont volumn to a folder
docker container run -it --name my_ubuntu --volume $HOME:/home/my_folder --rm ubuntu:latest bash

docker volume rm my_volume
docker volume inspect my_volume

```


```sh title="Image"
# list all image
docker image ls # alias : docker images

# pull image
docker image pull ubuntu:latest

```

```sh title="Image Build"
docker image build . -t my_image:latest

# Push image
docker login 
docker image push username/imagename:tag

# Créez une archive à partir de l'image créée
docker image save --output my_docker_image.tar my_image
# Recréez l'image à partir de l'archive
docker image load --input my_docker_image.tar

```

```yaml title="Docker Compose"
version: "3.9"
services:
  jupyter:
    image: jupyter/minimal-notebook:ubuntu-18.04
    container_name: my_jupyter_from_compose
    networks:
      - my_network_from_compose
    ports:
      - target: 8888
        published: 4444
        protocol: tcp
        mode: host
    environment:
      JUPYTER_TOKEN: "bonjour"
  elasticsearch:
    image: elasticsearch:7.2.0
    container_name: my_es_from_compose
    networks:
      - my_network_from_compose
    ports:
      - "9200:9200"
      - "9300:9300"
    environment:
      discovery.type: single-node
networks:
  my_network_from_compose:
```


## Bash
```sh title="zip"
tar -cvf exam_VINH.tar exam_VINH
```