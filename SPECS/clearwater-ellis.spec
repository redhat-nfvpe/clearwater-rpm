Name:          clearwater-ellis
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/ellis

Source0:       %{name}-%{version}.tar.bz2
Source1:       scriptlet-util.sh
Source2:       ellis.service
Source3:       ellis.sh

BuildRequires: make python-virtualenv gcc-c++ ccache
BuildRequires: python-devel mysql-devel curl-devel libffi-devel
BuildRequires: systemd

%global debug_package %{nil}

Summary:       Clearwater - Ellis
Requires:      python-virtualenv python2-pip libffi
Requires:      mariadb-server
AutoReq:       no
%{?systemd_requires}
#Requires:      clearwater-infrastructure clearwater-nginx clearwater-log-cleanup clearwater-monit

%package -n clearwater-prov-tools
Summary:       Clearwater - Provisioning Tools
Requires:      python-virtualenv
AutoReq:       no
#Requires:      clearwater-infrastructure

%package -n clearwater-node-ellis
Summary:       Clearwater Node - Ellis
Requires:      clearwater-ellis clearwater-infrastructure
AutoReq:       no

%description
user/number provisioning portal

%description -n clearwater-prov-tools
provisioning tools

%description -n clearwater-node-ellis
Clearwater Ellis node

%prep
%setup

%build
make env MAKE="make --jobs=$(nproc)"

