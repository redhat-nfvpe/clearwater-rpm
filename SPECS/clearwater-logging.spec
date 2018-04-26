Name:          clearwater-logging
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/clearwater-logging

Source0:       %{name}-%{version}.tar.bz2
Source1:       housekeeping.sh

%global debug_package %{nil}

Summary:       Clearwater - Logging
Requires:      nagios nagios-plugins nagios-selinux sysstat
Requires:      clearwater-splunkforwarder-fake
AutoReq:       no

%description
Common logging infrastructure

%prep
%setup

%install
# See: debian/clearwater-logging.install
cp --recursive clearwater-logging/* %{buildroot}/
mv %{buildroot}/etc/nagios3 %{buildroot}/etc/nagios

# Patch for Nagios 4
find %{buildroot} -type f -exec sed --in-place 's/nagios3/nagios/g' {} \;
find %{buildroot} -type f -exec sed --in-place 's/\/etc\/nagios\/resource.cfg/\/etc\/nagios\/private\/resource.cfg/g' {} \;
find %{buildroot} -type f -exec sed --in-place 's/\/var\/lib\/nagios\/spool\//\/var\/spool\/nagios\//g' {} \;

%files
/usr/lib/nagios/plugins/check_cpu_perf
/usr/lib/nagios/plugins/check_iftraffic_nrpe
%attr(755,-,-) /usr/share/clearwater/bin/clearwater-logging-update
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/clearwater-logging
/etc/nagios/clearwater/commands.cfg
/etc/nagios/clearwater/nagios.cfg
/opt/splunkforwarder/etc/apps/search/local/inputs.conf.clearwater
%ghost /etc/nagios/clearwater/nagios.cfg.preinst
%ghost /etc/nagios/clearwater/commands.cfg.preinst

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/postinst

# TODO: need to do more work for CentOS and Nagios 4 compatibility
#cp /etc/nagios/nagios.cfg /etc/nagios/clearwater/nagios.cfg.preinst
#cp /etc/nagios/clearwater/nagios.cfg /etc/nagios/nagios.cfg
#cp /etc/nagios/objects/commands.cfg /etc/nagios/clearwater/commands.cfg.preinst
#cp /etc/nagios/clearwater/commands.cfg /etc/nagios/objects/commands.cfg

touch /var/log/nagios/host-perfdata
touch /var/log/nagios/service-perfdata
chown nagios:nagios /var/log/nagios/host-perfdata
chown nagios:nagios /var/log/nagios/service-perfdata

service_action nagios restart

add_section () {
  local FILE=$1
  local NAME=$2
  local DELTA=$3
  {
    echo "#+$NAME"
    cat "$DELTA"
    echo "#-$NAME"
  } >> "$FILE"
}

add_section /opt/splunkforwarder/etc/apps/search/local/inputs.conf clearwater-logging /opt/splunkforwarder/etc/apps/search/local/inputs.conf.clearwater
/usr/share/clearwater/infrastructure/scripts/clearwater-logging
/opt/splunkforwarder/bin/splunk start --accept-license
/opt/splunkforwarder/bin/splunk enable boot-start
/usr/share/clearwater/bin/clearwater-logging-update

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/prerm
/opt/splunkforwarder/bin/splunk 
/opt/splunkforwarder/bin/splunk disable boot-start
/opt/splunkforwarder/bin/splunk stop

remove_section () {
  local FILE=$1
  local NAME=$2
  local TMP_FILE=$(mktemp)
  awk '/^#\+'$NAME'$/,/^#-'$NAME'$/ {next} {print}' "$FILE" > "$TMP_FILE"
  mv "$TMP_FILE" "$FILE"
}

remove_section /opt/splunkforwarder/etc/apps/search/local/inputs.conf clearwater-logging
remove_section /opt/splunkforwarder/etc/system/local/outputs.conf clearwater-logging

#mv /etc/nagios/clearwater/nagios.cfg.preinst /etc/nagios/nagios.cfg
#mv /etc/nagios/clearwater/commands.cfg.preinst /etc/nagios/commands.cfg

service_action nagios restart
