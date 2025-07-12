# Rockstor integration for Home assistant


Home assistant Integration for Rockstor NAS

## Installation:  
1. In HACS, add this repo as custom repositories  
2. restart HA
3. In Devices and services, add "add integration" and search for rockstor  
4. Fill in the form and click submit.  
5. restart HA

## Sensors:
For each pool you get these sensors:
| Entity ID | State | Attributes |
|-----------|-------|------------|
Rockstor Pool familyPool Free | 807.83 | unit_of_measurement: GB,  device_class: data_size,  friendly_name: Rockstor Pool familyPool Free  
Rockstor Pool familyPool Size | 931.51 | unit_of_measurement: GB,device_class: data_size, friendly_name: Rockstor Pool familyPool Size
Rockstor Pool familyPool Used | 123.68 | unit_of_measurement: GB, device_class: data_size, friendly_name: Rockstor Pool familyPool Used


## To be continued...
