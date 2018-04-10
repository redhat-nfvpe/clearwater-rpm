Name:          clearwater-crest
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/crest

Source0:       %{name}-%{version}.tar.bz2
Source1:       common.sh
Source2:       homer.service
Source3:       homer.sh

BuildRequires: make python-virtualenv gcc-c++
BuildRequires: python-devel libffi-devel libxslt-devel openssl-devel
BuildRequires: systemd

%global debug_package %{nil}

Summary:       Clearwater - Crest
Requires:      python-virtualenv libffi libxslt openssl-libs
#Requires:      clearwater-infrastructure clearwater-nginx clearwater-log-cleanup clearwater-monit
AutoReq:       no

%package prov
Summary:       Clearwater - Crest Provisioning
Requires:      python-virtualenv
AutoReq:       no

%package -n clearwater-homer
Summary:       Clearwater - Homer
Requires:      clearwater-crest
#Requires:      clearwater-debian
AutoReq:       no
%{?systemd_requires}

%package -n clearwater-homer-cassandra
Summary:       Clearwater - Cassandra for Homer
Requires:      clearwater-cassandra
#Requires:      clearwater-infrastructure

%package -n clearwater-homestead-prov
Summary:       Clearwater - Homestead Provisioning
Requires:      clearwater-crest

%package -n clearwater-homestead-prov-cassandra
Summary:       Clearwater - Cassandra for Homestead Provisioning
Requires:      clearwater-cassandra clearwater-homestead-cassandra
#Requires:      clearwater-infrastructure

%description
Cassandra-powered generic RESTful HTTP server platform

%description prov
Provision Crest

%description -n clearwater-homer
XDMS

%description -n clearwater-homer-cassandra
Commission Cassandra for Homer

%description -n clearwater-homestead-prov
Provision Homestead

%description -n clearwater-homestead-prov-cassandra
Commission Cassandra for Homestead Provisioning

%prep
%setup

%build
make env MAKE="make --jobs=$(nproc)"

%install
mkdir --parents %{buildroot}%{_unitdir}/
mkdir --parents %{buildroot}/lib/systemd/scripts/
install --mode=644 %{SOURCE2} %{buildroot}%{_unitdir}/homer.service
install --mode=755 %{SOURCE3} %{buildroot}/lib/systemd/scripts/homer.sh

#mkdir --parents %{buildroot}%{_initrddir}/
#install --mode=755 debian/homer.init.d %{buildroot}%{_initrddir}/homer
#install --mode=755 debian/homestead-prov.init.d %{buildroot}%{_initrddir}/homestead-prov

