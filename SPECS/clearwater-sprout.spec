Name:          clearwater-sprout
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/sprout

Source0:       %{name}-%{version}.tar.bz2
Source1:       common.sh
Source2:       sprout.service
Source3:       sprout.sh
Source4:       bono.service
Source5:       bono.sh
Source6:       restund.service
Source7:       restund.sh
Source8:       clearwater-sip-stress.service
Source9:       clearwater-sip-stress.sh
Source10:      clearwater-sip-stress-stats.service
Source11:      clearwater-sip-stress-stats.sh
Source12:      clearwater-sip-perf.service
Source13:      clearwater-sip-perf.sh

BuildRequires: make cmake libtool gcc-c++ byacc flex rubygems rsync
BuildRequires: libevent-devel boost-devel boost-static openssl-devel ncurses-devel zeromq-devel
BuildRequires: net-snmp-devel
BuildRequires: systemd

# Note: Why byacc and not bison? Because libmemached for some reason breaks with our version of
# bison, but is OK with byacc. (Why, then, do other specs (ralf, homestead) that have libmemcached
# build fine with bison?)

# Note: zeromq-devel requires epel-release

%global debug_package %{nil}

Summary:       Clearwater - Sprout
Requires:      clearwater-sprout-libs
Requires:      libevent openssl-libs ncurses zeromq net-snmp-libs
%{?systemd_requires}

%package libs
Summary:       Clearwater - Sprout Libraries

%package plugin-scscf
Summary: Clearwater - Sprout S-CSCF Plugin

%package plugin-icscf
Summary: Clearwater - Sprout I-CSCF Plugin

%package plugin-bgcf
Summary: Clearwater - Sprout BGCF Plugin

%package as-plugin-mmtel
Summary: Clearwater - Sprout MMTEL Application Server Plugin

%package as-plugin-gemini
Summary: Clearwater - Sprout Gemini Application Server Plugin

%package as-plugin-memento
Summary: Clearwater - Sprout Memento Application Server Plugin

%package as-plugin-call-diversion
Summary: Clearwater - Sprout Call Diversion Application Server Plugin

%package as-plugin-mangelwurzel
Summary: Clearwater - Sprout Mangelwurzel Application Server Plugin

%package -n clearwater-bono
Summary: Clearwater - Bono
%{?systemd_requires}

%package -n clearwater-restund
Summary: Clearwater - restund
%{?systemd_requires}

%package -n clearwater-sipp
Summary: Clearwater - SIPp

%package -n clearwater-sip-stress
Summary: Clearwater - SIP Stress Tests
%{?systemd_requires}

%package -n clearwater-sip-stress-stats
Summary: Clearwater - SPI Stress Tests Statistics
%{?systemd_requires}

%package -n clearwater-sip-perf
Summary: Clearwater - SIP Performance Tests
%{?systemd_requires}

%description
SIP router

%description libs
Sprout libraries

%description plugin-scscf
SIP router S-CSCF plugin

%description plugin-icscf
SIP router I-CSCF plugin

%description plugin-bgcf
SIP router BGCF plugin

%description as-plugin-mmtel
SIP router MMTEL application server plugin

%description as-plugin-gemini
Mobile twinning application server plugin

%description as-plugin-memento
Call list application server plugin

%description as-plugin-call-diversion
Call diversion application server plugin

%description as-plugin-mangelwurzel
B2BUA and SCC-AS emulator application server plugin

%description -n clearwater-bono
SIP edge proxy

%description -n clearwater-restund
STUN/TURN server

%description -n clearwater-sipp
Clearwater build of SIPp, used for running SIP stress and performance tests

%description -n clearwater-sip-stress
Runs SIP stress against Clearwater

%description -n clearwater-sip-stress-stats
Exposes SIP stress statistics over the Clearwater statistics interface.

%description -n clearwater-sip-perf
Runs SIP performance tests against Clearwater

%prep
%setup

%build
# pjsip fails to build in concurrent mode, so override
sed --in-place '1ioverride MAKE = make' modules/pjsip/Makefile

make MAKE="make --jobs=$(nproc)"

