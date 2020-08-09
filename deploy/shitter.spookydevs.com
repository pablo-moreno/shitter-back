server {
	listen 443 ssl http2;
	listen [::]:443 ssl http2;
	error_log /var/log/shitter/error.log;
	access_log /var/log/shitter/access.log;
	server_name shitter.spookydevs.com;

	# SSL
    ssl_certificate /etc/letsencrypt/live/shitter.spookydevs.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/shitter.spookydevs.com/privkey.pem; # managed by Certbot
	ssl_trusted_certificate /etc/letsencrypt/live/shitter.spookydevs.com/chain.pem;

	# reverse proxy
	location / {
		proxy_pass http://127.0.0.1:8282;
		include nginxconfig.io/proxy.conf;
	}

	location /api {
		proxy_set_header HTTP_X_FORWARDED_PROTO https;
		proxy_pass http://127.0.0.1:8000;
		include nginxconfig.io/proxy.conf;
	}

	location /healthy {
		proxy_set_header HTTP_X_FORWARDED_PROTO https;
		proxy_pass http://127.0.0.1:8000;
		include nginxconfig.io/proxy.conf;
	}
        
        location /admin {
		proxy_set_header HTTP_X_FORWARDED_PROTO https;
		proxy_pass http://127.0.0.1:8000;
		include nginxconfig.io/proxy.conf;
 	}

        # CDN
	location /media/ {
		alias /var/www/shitter/media/;
	}

	location /static/ {
		alias /var/www/shitter/static/;
	}

	include nginxconfig.io/general.conf;

    ssl_certificate /etc/letsencrypt/live/shitter.spookydevs.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/shitter.spookydevs.com/privkey.pem; # managed by Certbot


}

# HTTP redirect
server {
    if ($host = shitter.spookydevs.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


	listen 80;
	listen [::]:80;

	server_name .shitter.spookydevs.com;

	include nginxconfig.io/letsencrypt.conf;

	location / {
		return 301 https://shitter.spookydevs.com$request_uri;
	}


}
