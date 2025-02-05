---
title: Libraries
---

## Docker local

```sh title="install docker library"
pip install docker
```

```python title="Sample code using docker lib"

from docker import DockerClient

client = DockerClient()

client.containers.run(image='datascientest/neo4j:latest',
                      name='my_neo4j',
                      detach=True,
                      auto_remove=True,
                      ports={
                          '7474/tcp': 7474,
                           '7687/tcp':7687},
                      network='bridge'
                    )

# printing names of active containers
for c in client.containers.list():
    print(c.name, c.image)

```

## Polars

**Compare Pandas vs Polars**

- https://blog.jetbrains.com/pycharm/2024/07/polars-vs-pandas/