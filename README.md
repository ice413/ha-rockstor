# Rockstor integration for Home assistant


Home assistant Integration for Rockstor NAS

## Installation:  
1. In HACS, add this repo as custom repositories  
2. restart HA
3. In Devices and services, add "add integration" and search for rockstor  
4. Fill in the form and click submit.  
5. restart HA

## Sensors:
### For each pool you get these sensors:
| Entity ID | State | Attributes |
|-----------|-------|------------|
Rockstor Pool familyPool Free | 807.83 | unit_of_measurement: GB<br>  device_class: data_size<br>  friendly_name: Rockstor Pool familyPool Free  
Rockstor Pool familyPool Size | 931.51 | unit_of_measurement: GB<br>  device_class: data_size<br>  friendly_name: Rockstor Pool familyPool Size
Rockstor Pool familyPool Used | 123.68 | unit_of_measurement: GB<br>  device_class: data_size<br>  friendly_name: Rockstor Pool familyPool Used

### For each share you get these sensors:
| Entity ID | State | Attributes |
|-----------|-------|------------|
| sensor.rockstor_share_kort_free<br>  Rockstor Share kort Free | 814.01 | state_class: measurement<br>  unit_of_measurement: GB<br>  friendly_name: Rockstor Share kort Free
sensor.rockstor_share_kort_size<br>  Rockstor Share kort Size | 931.0 | state_class: measurement<br>  unit_of_measurement: GB<br>  friendly_name: Rockstor Share kort Size

###  For RockOn's:  
| Entity ID | State | Attributes |
|-----------|-------|------------|
| sensor.rockstor_installed_rock_ons | 1 | Installed:<br>  Nextcloud-Official: started<br>  icon: mdi:docker<br>  friendly_name: Rockstor Installed Rock-ons



# Rockstor 5.0.15 REST API Reference

A list of confirmed REST API endpoints based on Rockstor 5.0.15 (native install).
---

## ✅ Auth & Certificates

- `GET /api/oauth_app`
- `GET /api/oauth_app/<id>`
- `GET /api/certificate`

---

## 📡 Network

- `GET /api/network/interfaces/`
- `GET /api/network/connections/`

---

## 💾 Storage

- `GET /api/disks/`
- `GET /api/pools/`
- `GET /api/shares/`

---

## 📁 Samba (SMB)

- `GET /api/samba`
- `GET /api/samba/<smb_id>`

---

## 📁 NFS

- `GET /api/nfs-exports`
- `GET /api/nfs-exports/<export_id>`
- `GET /api/adv-nfs-exports`

---

## 📁 SFTP

- `GET /api/sftp`
- `GET /api/sftp/<id>`

---

## ⚙️ Rock-ons

- `GET /api/rockons`
- (Additional routes included via `storageadmin.urls.rockons`)

---

## 📧 Email Client

- `GET /api/email`
- `POST /api/email/<command>`

---

## 🔁 Subscriptions

- `GET /api/update-subscriptions`
- `POST /api/update-subscriptions/<action>`

---

## 🔧 Services

- `GET /api/sm/services`
- (More routes from `smart_manager.urls.services`)

---

## 🕒 Task Scheduler

- `GET /api/sm/tasks`
- (More routes from `smart_manager.urls.tasks`)

---

## 🔍 System Probes

- `GET /api/sm/sprobes`
- (More routes from `smart_manager.urls.sprobes`)

---

## 🔄 Replication

- `GET /api/sm/replicas`
- (More routes from `smart_manager.urls.replicas`)

---

## 🔐 Pincard

- `POST /api/pincardmanager/create/<user>`
- `POST /api/pincardmanager/reset/<user>`

---

## 💾 Config Backup

- `GET /api/config-backup`
- `GET /api/config-backup/<backup_id>`
- `POST /api/config-backup/file-upload`

---

## 📊 Dashboard

- `GET /api/dashboardconfig`

---

## 🧠 Notes

- All endpoints require HTTP Basic Auth (e.g., `admin:yourpass`).
- Some APIs support `POST`, `PUT`, `DELETE` — test via curl or browser Dev Tools.
- More endpoints may be dynamically included via nested `urls.py`.