%install
mkdir --parents %{buildroot}%{_unitdir}/
mkdir --parents %{buildroot}/lib/systemd/scripts/
install --mode=644 %{SOURCE2} %{buildroot}%{_unitdir}/sprout.service
install --mode=755 %{SOURCE3} %{buildroot}/lib/systemd/scripts/sprout.sh
install --mode=644 %{SOURCE4} %{buildroot}%{_unitdir}/bono.service
install --mode=755 %{SOURCE5} %{buildroot}/lib/systemd/scripts/bono.sh
install --mode=644 %{SOURCE6} %{buildroot}%{_unitdir}/restund.service
install --mode=755 %{SOURCE7} %{buildroot}/lib/systemd/scripts/restund.sh
install --mode=644 %{SOURCE8} %{buildroot}%{_unitdir}/clearwater-sip-stress.service
install --mode=755 %{SOURCE9} %{buildroot}/lib/systemd/scripts/clearwater-sip-stress.sh
install --mode=644 %{SOURCE10} %{buildroot}%{_unitdir}/clearwater-sip-stress-stats.service
install --mode=755 %{SOURCE11} %{buildroot}/lib/systemd/scripts/clearwater-sip-stress-stats.sh
install --mode=644 %{SOURCE12} %{buildroot}%{_unitdir}/clearwater-sip-perf.service
install --mode=755 %{SOURCE13} %{buildroot}/lib/systemd/scripts/clearwater-sip-perf.sh

#mkdir --parents %{buildroot}%{_initrddir}/
#install --mode=755 debian/bono.init.d %{buildroot}%{_initrddir}/bono
#install --mode=755 debian/restund.init.d %{buildroot}%{_initrddir}/restund
#install --mode=755 debian/clearwater-sip-stress.init.d %{buildroot}%{_initrddir}/clearwater-sip-stress
#install --mode=755 debian/clearwater-sip-stress-stats.init.d %{buildroot}%{_initrddir}/clearwater-sip-stress-stats
#install --mode=755 debian/clearwater-sip-perf.init.d %{buildroot}%{_initrddir}/clearwater-sip-perf

