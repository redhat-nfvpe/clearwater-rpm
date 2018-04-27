Name:          clearwater-ellis
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/ellis

Source0:       %{name}-%{version}.tar.bz2
Source1:       housekeeping.sh
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
%setup -q

%build
make env MAKE="make --jobs=$(nproc)"

%install
mkdir --parents %{buildroot}/usr/share/clearwater/ellis/.wheelhouse/
mkdir --parents %{buildroot}/usr/share/clearwater/ellis/src/metaswitch/ellis/
mkdir --parents %{buildroot}/usr/share/clearwater/ellis/templates/
cp ellis_wheelhouse/*.whl %{buildroot}/usr/share/clearwater/ellis/.wheelhouse/
rm --recursive web-content/.project web-content/.settings
cp --recursive web-content %{buildroot}/usr/share/clearwater/ellis/
cp local_settings.py %{buildroot}/usr/share/clearwater/ellis/
cp src/metaswitch/ellis/data/*.sql %{buildroot}/usr/share/clearwater/ellis/
cp --recursive src/metaswitch/ellis/tools %{buildroot}/usr/share/clearwater/ellis/src/metaswitch/ellis/
cp *.monit %{buildroot}/usr/share/clearwater/ellis/templates/ # we are putting these here for consistency
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
cp %{SOURCE2} %{buildroot}%{_unitdir}/ellis.service
cp %{SOURCE3} %{buildroot}/lib/systemd/scripts/ellis.sh

sed --in-place 's/\/etc\/init.d\/ellis/service ellis/g' %{buildroot}/usr/share/clearwater/ellis/templates/ellis.monit
sed --in-place 's/\/etc\/init.d\/mysql/service mysql/g' %{buildroot}/usr/share/clearwater/ellis/templates/mysql.monit

#mkdir --parents %{buildroot}%{_initrddir}/
#cp debian/ellis.init.d %{buildroot}%{_initrddir}/ellis.service

%files
%attr(644,-,-) %{_unitdir}/ellis.service
%attr(755,-,-) /lib/systemd/scripts/ellis.sh
%attr(755,-,-) /etc/cron.hourly/ellis-log-cleanup
%attr(755,-,-) /usr/share/clearwater/bin/poll_ellis.sh
%attr(755,-,-) /usr/share/clearwater/bin/poll_ellis_https.sh
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/ellis
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/restart/ellis_restart
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/create-ellis-nginx-config
/usr/share/clearwater/ellis/.wheelhouse
/usr/share/clearwater/ellis/apply_db_updates.sql
%attr(755,-,-) /usr/share/clearwater/ellis/backup/do_backup.sh
%attr(755,-,-) /usr/share/clearwater/ellis/backup/list_backups.sh
%attr(755,-,-) /usr/share/clearwater/ellis/backup/restore_backup.sh
/usr/share/clearwater/ellis/templates/ellis.monit
/usr/share/clearwater/ellis/templates/mysql.monit
/usr/share/clearwater/ellis/schema.sql
%attr(755,-,-) /usr/share/clearwater/ellis/src/metaswitch/ellis/tools/create_numbers.py
/usr/share/clearwater/ellis/src/metaswitch/ellis/tools/create_numbers.pyc
/usr/share/clearwater/ellis/src/metaswitch/ellis/tools/create_numbers.pyo
%attr(755,-,-) /usr/share/clearwater/ellis/src/metaswitch/ellis/tools/sync_databases.py
/usr/share/clearwater/ellis/src/metaswitch/ellis/tools/sync_databases.pyc
/usr/share/clearwater/ellis/src/metaswitch/ellis/tools/sync_databases.pyo
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
/usr/share/clearwater/ellis/local_settings.py*
%config /usr/share/clearwater/ellis/web-content/js/app-servers.json
%ghost /usr/share/clearwater/ellis/env/
%ghost /etc/monit/conf.d/ellis.monit
%ghost /etc/monit/conf.d/mysql.monit

%files -n clearwater-prov-tools
%attr(755,-,-) /usr/share/clearwater/bin/update_user
%attr(755,-,-) /usr/share/clearwater/bin/delete_user
%attr(755,-,-) /usr/share/clearwater/bin/display_user
%attr(755,-,-) /usr/share/clearwater/bin/create_user
%attr(755,-,-) /usr/share/clearwater/bin/list_users
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/clearwater-prov-tools
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
cw_create_user ellis
cw_create_log_dir ellis
cw_create_virtualenv ellis
chown --recursive ellis:root /usr/share/clearwater/ellis/
%systemd_post ellis.service
cw_activate ellis

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/ellis.prerm
%systemd_remove ellis.service
cw_deactivate ellis
cw_remove_virtualenv ellis
if [ "$1" = 0 ]; then # Uninstall
  rm --force /tmp/.ellis-sock*
  cw_remove_user ellis
  cw_remove_log_dir ellis
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

cw_create_user clearwater-prov-tools
cw_create_log_dir clearwater-prov-tools
cw_create_virtualenv clearwater-prov-tools
chown --recursive clearwater-prov-tools:root /usr/share/clearwater/clearwater-prov-tools/
service_action clearwater-infrastructure restart

%preun -n clearwater-prov-tools -p /bin/bash
%include %{SOURCE1}
cw_remove_virtualenv clearwater-prov-tools
if [ "$1" = 0 ]; then # Uninstall
  cw_remove_user clearwater-prov-tools
  cw_remove_log_dir clearwater-prov-tools
fi

# See: debian/clearwater-prov-tools.links
rm --force /usr/bin/cw-create_user
rm --force /usr/bin/cw-delete_user
rm --force /usr/bin/cw-display_user
rm --force /usr/bin/cw-update_user
rm --force /usr/bin/cw-list_users
