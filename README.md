# My youtube

## 1. Launch the project

**In order to run the project using localhost, create :**

- `.env` file:
  * Path: `./`
  * Content :
    ```bash
    API_MOD=DEV #API DEBUG MOD
    DOMAIN=localhost #the domain your deploying on
    EMAIL=eliot.courtel@wanadoo.fr #a mail to be used in let's encrypt
    DB_USER=myyoutube #a database username
    DB_PASS=1q2W3e4R #a database password
    ```


**You're ready to deploy the infrastructure**

* ```bash
  docker-compose -f docker-compose.yml -f docker-compose.admin.yml up -d
  ```

**Lastly:**

* Go to `http://admin.${YOUR_DOMAIN}/phpmyadmin/` and import `./webapp/db/sql/dumps/youtube.sql` into the **youtube**'s database

**You can know use the landing page, the dashboard and the api properly !**


## 2. Administrate the project

There are multiple functionnalities available to manage your project, for exemple **goaccess** available at `http://admin.${YOUR_DOMAIN}/stats/` allow you to see up-to-date statistics of your website

To use this service you'll need to create a few files:


- `api.${YOUR_DOMAIN}_location` file:
  * Path: `./proxy/vhost/`
  * Content:
    ```perl
    access_log  /customlogs/api.${YOUR_DOMAIN}.log  main;
    ```

Feel free to add anylog services exposed to the outworld by adding an `_location` file into `./proxy/vhost/`, don't forget to add the proper command to the `goaccesscli` container's entrypoint:
```perl
entrypoint: "watch `goaccess /logs/api.${DOMAIN}.log -o /results/api${DOMAIN}.html --log-format=COMBINED;
                    ${YOUR_COMMAND};`
                "
```
**⚠️ Warning : `DOMAIN` env variable refer to the one define in `.env`**

Composition of the command is: `goaccess ${LOGFILE} -o {HTML_OUTPUT} --logformat=COMBINED`

## 3. Secure your project

To secure the project you can use *Basic Auth* by simply using
```bash
htpasswd -c ./proxy/passwd/${THE_DOMAIN_TO_PROTECT} ${YOUR_USER}
```
(For example `htpasswd -c ./proxy/passwd/admin.localhost test`)
