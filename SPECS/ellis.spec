Name:          ellis
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/ellis
Requires:      python-virtualenv
BuildRequires: git, rsync, make, python-virtualenv, gcc-c++
BuildRequires: python-devel, mysql-devel, curl-devel, libffi-devel

Summary: Clearwater - Ellis

%package -n clearwater-prov-tools
Summary: Clearwater - Provisioning Tools

%description
user/number management interface

%description -n clearwater-prov-tools
provisioning tools

%prep
if [ ! -d ellis ]; then
  git config --global url."https://github.com/".insteadOf git@github.com:
  git clone --recursive --branch release-%{version} git@github.com:Metaswitch/ellis.git
fi

%install
cd %{_builddir}/ellis

# The build for some reason requires us to be in a git repository 
if [ ! -d .git ]; then
  git init
fi

make env

# See: debian/ellis.install
mkdir --parents %{buildroot}/usr/share/clearwater/ellis/.wheelhouse/
mkdir --parents %{buildroot}/usr/share/clearwater/ellis/src/metaswitch/ellis/
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

%post
# See: debian/ellis.postinst
useradd --system --no-create-home --home-dir /usr/share/clearwater/ellis --shell /bin/false ellis
mkdir --parents --mode=755 /var/log/ellis
chown --recursive ellis:root /var/log/ellis
virtualenv /usr/share/clearwater/ellis/env
/usr/share/clearwater/ellis/env/bin/pip install --upgrade pip
/usr/share/clearwater/ellis/env/bin/pip install --no-index --find-links /usr/share/clearwater/ellis/.wheelhouse wheel ellis 

%post -n clearwater-prov-tools
# See: debian/clearwater-prov-tools.postinst
useradd --system --no-create-home --home-dir /usr/share/clearwater/clearwater-prov-tools --shell /bin/false clearwater-prov-tools
mkdir --parents --mode=755 /var/log/clearwater-prov-tools
chown --recursive clearwater-prov-tools:root /var/log/clearwater-prov-tools
virtualenv /usr/share/clearwater/clearwater-prov-tools/env
/usr/share/clearwater/clearwater-prov-tools/env/bin/pip install --upgrade pip
/usr/share/clearwater/clearwater-prov-tools/env/bin/pip install --no-index --find-links /usr/share/clearwater/clearwater-prov-tools/.wheelhouse wheel clearwater-prov-tools 

# See: debian/clearwater-prov-tools.links
ln --symbolic /usr/share/clearwater/bin/create_user /usr/bin/cw-create_user
ln --symbolic /usr/share/clearwater/bin/delete_user /usr/bin/cw-delete_user
ln --symbolic /usr/share/clearwater/bin/display_user /usr/bin/cw-display_user
ln --symbolic /usr/share/clearwater/bin/update_user /usr/bin/cw-update_user
ln --symbolic /usr/share/clearwater/bin/list_users /usr/bin/cw-list_users

%preun -n clearwater-prov-tools
rm /usr/bin/cw-create_user
rm /usr/bin/cw-delete_user
rm /usr/bin/cw-display_user
rm /usr/bin/cw-update_user
rm /usr/bin/cw-list_users

%files
/etc/cron.hourly/ellis-log-cleanup
/usr/share/clearwater/bin/poll_ellis.sh
/usr/share/clearwater/bin/poll_ellis_https.sh
/usr/share/clearwater/infrastructure/scripts/ellis
/usr/share/clearwater/infrastructure/scripts/restart/ellis_restart
/usr/share/clearwater/infrastructure/scripts/create-ellis-nginx-config
/usr/share/clearwater/node_type.d/20_ellis
/usr/share/clearwater/ellis/
/usr/share/clearwater/clearwater-diags-monitor/scripts/ellis_diags
%ghost /usr/share/clearwater/ellis/env/
%ghost /var/log/ellis/

# TODO: These config files should be in /etc!
#%config /usr/share/clearwater/ellis/local_settings.py
#%config /usr/share/clearwater/ellis/local_settings.pyo
#%config /usr/share/clearwater/ellis/local_settings.pyc
#%config /usr/share/clearwater/ellis/web-content/js/app-servers.json

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
