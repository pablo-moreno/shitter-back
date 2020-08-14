#!/bin/bash

# Run as sudo!

cp ./deploy/nginx/sites-available/shitter.spookydevs.com /etc/nginx/sites-available/
cp ./deploy/nginx/*.conf /etc/nginx/

ln -s /etc/nginx/sites-available/shitter.spookydevs.com /etc/nginx/sites-enabled/shitter.spookydevs.com
service nginx restart
certbot --nginx