# See: debian/crest.install
mkdir --parents %{buildroot}/usr/share/clearwater/crest/.wheelhouse/
cp --recursive crest_wheelhouse/* %{buildroot}/usr/share/clearwater/crest/.wheelhouse/

# See: debian/crest-prov.install
mkdir --parents %{buildroot}/usr/share/clearwater/crest-prov/src/metaswitch/crest/
mkdir --parents %{buildroot}/usr/share/clearwater/crest-prov/tools/sstable_provisioning/
mkdir --parents %{buildroot}/usr/share/clearwater/crest-prov/.wheelhouse/
cp --recursive src/metaswitch/crest/tools %{buildroot}/usr/share/clearwater/crest-prov/src/metaswitch/crest/
cp src/metaswitch/crest/tools/sstable_provisioning/* %{buildroot}/usr/share/clearwater/crest-prov/tools/sstable_provisioning/
cp crest_wheelhouse/* %{buildroot}/usr/share/clearwater/crest-prov/.wheelhouse/

# See: debian/homer.install
mkdir --parents %{buildroot}/usr/share/clearwater/homer/.wheelhouse/
mkdir --parents %{buildroot}/usr/share/clearwater/homer/src/metaswitch/homer/
mkdir --parents %{buildroot}/usr/share/clearwater/homer/templates/
cp homer_wheelhouse/* %{buildroot}/usr/share/clearwater/homer/.wheelhouse/
cp --recursive src/metaswitch/homer/tools %{buildroot}/usr/share/clearwater/homer/src/metaswitch/homer/
cp homer.local_settings/local_settings.py %{buildroot}/usr/share/clearwater/homer/templates/
cp homer.monit %{buildroot}/usr/share/clearwater/homer/templates/
cp --recursive homer.root/* %{buildroot}/

# See: debian/homer-cassandra.install
cp --recursive homer-cassandra.root/* %{buildroot}/

# See: debian/homestead-prov.install
mkdir --parents %{buildroot}/usr/share/clearwater/homestead/.wheelhouse/
mkdir --parents %{buildroot}/usr/share/clearwater/homestead/templates/
cp homestead_prov_wheelhouse/* %{buildroot}/usr/share/clearwater/homestead/.wheelhouse/
cp homestead.local_settings/local_settings.py %{buildroot}/usr/share/clearwater/homestead/templates/
cp --recursive homestead.root/* %{buildroot}/

# See: debian/homestead-prov-cassandra.install
cp --recursive homestead-prov-cassandra.root/* %{buildroot}/

%files
/usr/share/clearwater/crest/.wheelhouse/

%files prov
/usr/share/clearwater/crest-prov/

%files -n clearwater-homer
%{_unitdir}/homer.service
/lib/systemd/scripts/homer.sh
/usr/share/clearwater/homer/.wheelhouse/
/usr/share/clearwater/homer/handlers/
/usr/share/clearwater/homer/schemas/
/usr/share/clearwater/homer/src/
/usr/share/clearwater/homer/templates/homer.monit
/usr/share/clearwater/bin/poll_homer.sh
/usr/share/clearwater/clearwater-diags-monitor/scripts/homer_diags
/usr/share/clearwater/infrastructure/scripts/restart/homer_restart
/usr/share/clearwater/infrastructure/scripts/create-homer-nginx-config
/usr/share/clearwater/infrastructure/scripts/homer
/usr/share/clearwater/node_type.d/20_homer
%config /usr/share/clearwater/homer/templates/local_settings.py
%config /usr/share/clearwater/homer/templates/local_settings.pyc
%config /usr/share/clearwater/homer/templates/local_settings.pyo
%config /etc/clearwater/secure-connections/homer.conf
%config /etc/cron.hourly/homer-log-cleanup
# %ghost /etc/monit/conf.d/homer.monit

%files -n clearwater-homer-cassandra
/usr/share/clearwater/cassandra/users/homer
/usr/share/clearwater/cassandra-schemas/homer.sh

%files -n clearwater-homestead-prov
#%{_unitdir}/homestead-prov.service
/usr/share/clearwater/homestead/
/usr/share/clearwater/bin/poll_homestead-prov.sh
/usr/share/clearwater/clearwater-diags-monitor/scripts/homestead_prov_diags
/usr/share/clearwater/infrastructure/scripts/restart/homestead_prov_restart
/usr/share/clearwater/infrastructure/scripts/create-homestead-prov-nginx-config
/usr/share/clearwater/infrastructure/scripts/homestead-prov
/usr/share/clearwater/infrastructure/scripts/homestead-prov.monit
%config /etc/clearwater/secure-connections/homestead.conf
%config /etc/cron.hourly/homestead-prov-log-cleanup

%files -n clearwater-homestead-prov-cassandra
/usr/share/clearwater/cassandra/users/homestead-prov
/usr/share/clearwater/cassandra-schemas/homestead_provisioning.sh

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/crest.postinst
cw-create-virtualenv crest
service-action clearwater-secure-connections reload
service-action clearwater-cluster-manager stop
%systemd_post homer.service

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/crest.preun
%systemd_preun homer.service
cw-remove-virtualenv crest

%postun
%systemd_postun_with_restart homer.service

%post prov -p /bin/bash
%include %{SOURCE1}
# See: debian/crest-prov.postinst
cw-create-virtualenv crest-prov crest

%preun prov -p /bin/bash
%include %{SOURCE1}
cw-remove-virtualenv crest-prov

%post -n clearwater-homer -p /bin/bash
%include %{SOURCE1}
# See: debian/homer.postinst
if [ -f /usr/share/clearwater/cassandra-schemas/homer.sh ]; then
  cw-config
  /usr/share/clearwater/cassandra-schemas/homer.sh
fi
cw-add-to-virtualenv crest homer
cw-start homer

%preun -n clearwater-homer -p /bin/bash
%include %{SOURCE1}
# See: debian/homer.prerm
cw-stop homer
# TODO: remove from virtualenv?

%post -n clearwater-homer-cassandra -p /bin/bash
%include %{SOURCE1}
# See: debian/homer-cassandra.postinst
service-action clearwater-infrastructure restart

%post -n clearwater-homestead-prov -p /bin/bash
%include %{SOURCE1}
# See: debian/homestead-prov.postinst
cw-add-to-virtualenv crest homestead homestead-prov
cw-start homestead-prov

%preun -n clearwater-homestead-prov -p /bin/bash
%include %{SOURCE1}
# See: debian/homestead-prov.prerm
cw-stop homestead-prov
rm --force /usr/share/clearwater/homestead/local_settings.py

%post -n clearwater-homestead-prov-cassandra -p /bin/bash
%include %{SOURCE1}
# See: debian/homestead-prov-cassandra.postinst
service-action clearwater-infrastructure restart
