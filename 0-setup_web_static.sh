#!/usr/bin/env bash
#  sets up your web servers for the deployment of web_static

sudo apt-get -y install nginx

mk_dir () {
	if [ ! -d "$1" ];
	then
		sudo mkdir "$1"
	fi
}


mk_dir "/data/"
mk_dir "/data/web_static/"
mk_dir "/data/web_static/releases/"
mk_dir "/data/web_static/shared/"
mk_dir "/data/web_static/releases/test/"

echo "<!DOCTYPE html>
<html>
	<head>
	</head>
	<body>
		<p>Hello DBINN</p>
	</body>
</html>" > /data/web_static/releases/test/index.html

if [ ! -e "/data/web_static/current" ];
then
	ln -s /data/web_static/releases/test/ /data/web_static/current

elif [ -e "/data/web_static/current" ];
then
	rm -r /data/web_static/current
	ln -s /data/web_static/releases/test/ /data/web_static/current
fi

sudo chown -R ubuntu:ubuntu /data/

sed -i "55i \\\n\tlocation /hbnb_static {\n\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-enabled/default
sudo service nginx restart
