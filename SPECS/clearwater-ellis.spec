Name:          clearwater-ellis
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/ellis

Source0:       %{name}-%{version}.tar.bz2
BuildRequires: rsync make python-virtualenv gcc-c++
BuildRequires: python-devel mysql-devel curl-devel libffi-devel

%global debug_package %{nil}

Summary:       Clearwater - Ellis
Requires:      clearwater-infrastructure clearwater-nginx clearwater-log-cleanup clearwater-monit
Requires:      python-virtualenv libffi

%package -n clearwater-prov-tools
Summary:       Clearwater - Provisioning Tools
Requires:      clearwater-infrastructure
Requires:      python-virtualenv

%description
user/number management interface

%description -n clearwater-prov-tools
provisioning tools

%prep
%setup

%build
make env

%install
# See: debian/ellis.install
mkdir --parents %{buildroot}%{_initrddir}/
mkdir --parents %{buildroot}/usr/share/clearwater/ellis/.wheelhouse/
mkdir --parents %{buildroot}/usr/share/clearwater/ellis/src/metaswitch/ellis/
rsync debian/ellis.init.d %{buildroot}%{_initrddir}/ellis
rsync ellis_wheelhouse/*.whl %{buildroot}/usr/share/clearwater/ellis/.wheelhouse/
rsync --recursive --exclude .project --exclude .settings web-content %{buildroot}/usr/share/clearwater/ellis/
rsync local_settings.py %{buildroot}/usr/share/clearwater/ellis/
rsync src/metaswitch/ellis/data/*.sql %{buildroot}/usr/share/clearwater/ellis/
rsync --recursive src/metaswitch/ellis/tools %{buildroot}/usr/share/clearwater/ellis/src/metaswitch/ellis/
rsync *.monit %{buildroot}/usr/share/clearwater/ellis/
rsync --recursive root/* %{buildroot}/
rsync --recursive backup %{buildroot}/usr/share/clearwater/ellis/

# See: debian/clearwater-prov-tools.install
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-prov-tools/.wheelhouse/
rsync prov_tools_wheelhouse/*.whl %{buildroot}/usr/share/clearwater/clearwater-prov-tools/.wheelhouse/
rsync local_settings.py %{buildroot}/usr/share/clearwater/clearwater-prov-tools/
rsync --recursive clearwater-prov-tools.root/* %{buildroot}/

%files
%{_initrddir}/ellis
/etc/cron.hourly/ellis-log-cleanup
/usr/share/clearwater/bin/poll_ellis.sh
/usr/share/clearwater/bin/poll_ellis_https.sh
/usr/share/clearwater/infrastructure/scripts/ellis
/usr/share/clearwater/infrastructure/scripts/restart/ellis_restart
/usr/share/clearwater/infrastructure/scripts/create-ellis-nginx-config
/usr/share/clearwater/node_type.d/20_ellis
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
%ghost /var/log/ellis/
# TODO: %ghost /etc/monit/conf.d/*.monit

%files -n clearwater-prov-tools
/usr/share/clearwater/bin/update_user
/usr/share/clearwater/bin/delete_user
/usr/share/clearwater/bin/display_user
/usr/share/clearwater/bin/create_user
/usr/share/clearwater/bin/list_users
/usr/share/clearwater/infrastructure/scripts/clearwater-prov-tools
/usr/share/clearwater/clearwater-prov-tools/
%ghost /usr/share/clearwater/clearwater-prov-tools/env/
%ghost /var/log/clearwater-prov-tools/

%post
# See: debian/ellis.postinst
set -e
if ! grep -q "^ellis:" /etc/passwd; then
  useradd --system --no-create-home --home-dir /usr/share/clearwater/ellis/ --shell /bin/false ellis
fi
mkdir --parents --mode=755 /var/log/ellis/
chown --recursive ellis:root /var/log/ellis/
virtualenv /usr/share/clearwater/ellis/env/
/usr/share/clearwater/ellis/env/bin/pip install --upgrade pip
#/usr/share/clearwater/ellis/env/bin/pip install /usr/share/clearwater/ellis/.wheelhouse/pip-*.whl
/usr/share/clearwater/ellis/env/bin/pip install --no-index --find-links /usr/share/clearwater/ellis/.wheelhouse/ wheel ellis
chown --recursive ellis:root /usr/share/clearwater/ellis/
mysql -u root --password= < /usr/share/clearwater/ellis/schema.sql
mysql -u root --password= < /usr/share/clearwater/ellis/apply_db_updates.sql
service clearwater-infrastructure restart
cp /usr/share/clearwater/ellis/*.monit /etc/monit/conf.d/
service clearwater-monit reload || /bin/true
service ellis stop || /bin/true

%preun
# See: debian/ellis.prerm
set -e
for F in /usr/share/clearwater/ellis/*.monit; do rm --force "/etc/monit/conf.d/$(basename "$F")"; done
service clearwater-monit reload || /bin/true
service ellis stop
rm --recursive --force /usr/share/clearwater/ellis/env
rm --recursive --force /var/run/ellis/
if [ "$1" = 0 ]; then # Uninstall
  rm --force /tmp/.ellis-sock*
  if grep -q "^ellis:" /etc/passwd; then
    userdel ellis
  fi
fi

%post -n clearwater-prov-tools
# See: debian/clearwater-prov-tools.links
set -e
ln --symbolic /usr/share/clearwater/bin/create_user /usr/bin/cw-create_user
ln --symbolic /usr/share/clearwater/bin/delete_user /usr/bin/cw-delete_user
ln --symbolic /usr/share/clearwater/bin/display_user /usr/bin/cw-display_user
ln --symbolic /usr/share/clearwater/bin/update_user /usr/bin/cw-update_user
ln --symbolic /usr/share/clearwater/bin/list_users /usr/bin/cw-list_users

# See: debian/clearwater-prov-tools.postinst
if ! grep -q "^clearwater-prov-tools:" /etc/passwd; then
  useradd --system --no-create-home --home-dir /usr/share/clearwater/clearwater-prov-tools/ --shell /bin/false clearwater-prov-tools
fi
mkdir --parents --mode=755 /var/log/clearwater-prov-tools/
chown --recursive clearwater-prov-tools:root /var/log/clearwater-prov-tools/
virtualenv /usr/share/clearwater/clearwater-prov-tools/env/
/usr/share/clearwater/clearwater-prov-tools/env/bin/pip install --upgrade pip
/usr/share/clearwater/clearwater-prov-tools/env/bin/pip install --no-index --find-links /usr/share/clearwater/clearwater-prov-tools/.wheelhouse/ wheel clearwater-prov-tools 
chown --recursive clearwater-prov-tools:root /usr/share/clearwater/clearwater-prov-tools/
mkdir --parents /var/log/clearwater-prov-tools/
service clearwater-infrastructure restart

%preun -n clearwater-prov-tools
set -e
rm --recursive --force /usr/share/clearwater/clearwater-prov-tools/env/
if [ "$1" = 0 ]; then # Uninstall
  rm --recursive --force /var/log/clearwater-prov-tools
fi
rm --force /usr/bin/cw-create_user
rm --force /usr/bin/cw-delete_user
rm --force /usr/bin/cw-display_user
rm --force /usr/bin/cw-update_user
rm --force /usr/bin/cw-list_users
