# Configuring Ubuntu 18.04 Server

## Update everything

```bash
sudo apt-get update
```

## Nginx and certbot

Install nginx from the default package feed

```bash
sudo apt-get install nginx
```

### Install and configure certbot

Following instructions on [lets-encrypt site for getting certbot setup](https://certbot.eff.org/lets-encrypt/ubuntubionic-nginx)

```bash
$ sudo apt-get install software-properties-common
0 upgraded, 0 newly installed, 0 to remove and 11 not upgraded.

$ sudo add-apt-repository ppa:certbot/certbot
...
Press [ENTER] to continue or Ctrl-c to cancel adding it.
...

$ sudo apt-get update

$ sudo apt-get install python-certbot-nginx
```
