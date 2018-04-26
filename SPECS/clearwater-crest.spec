Name:          clearwater-crest
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/crest

Source0:       %{name}-%{version}.tar.bz2
Source1:       housekeeping.sh
Source2:       homer.service
Source3:       homer.sh
Source4:       homestead-prov.service
Source5:       homestead-prov.sh

BuildRequires: make python-virtualenv gcc-c++ ccache
BuildRequires: python-devel libffi-devel libxslt-devel openssl-devel
BuildRequires: systemd

%global debug_package %{nil}

Summary:       Clearwater - Crest
Requires:      python-virtualenv libffi libxslt openssl-libs
AutoReq:       no
#Requires:      clearwater-infrastructure clearwater-nginx clearwater-log-cleanup clearwater-monit

%package prov
Summary:       Clearwater - Crest Provisioning API
Requires:      python-virtualenv
AutoReq:       no

%package -n clearwater-homer
Summary:       Clearwater - Homer
Requires:      clearwater-crest
AutoReq:       no
%{?systemd_requires}

%package -n clearwater-homer-cassandra
Summary:       Clearwater - Cassandra for Homer
Requires:      clearwater-cassandra
AutoReq:       no
#Requires:      clearwater-infrastructure

%package -n clearwater-homestead-prov
Summary:       Clearwater - Homestead Provisioning API
Requires:      clearwater-crest
AutoReq:       no

%package -n clearwater-homestead-prov-cassandra
Summary:       Clearwater - Cassandra for Homestead Provisioning API
Requires:      clearwater-cassandra clearwater-homestead-cassandra
AutoReq:       no
#Requires:      clearwater-infrastructure

%package -n clearwater-node-homer
Summary:       Clearwater Node - Homer
Requires:      clearwater-homer clearwater-infrastructure
AutoReq:       no

%description
Cassandra-powered generic RESTful HTTP server platform

%description prov
Crest provisioning API

%description -n clearwater-homer
XDMS

%description -n clearwater-homer-cassandra
Commission Cassandra for Homer

%description -n clearwater-homestead-prov
Homestead provisioning API

%description -n clearwater-homestead-prov-cassandra
Commission Cassandra for Homestead Provisioning API

%description -n clearwater-node-homer
Clearwater Homer node

%prep
%setup

%build
make env MAKE="make --jobs=$(nproc)"

%install
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

# systemd
mkdir --parents %{buildroot}%{_unitdir}/
mkdir --parents %{buildroot}/lib/systemd/scripts/
cp %{SOURCE2} %{buildroot}%{_unitdir}/homer.service
cp %{SOURCE3} %{buildroot}/lib/systemd/scripts/homer.sh
cp %{SOURCE4} %{buildroot}%{_unitdir}/homestead-prov.service
cp %{SOURCE5} %{buildroot}/lib/systemd/scripts/homestead-prov.sh

sed --in-place 's/\/etc\/init.d\/homestead-prov/service homestead-prov/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/homestead-prov.monit
sed --in-place 's/\/etc\/init.d\/homer/service homer/g' %{buildroot}/usr/share/clearwater/homer/templates/homer.monit
sed --in-place 's/reload clearwater-monit/service reload clearwater-monit/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/homestead-prov.monit

#mkdir --parents %{buildroot}%{_initrddir}/
#cp debian/homer.init.d %{buildroot}%{_initrddir}/homer
#cp debian/homestead-prov.init.d %{buildroot}%{_initrddir}/homestead-prov

%files
/usr/share/clearwater/crest/.wheelhouse/
%ghost /usr/share/clearwater/crest/env/

%files prov
/usr/share/clearwater/crest-prov/

