---
title: Amazon ElastiCache
---

Documentation link: https://docs.aws.amazon.com/elasticache/

Amazon ElastiCache is a full managed in-memory data store service. There are two implementations:
- Memcached
- Redis OSS

**Features**

- Billed by node size and hours of use.
- ElastiCache EC2 nodes cannot be accessed from the Internet, nor can they be accessed by EC2 instances in other VPCs.



# Memcached

You can get started with a **serverless cache** or choose to design your own **cache cluster**.

## Comparing Memcached and Redis OSS

Choose Memcached  if the following apply for you:
- You need the simplest model possible (key/value pair)
- You need to cache objects