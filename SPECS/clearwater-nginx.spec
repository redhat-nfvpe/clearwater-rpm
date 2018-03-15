Name:          clearwater-nginx
Version:       129
Release:       1%{?dist}
License:       AGPLv3+
URL:           https://github.com/Metaswitch/clearwater-nginx

Source0:       %{name}-%{version}.tar.bz2

%global debug_package %{nil}

Summary:       Clearwater - Nginx
Requires:      clearwater-infrastructure clearwater-monit
Requires:      nginx openssl

%description
Nginx configured for Clearwater

%prep
%setup

%install
# See: debian/clearwater-nginx.install
mkdir --parents %{buildroot}/usr/bin/
cp --recursive clearwater-nginx/* %{buildroot}/
cp nginx-ensite/nginx_ensite %{buildroot}/usr/bin/
cp nginx-ensite/nginx_dissite %{buildroot}/usr/bin/

%files
/usr/bin/nginx_ensite
/usr/bin/nginx_dissite
/usr/share/clearwater/infrastructure/alarms/nginx_alarms.json
/usr/share/clearwater/infrastructure/monit_uptime/check-nginx-uptime
/usr/share/clearwater-nginx/nginx_ping
/usr/share/clearwater-nginx/nginx.monit
/usr/share/clearwater-nginx/run-in-nginx-namespace
%config /etc/nginx/sites-available/ping
%config /etc/nginx/ssl/nginx_openssl_config

%post
# See: debian/clearwater-nginx.postinst
set -e
install /usr/share/clearwater-nginx /etc/monit/conf.d/nginx.monit
rm --force /etc/nginx/sites-enabled/default
rm --force /etc/nginx/sites-available/default
nginx_ensite ping
mkdir --parents /etc/nginx/ssl/
cd /etc/nginx/ssl/
openssl req -nodes -sha256 -newkey rsa:2048 -keyout nginx.key -out nginx.csr -config nginx_openssl_config
openssl x509 -sha256 -req -in nginx.csr -signkey nginx.key -out nginx.crt
service nginx stop || /bin/true
service clearwater-monit reload || /bin/true

%preun
# See: debian/clearwater-nginx.prerm
set -e
rm --force /etc/monit/conf.d/nginx.monit
service clearwater-monit reload || /bin/true
nginx_dissite ping
service nginx reload