%files -n clearwater-homer
%attr(644,-,-) %{_unitdir}/homer.service
%attr(755,-,-)/lib/systemd/scripts/homer.sh
/usr/share/clearwater/homer/.wheelhouse/
/usr/share/clearwater/homer/handlers/
/usr/share/clearwater/homer/schemas/
/usr/share/clearwater/homer/src/
/usr/share/clearwater/homer/templates/homer.monit
%attr(755,-,-) /usr/share/clearwater/bin/poll_homer.sh
%attr(755,-,-) /usr/share/clearwater/clearwater-diags-monitor/scripts/homer_diags
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/restart/homer_restart
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/create-homer-nginx-config
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/homer
/etc/clearwater/secure-connections/homer.conf
%attr(755,-,-) /etc/cron.hourly/homer-log-cleanup
/usr/share/clearwater/homer/templates/local_settings.py*

%files -n clearwater-homer-cassandra
%attr(755,-,-) /usr/share/clearwater/cassandra/users/homer
%attr(755,-,-) /usr/share/clearwater/cassandra-schemas/homer.sh

%files -n clearwater-homestead-prov
%attr(644,-,-) %{_unitdir}/homestead-prov.service
%attr(755,-,-) /lib/systemd/scripts/homestead-prov.sh
/usr/share/clearwater/homestead/
%attr(755,-,-) /usr/share/clearwater/bin/poll_homestead-prov.sh
%attr(755,-,-) /usr/share/clearwater/clearwater-diags-monitor/scripts/homestead_prov_diags
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/restart/homestead_prov_restart
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/create-homestead-prov-nginx-config
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/homestead-prov
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/homestead-prov.monit
/etc/clearwater/secure-connections/homestead.conf
%attr(755,-,-) /etc/cron.hourly/homestead-prov-log-cleanup
%ghost /etc/monit/conf.d/homestead-prov.monit

%files -n clearwater-homestead-prov-cassandra
%attr(755,-,-) /usr/share/clearwater/cassandra/users/homestead-prov
%attr(755,-,-) /usr/share/clearwater/cassandra-schemas/homestead_provisioning.sh

%files -n clearwater-node-homer
/usr/share/clearwater/node_type.d/20_homer

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/crest.postinst
cw_create_virtualenv crest
service_action clearwater-secure-connections reload
service_action clearwater-cluster-manager stop

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/crest.preun
cw_remove_virtualenv crest

%post prov -p /bin/bash
%include %{SOURCE1}
# See: debian/crest-prov.postinst
cw_create_virtualenv crest-prov crest

%preun prov -p /bin/bash
%include %{SOURCE1}
cw_remove_virtualenv crest-prov

%post -n clearwater-homer -p /bin/bash
%include %{SOURCE1}
# See: debian/homer.postinst
if [ -f /usr/share/clearwater/cassandra-schemas/homer.sh ]; then
  cw_config
  /usr/share/clearwater/cassandra-schemas/homer.sh
fi
cw_add_to_virtualenv crest homer
%systemd_post homer.service
cw_activate homer

%preun -n clearwater-homer -p /bin/bash
%include %{SOURCE1}
# See: debian/homer.prerm
cw_deactivate homer
# TODO: remove from virtualenv?
%systemd_preun homer.service

%postun -n clearwater-homer
%systemd_postun_with_restart homer.service

%post -n clearwater-homer-cassandra -p /bin/bash
%include %{SOURCE1}
# See: debian/homer-cassandra.postinst
service_action clearwater-infrastructure restart

%post -n clearwater-homestead-prov -p /bin/bash
%include %{SOURCE1}
# See: debian/homestead-prov.postinst
cw_add_to_virtualenv crest homestead homestead-prov
%systemd_post homestead-prov.service
cw_activate homestead-prov

%preun -n clearwater-homestead-prov -p /bin/bash
%include %{SOURCE1}
# See: debian/homestead-prov.prerm
cw_deactivate homestead-prov
rm --force /usr/share/clearwater/homestead/local_settings.py*
%systemd_preun homestead-prov.service

%postun -n clearwater-homestead-prov
%systemd_postun_with_restart homestead-prov.service

%post -n clearwater-homestead-prov-cassandra -p /bin/bash
%include %{SOURCE1}
# See: debian/homestead-prov-cassandra.postinst
service_action clearwater-infrastructure restart