# See: debian/sprout-base.install
mkdir --parents %{buildroot}/usr/share/clearwater/bin/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
mkdir --parents %{buildroot}/etc/cron.hourly/
cp build/bin/sprout %{buildroot}/usr/share/clearwater/bin/
cp --recursive sprout-base.root/* %{buildroot}/
rm %{buildroot}/etc/init.d/sprout
cp scripts/sprout-log-cleanup %{buildroot}/etc/cron.hourly/
cp modules/clearwater-etcd-plugins/sprout/sprout_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp modules/clearwater-etcd-plugins/sprout/sprout_scscf_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp modules/clearwater-etcd-plugins/sprout/sprout_enum_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp modules/clearwater-etcd-plugins/sprout/sprout_rph_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp modules/clearwater-etcd-plugins/clearwater_config_access/scscf_json_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
cp modules/clearwater-etcd-plugins/clearwater_config_access/enum_json_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
cp modules/clearwater-etcd-plugins/clearwater_config_access/rph_json_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/

# See: debian/sprout-libs.install
mkdir --parents %{buildroot}/usr/share/clearwater/sprout/lib/
cp usr/lib/*.so %{buildroot}/usr/share/clearwater/sprout/lib/
cp usr/lib/*.so.* %{buildroot}/usr/share/clearwater/sprout/lib/

# See: debian/sprout-scscf.install
mkdir --parents %{buildroot}/usr/share/clearwater/sprout/plugins
cp build/bin/sprout_scscf.so %{buildroot}/usr/share/clearwater/sprout/plugins/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/shared_ifcs_xml_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/fallback_ifcs_xml_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/remove_shared_ifcs_xml %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/remove_fallback_ifcs_xml %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/validate_shared_ifcs_xml %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/validate_fallback_ifcs_xml %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/display_shared_ifcs %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/display_fallback_ifcs %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/config_validation/* %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/
cp modules/clearwater-etcd-plugins/clearwater_config_access/shared_ifcs_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
cp modules/clearwater-etcd-plugins/clearwater_config_access/fallback_ifcs_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/

# See: debian/sprout-icscf.install
cp build/bin/sprout_icscf.so %{buildroot}/usr/share/clearwater/sprout/plugins/

# See: debian/sprout-bgcf.install
cp build/bin/sprout_bgcf.so %{buildroot}/usr/share/clearwater/sprout/plugins/
cp --recursive sprout-bgcf.root/* %{buildroot}/
cp modules/clearwater-etcd-plugins/sprout/sprout_bgcf_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp modules/clearwater-etcd-plugins/clearwater_config_access/bgcf_json_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/

# See: debian/sprout-mmtel-as.install
cp build/bin/sprout_mmtel_as.so %{buildroot}/usr/share/clearwater/sprout/plugins/
cp --recursive sprout-mmtel-as.root/* %{buildroot}/

# See: debian/gemini-as.install
cp build/bin/gemini-as.so %{buildroot}/usr/share/clearwater/sprout/plugins/

# See: debian/memento-as.install
cp build/bin/memento-as.so %{buildroot}/usr/share/clearwater/sprout/plugins/
cp --recursive memento-as.root/* %{buildroot}/

# See: debian/call-diversion-as.install
cp build/bin/call-diversion-as.so %{buildroot}/usr/share/clearwater/sprout/plugins/

# See: debian/mangelwurzel-as.install
cp build/bin/mangelwurzel-as.so %{buildroot}/usr/share/clearwater/sprout/plugins/

# See: debian/bono.install
cp build/bin/sprout %{buildroot}/usr/share/clearwater/bin/bono
cp --recursive bono.root/* %{buildroot}/
cp scripts/bono-log-cleanup %{buildroot}/etc/cron.hourly/

# See: debian/restund.install
mkdir --parents %{buildroot}/usr/share/clearwater/restund/lib/
cp usr/sbin/restund %{buildroot}/usr/share/clearwater/bin/
cp usr/lib/libre.* %{buildroot}/usr/share/clearwater/restund/lib/
cp usr/lib/restund/modules/* %{buildroot}/usr/share/clearwater/restund/lib/
cp --recursive restund.root/* %{buildroot}/

# See: debian/clearwater-sipp.install
cp --recursive clearwater-sipp.root/* %{buildroot}/
cp modules/sipp/sipp %{buildroot}/usr/share/clearwater/bin/

# See: debian/clearwater-sip-stress.install
cp --recursive clearwater-sip-stress.root/* %{buildroot}/

# See: debian/clearwater-sip-stress-stats.install
mkdir --parents %{buildroot}/usr/share/clearwater/gems/
cp scripts/sipp-stats/clearwater-sipp-stats-*.gem %{buildroot}/usr/share/clearwater/gems/

# See: debian/clearwater-sip-perf.install
cp --recursive clearwater-sip-perf.root/* %{buildroot}/

%files
%{_unitdir}/sprout.service
/lib/systemd/scripts/sprout.sh
/usr/share/clearwater/bin/sprout
/usr/share/clearwater/bin/poll_sprout_http.sh
/usr/share/clearwater/bin/poll_sprout_sip.sh
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/enum_schema.json
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/rph_schema.json
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/rph_validation.py*
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/scscf_schema.json
/usr/share/clearwater/clearwater-diags-monitor/scripts/sprout_base_diags
/usr/share/clearwater/infrastructure/alarms/sprout_alarms.json
/usr/share/clearwater/infrastructure/monit_stability/sprout-stability
/usr/share/clearwater/infrastructure/monit_uptime/check-sprout-uptime
/usr/share/clearwater/infrastructure/scripts/reload/fallback_ifcs_xml/sprout_reload
/usr/share/clearwater/infrastructure/scripts/reload/memcached/sprout_reload
/usr/share/clearwater/infrastructure/scripts/reload/shared_ifcs_xml/sprout_reload
/usr/share/clearwater/infrastructure/scripts/restart/sprout_restart
/usr/share/clearwater/infrastructure/scripts/create-analytics-syslog-config
/usr/share/clearwater/infrastructure/scripts/create-sprout-nginx-config
/usr/share/clearwater/infrastructure/scripts/sprout.monit
/usr/share/clearwater/node_type.d/20_sprout
/usr/share/clearwater/clearwater-config-manager/plugins/sprout_json_plugin.py*
/usr/share/clearwater/clearwater-config-manager/plugins/sprout_scscf_json_plugin.py*
/usr/share/clearwater/clearwater-config-manager/plugins/sprout_enum_json_plugin.py*
/usr/share/clearwater/clearwater-config-manager/plugins/sprout_rph_json_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/scscf_json_config_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/enum_json_config_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/rph_json_config_plugin.py*
%config /etc/clearwater/logging/sprout
%config /etc/logrotate.d/sproutanalytics
%config /etc/security/limits.conf.sprout
%config /etc/cron.hourly/sprout-log-cleanup

%files libs
/usr/share/clearwater/sprout/lib/

%files plugin-scscf
/usr/share/clearwater/sprout/plugins/sprout_scscf.so
/usr/share/clearwater/clearwater-config-manager/plugins/shared_ifcs_xml_plugin.py*
/usr/share/clearwater/clearwater-config-manager/plugins/fallback_ifcs_xml_plugin.py*
/usr/share/clearwater/clearwater-config-manager/scripts/remove_shared_ifcs_xml
/usr/share/clearwater/clearwater-config-manager/scripts/remove_fallback_ifcs_xml
/usr/share/clearwater/clearwater-config-manager/scripts/validate_shared_ifcs_xml
/usr/share/clearwater/clearwater-config-manager/scripts/validate_fallback_ifcs_xml
/usr/share/clearwater/clearwater-config-manager/scripts/display_shared_ifcs
/usr/share/clearwater/clearwater-config-manager/scripts/display_fallback_ifcs
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/
/usr/share/clearwater/clearwater-config-access/plugins/shared_ifcs_config_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/fallback_ifcs_config_plugin.py*

%files plugin-icscf
/usr/share/clearwater/sprout/plugins/sprout_icscf.so

%files plugin-bgcf
/usr/share/clearwater/sprout/plugins/sprout_bgcf.so
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/bgcf_schema.json
/usr/share/clearwater/clearwater-config-manager/scripts/print-bgcf-configuration
/usr/share/clearwater/clearwater-config-manager/scripts/upload_bgcf_json
/usr/share/clearwater/clearwater-config-manager/plugins/sprout_bgcf_json_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/bgcf_json_config_plugin.py*

%files as-plugin-mmtel
/usr/share/clearwater/sprout/plugins/sprout_mmtel_as.so
/usr/share/clearwater/clearwater-diags-monitor/scripts/sprout_mmtel_as_diags

%files as-plugin-gemini
/usr/share/clearwater/sprout/plugins/gemini-as.so

%files as-plugin-memento
/usr/share/clearwater/sprout/plugins/memento-as.so
/usr/share/clearwater/infrastructure/alarms/memento_as_alarms.json

%files as-plugin-call-diversion
/usr/share/clearwater/sprout/plugins/call-diversion-as.so

%files as-plugin-mangelwurzel
/usr/share/clearwater/sprout/plugins/mangelwurzel-as.so

%files -n clearwater-bono
%{_unitdir}/bono.service
/lib/systemd/scripts/bono.sh
/usr/share/clearwater/bin/bono
/usr/share/clearwater/bin/poll_bono.sh
/usr/share/clearwater/clearwater-diags-monitor/scripts/bono_diags
/usr/share/clearwater/infrastructure/scripts/restart/bono_restart
/usr/share/clearwater/infrastructure/scripts/bono.monit
/usr/share/clearwater/node_type.d/20_bono
%config /etc/clearwater/logging/bono
%config /etc/security/limits.conf.bono
%config /etc/cron.hourly/bono-log-cleanup

%files -n clearwater-restund
%{_unitdir}/restund.service
/lib/systemd/scripts/restund.sh
/usr/share/clearwater/bin/restund
/usr/share/clearwater/restund/lib/
/usr/share/clearwater/bin/poll_restund.sh
/usr/share/clearwater/infrastructure/scripts/restund
%config /etc/security/limits.conf.restund

%files -n clearwater-sipp
/etc/sysctl.conf.clearwater-sipp
/usr/share/clearwater/bin/sipp

%files -n clearwater-sip-stress
%{_unitdir}/clearwater-sip-stress.service
/lib/systemd/scripts/clearwater-sip-stress.sh
/etc/cron.hourly/clearwater-sip-stress-log-cleanup
/usr/share/clearwater/bin/sip-stress
/usr/share/clearwater/infrastructure/scripts/sip-stress
/usr/share/clearwater/sip-stress/sip-stress.xml

%files -n clearwater-sip-stress-stats
%{_unitdir}/clearwater-sip-stress-stats.service
/lib/systemd/scripts/clearwater-sip-stress-stats.sh
/usr/share/clearwater/gems/clearwater-sipp-stats-*.gem

%files -n clearwater-sip-perf
%{_unitdir}/clearwater-sip-perf.service
/lib/systemd/scripts/clearwater-sip-perf.sh
/usr/share/clearwater/bin/sip-perf
/usr/share/clearwater/infrastructure/scripts/sip-perf
/usr/share/clearwater/sip-perf/sip-perf.xml

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/sprout-base.postinst
cw-create-user sprout
cw-create-log-dir sprout
cw-add-security-limits sprout
cw-start sprout
%systemd_post sprout.service

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/sprout-base.prerm
%systemd_preun sprout.service
cw-stop sprout
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user sprout
  cw-remove-log-dir sprout
  cw-remove-run-dir sprout
fi
cw-remove-security-limits sprout

%postun
%systemd_postun_with_restart sprout.service

%post plugin-scscf
# See: debian/scsf-bgcf.links
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/validate_shared_ifcs_xml /usr/bin/cw-validate_shared_ifcs_xml
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/validate_fallback_ifcs_xml /usr/bin/cw-validate_fallback_ifcs_xml
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/display_shared_ifcs /usr/bin/cw-display_shared_ifcs
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/display_fallback_ifcs /usr/bin/cw-display_fallback_ifcs
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/remove_shared_ifcs_xml /usr/sbin/cw-remove_shared_ifcs_xml
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/remove_fallback_ifcs_xml /usr/sbin/cw-remove_fallback_ifcs_xml

%preun plugin-scscf
rm --force /usr/bin/cw-validate_shared_ifcs_xml
rm --force /usr/bin/cw-validate_fallback_ifcs_xml
rm --force /usr/bin/cw-display_shared_ifcs
rm --force /usr/bin/cw-display_fallback_ifcs
rm --force /usr/sbin/cw-remove_shared_ifcs_xml
rm --force /usr/sbin/cw-remove_fallback_ifcs_xml

%post plugin-bgcf
# See: debian/sprout-bgcf.links
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/upload_bgcf_json /usr/bin/cw-upload_bgcf_json

%preun plugin-bgcf
rm --force /usr/bin/cw-upload_bgcf_json

%post -n clearwater-bono -p /bin/bash
%include %{SOURCE1}
# See: debian/bono.postinst
cw-create-user bono
cw-create-log-dir bono
cw-add-security-limits bono
cw-start bono
%systemd_post bono.service

%preun -n clearwater-bono -p /bin/bash
%include %{SOURCE1}
# See: debian/bono.prerm
%systemd_preun bono.service
cw-stop bono
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user bono
  cw-remove-log-dir bono
  cw-remove-run-dir bono
fi
cw-remove-security-limits bono

%postun -n clearwater-bono
%systemd_postun_with_restart bono.service

%post -n clearwater-restund -p /bin/bash
%include %{SOURCE1}
# See: debian/restund.postinst
cw-create-user restund
cw-create-log-dir restund
cw-add-security-limits restund
cw-start restund
%systemd_post restund.service

%preun -n clearwater-restund -p /bin/bash
%include %{SOURCE1}
# See: debian/restund.prerm
%systemd_preun restund.service
cw-stop restund
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user restund
  cw-remove-log-dir restund
  cw-remove-run-dir restund
fi
cw-remove-security-limits restund

%postun -n clearwater-restund
%systemd_postun_with_restart restund.service

%post -n clearwater-sip-stress -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-sip-stress.postinst
/usr/share/clearwater/infrastructure/scripts/sip-stress
service-action clearwater-sip-stress start
%systemd_post clearwater-sip-stress.service

%preun -n clearwater-sip-stress
%systemd_preun clearwater-sip-stress.service

%postun -n clearwater-sip-stress
%systemd_postun_with_restart clearwater-sip-stress.service

%post -n clearwater-sip-stress-stats -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-sip-stress-stats.postinst
gem install /usr/share/clearwater/gems/clearwater-sipp-stats-1.0.0.gem --no-ri --no-rdoc
service-action clearwater-sip-stress-stats start
%systemd_post clearwater-sip-stress-stats.service

%preun -n clearwater-sip-stress-stats
%systemd_preun clearwater-sip-stress-stats.service

%postun -n clearwater-sip-stress-stats
%systemd_postun_with_restart clearwater-sip-stress-stats.service

%post -n clearwater-sip-perf -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-sip-perf.postinst
/usr/share/clearwater/infrastructure/scripts/sip-perf
%systemd_post clearwater-sip-perf.service

%preun -n clearwater-sip-perf
%systemd_preun clearwater-sip-perf.service

%postun -n clearwater-sip-perf
%systemd_postun_with_restart clearwater-sip-perf.service