%install
mkdir --parents %{buildroot}/usr/share/clearwater/ellis/.wheelhouse/
mkdir --parents %{buildroot}/usr/share/clearwater/ellis/src/metaswitch/ellis/
cp ellis_wheelhouse/*.whl %{buildroot}/usr/share/clearwater/ellis/.wheelhouse/
rm --recursive web-content/.project web-content/.settings
cp --recursive web-content %{buildroot}/usr/share/clearwater/ellis/
cp local_settings.py %{buildroot}/usr/share/clearwater/ellis/
cp src/metaswitch/ellis/data/*.sql %{buildroot}/usr/share/clearwater/ellis/
cp --recursive src/metaswitch/ellis/tools %{buildroot}/usr/share/clearwater/ellis/src/metaswitch/ellis/
cp *.monit %{buildroot}/usr/share/clearwater/ellis/
cp --recursive root/* %{buildroot}/
cp --recursive backup %{buildroot}/usr/share/clearwater/ellis/

# See: debian/clearwater-prov-tools.install
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-prov-tools/.wheelhouse/
cp prov_tools_wheelhouse/*.whl %{buildroot}/usr/share/clearwater/clearwater-prov-tools/.wheelhouse/
cp local_settings.py %{buildroot}/usr/share/clearwater/clearwater-prov-tools/
cp --recursive clearwater-prov-tools.root/* %{buildroot}/

# systemd
mkdir --parents %{buildroot}%{_unitdir}/
mkdir --parents %{buildroot}/lib/systemd/scripts/
install --mode=644 %{SOURCE2} %{buildroot}%{_unitdir}/ellis.service
install --mode=755 %{SOURCE3} %{buildroot}/lib/systemd/scripts/ellis.sh

sed --in-place 's/\/etc\/init.d\/ellis/service ellis/g' %{buildroot}/usr/share/clearwater/ellis/ellis.monit
sed --in-place 's/\/etc\/init.d\/mysql/service mysql/g' %{buildroot}/usr/share/clearwater/ellis/mysql.monit

#mkdir --parents %{buildroot}%{_initrddir}/
#install --mode=755 debian/ellis.init.d %{buildroot}%{_initrddir}/ellis.service

%files
%{_unitdir}/ellis.service
/lib/systemd/scripts/ellis.sh
/etc/cron.hourly/ellis-log-cleanup
/usr/share/clearwater/bin/poll_ellis.sh
/usr/share/clearwater/bin/poll_ellis_https.sh
/usr/share/clearwater/infrastructure/scripts/ellis
/usr/share/clearwater/infrastructure/scripts/restart/ellis_restart
/usr/share/clearwater/infrastructure/scripts/create-ellis-nginx-config
/usr/share/clearwater/ellis/.wheelhouse
/usr/share/clearwater/ellis/apply_db_updates.sql
/usr/share/clearwater/ellis/backup/do_backup.sh
/usr/share/clearwater/ellis/backup/list_backups.sh
/usr/share/clearwater/ellis/backup/restore_backup.sh
/usr/share/clearwater/ellis/ellis.monit
/usr/share/clearwater/ellis/mysql.monit
/usr/share/clearwater/ellis/schema.sql
/usr/share/clearwater/ellis/src/metaswitch/ellis/tools/
/usr/share/clearwater/ellis/web-content/addressbook.html
/usr/share/clearwater/ellis/web-content/blank.html
/usr/share/clearwater/ellis/web-content/forgotpassword.html
/usr/share/clearwater/ellis/web-content/index.html
/usr/share/clearwater/ellis/web-content/login.html
/usr/share/clearwater/ellis/web-content/resetpassword.html
/usr/share/clearwater/ellis/web-content/signup.html
/usr/share/clearwater/ellis/web-content/css/
/usr/share/clearwater/ellis/web-content/img/
/usr/share/clearwater/ellis/web-content/js/addressbook.js
/usr/share/clearwater/ellis/web-content/js/app.js
/usr/share/clearwater/ellis/web-content/js/backbone-min.js
/usr/share/clearwater/ellis/web-content/js/backbone.js
/usr/share/clearwater/ellis/web-content/js/bootstrap.js
/usr/share/clearwater/ellis/web-content/js/bootstrap.min.js
/usr/share/clearwater/ellis/web-content/js/common.js
/usr/share/clearwater/ellis/web-content/js/fileuploader.js
/usr/share/clearwater/ellis/web-content/js/forgotpassword.js
/usr/share/clearwater/ellis/web-content/js/jquery.ba-bbq.min.js
/usr/share/clearwater/ellis/web-content/js/jquery.cookie.js
/usr/share/clearwater/ellis/web-content/js/jquery.js
/usr/share/clearwater/ellis/web-content/js/jquery.miniColors.js
/usr/share/clearwater/ellis/web-content/js/jquery.miniColors.min.js
/usr/share/clearwater/ellis/web-content/js/jquery.total-storage.js
/usr/share/clearwater/ellis/web-content/js/jquery.total-storage.min.js
/usr/share/clearwater/ellis/web-content/js/jquery.validate.js
/usr/share/clearwater/ellis/web-content/js/jquery.validate.min.js
/usr/share/clearwater/ellis/web-content/js/json2005.js
/usr/share/clearwater/ellis/web-content/js/loggedout.js
/usr/share/clearwater/ellis/web-content/js/login.js
/usr/share/clearwater/ellis/web-content/js/pwstrength.js
/usr/share/clearwater/ellis/web-content/js/resetpassword.js
/usr/share/clearwater/ellis/web-content/js/signup.js
/usr/share/clearwater/ellis/web-content/js/templates/addressbook-contacts.html
/usr/share/clearwater/ellis/web-content/js/underscore-min.js
/usr/share/clearwater/ellis/web-content/js/underscore.js
/usr/share/clearwater/ellis/web-content/js/zxcvbn-async.js
/usr/share/clearwater/ellis/web-content/js/zxcvbn.js
/usr/share/clearwater/clearwater-diags-monitor/scripts/ellis_diags
%config /usr/share/clearwater/ellis/local_settings.py
%config /usr/share/clearwater/ellis/local_settings.pyo
%config /usr/share/clearwater/ellis/local_settings.pyc
%config /usr/share/clearwater/ellis/web-content/js/app-servers.json
%ghost /usr/share/clearwater/ellis/env/

%files -n clearwater-prov-tools
/usr/share/clearwater/bin/update_user
/usr/share/clearwater/bin/delete_user
/usr/share/clearwater/bin/display_user
/usr/share/clearwater/bin/create_user
/usr/share/clearwater/bin/list_users
/usr/share/clearwater/infrastructure/scripts/clearwater-prov-tools
/usr/share/clearwater/clearwater-prov-tools/
%ghost /usr/share/clearwater/clearwater-prov-tools/env/

%files -n clearwater-node-ellis
/usr/share/clearwater/node_type.d/20_ellis

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/ellis.postinst
systemctl enable mariadb.service
systemctl start mariadb.service
mysql -u root --password= < /usr/share/clearwater/ellis/schema.sql
mysql -u root --password= < /usr/share/clearwater/ellis/apply_db_updates.sql
cw-create-user ellis
cw-create-log-dir ellis
cw-create-virtualenv ellis
chown --recursive ellis:root /usr/share/clearwater/ellis/
%systemd_post ellis.service
cw-start ellis

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/ellis.prerm
%systemd_remove ellis.service
cw-stop ellis
cw-remove-virtualenv ellis
if [ "$1" = 0 ]; then # Uninstall
  rm --force /tmp/.ellis-sock*
  cw-remove-user ellis
  cw-remove-log-dir ellis
fi

%postun
%systemd_postun_with_restart ellis.service

%post -n clearwater-prov-tools -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-prov-tools.links
ln --symbolic /usr/share/clearwater/bin/create_user /usr/bin/cw-create_user
ln --symbolic /usr/share/clearwater/bin/delete_user /usr/bin/cw-delete_user
ln --symbolic /usr/share/clearwater/bin/display_user /usr/bin/cw-display_user
ln --symbolic /usr/share/clearwater/bin/update_user /usr/bin/cw-update_user
ln --symbolic /usr/share/clearwater/bin/list_users /usr/bin/cw-list_users

cw-create-user clearwater-prov-tools
cw-create-log-dir clearwater-prov-tools
cw-create-virtualenv clearwater-prov-tools
chown --recursive clearwater-prov-tools:root /usr/share/clearwater/clearwater-prov-tools/
service-action clearwater-infrastructure restart

%preun -n clearwater-prov-tools -p /bin/bash
%include %{SOURCE1}
cw-remove-virtualenv clearwater-prov-tools
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user clearwater-prov-tools
  cw-remove-log-dir clearwater-prov-tools
fi

# See: debian/clearwater-prov-tools.links
rm --force /usr/bin/cw-create_user
rm --force /usr/bin/cw-delete_user
rm --force /usr/bin/cw-display_user
rm --force /usr/bin/cw-update_user
rm --force /usr/bin/cw-list_users
