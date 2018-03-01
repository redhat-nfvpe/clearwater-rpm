Name:          ellis
Version:       129
Release:       1%{?dist}
Summary:       Clearwater - Ellis
License:       GPLv3+
URL:           https://github.com/Metaswitch/ellis
Requires:      python-virtualenv
BuildRequires: python-virtualenv, mysql-devel, curl-devel, libffi-devel, gcc-c++, git
Source0:       ellis.tar.gz
Source1:       python-common.tar.gz
Source2:       cpp-common.tar.gz
Source3:       clearwater-build-infra.tar.gz

%package -n clearwater-prov-tools
Summary: Clearwater - Provisioning Tools

%description
Ellis is a sample provisioning portal providing self sign-up, password management, line management
and control of MMTEL service settings. It is not intended to be a part of production Clearwater
deployments (it is not easy to horizontally scale because of the MySQL underpinnings for one thing)
but to make the system easy to use out of the box.

%description -n clearwater-prov-tools
Provisioning Tools.

%prep
if [ ! -d ellis ]; then
  mkdir -p ellis
  cd ellis
  tar -xzf %{_sourcedir}/ellis.tar.gz --strip-components=1
  cd build-infra
  tar -xzf %{_sourcedir}/clearwater-build-infra.tar.gz --strip-components=1
  cd ../common
  tar -xzf %{_sourcedir}/python-common.tar.gz --strip-components=1
  cd build-infra
  tar -xzf %{_sourcedir}/clearwater-build-infra.tar.gz --strip-components=1
  cd ../cpp-common
  tar -xzf %{_sourcedir}/cpp-common.tar.gz --strip-components=1
fi

%install
cd %{_builddir}/ellis
if [ ! -d .git ]; then
  git init
fi
make env

# See: debian/ellis.install
mkdir -p %{buildroot}/usr/share/clearwater/ellis/.wheelhouse/
mkdir -p %{buildroot}/usr/share/clearwater/ellis/src/metaswitch/ellis/
cp ellis_wheelhouse/*.whl %{buildroot}/usr/share/clearwater/ellis/.wheelhouse/
cp -r web-content %{buildroot}/usr/share/clearwater/ellis/
cp local_settings.py %{buildroot}/usr/share/clearwater/ellis/
cp src/metaswitch/ellis/data/*.sql %{buildroot}/usr/share/clearwater/ellis/
cp -r src/metaswitch/ellis/tools %{buildroot}/usr/share/clearwater/ellis/src/metaswitch/ellis/
cp *.monit %{buildroot}/usr/share/clearwater/ellis/
cp -r root/* %{buildroot}/
cp -r backup %{buildroot}/usr/share/clearwater/ellis/

# See: debian/clearwater-prov-tools.install
mkdir -p %{buildroot}/usr/share/clearwater/clearwater-prov-tools/.wheelhouse/
cp prov_tools_wheelhouse/*.whl %{buildroot}/usr/share/clearwater/clearwater-prov-tools/.wheelhouse/
cp local_settings.py %{buildroot}/usr/share/clearwater/clearwater-prov-tools/
cp -r clearwater-prov-tools.root/* %{buildroot}/

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

%files
/etc/cron.hourly/ellis-log-cleanup
#/usr/share/doc/ellis/
/usr/share/clearwater/bin/poll_ellis.sh
/usr/share/clearwater/bin/poll_ellis_https.sh
/usr/share/clearwater/infrastructure/scripts/ellis
/usr/share/clearwater/infrastructure/scripts/restart/ellis_restart
/usr/share/clearwater/infrastructure/scripts/create-ellis-nginx-config
/usr/share/clearwater/node_type.d/20_ellis
/usr/share/clearwater/ellis/
/usr/share/clearwater/clearwater-diags-monitor/scripts/ellis_diags

%files -n clearwater-prov-tools
#/usr/share/doc/clearwater-prov-tools/
/usr/share/clearwater/bin/update_user
/usr/share/clearwater/bin/delete_user
/usr/share/clearwater/bin/display_user
/usr/share/clearwater/bin/create_user
/usr/share/clearwater/bin/list_users
/usr/share/clearwater/infrastructure/scripts/clearwater-prov-tools
/usr/share/clearwater/clearwater-prov-tools/
