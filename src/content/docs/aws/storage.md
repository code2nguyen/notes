---
title: Storage
---

## EBS Volumn
- Automaticially replicated within a single AZ

### GP2
- 3IOPS / GB, upto 16000 IOP / Volume
- Smaller than 1T can burst up to 3,000 IOP
- IOP change automatically base on size of volume.

### GP3
- baseline 3000 IOP for any size of volume(1G-16T)
- 20% cheeper
- up to 16000 IOP

### IO1
- up to 64000 IOP / Volume
- 50 IOP / G

### IO2
- 500 IOP / G
- Max 64 000 / Volume
- Same price


### IO2 Block Express
- SAN in cloud. Highest performance


### ST1 (HDD)
- 40MB/s per TB
- Max 500MB/s per Volume
=> Frequently access, through out intensive workload, big data, ETL...
=> Can not be boot volume

### SC2 (Cold HDD)
- 12M/s
- max 250M/s


When you create an EBS volume, it must be the same AZ as EC2.