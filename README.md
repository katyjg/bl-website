Quick Start
===========

A test deployment using docker-compose is included with this website code.
To use it, extract deploy/skel.tar.gz in a directory of your choice.

**Dependences:** 
 - Docker Engine 1.13.0+
 - Docker Compose
 
**Testing:**
 1. Extract deploy/skel.tar.gz in a directory of your choice
 2. Verify that the `hostname` and `SERVER_NAME` are correct in docker-compose.yml
 3. `docker-compose pull` 
 4. `docker-compose up -d` 
     - a new postgresql database is created in `./database/`, 
     - self-signed SSL certificates are created in `./certs/`,
     - a file `.db-init` is created in `./app-local/`
 5. `./test-site.sh <BEAMLINE_NAME>`
     - follow prompts to create an administrator account
     - a basic set of web pages are created for testing
 6. Find your new test website at https://{SERVER_NAME}
 7. Sign in with your new administrator account at https://{SERVER_NAME}/admin
 
**Deployment:**

The contents of the skel directory are:
```
    ├── app-local                   # local directory, mounted in docker container as /website/local
    │   ├── logs                    # location for apache access_log and error_log
    │   ├── media                   # location of uploaded files
    │   │   └── original_images     # images only included for testing
    │   │       ├── crystal-background.jpg
    │   │       ├── logo.png
    │   │       └── pattern.png
    │   └── settings.py             # local settings (used to change database, email settings, etc.)
    ├── certs                       # location of SSL certificates, mounted by default in docker container as /custom-certs
    ├── database-backups            # directory for backups of postgresql database, needed if using postgres-bkup:latest
    ├── database-init               # directory for files used to automate creation of databases on startup of postgres-bkup:latest
    │   └── website.sh
    ├── docker-compose.yml          
    └── test-site.sh                
```