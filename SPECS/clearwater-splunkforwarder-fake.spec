Name:          clearwater-splunkforwarder-fake
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/clearwater-logging

%global debug_package %{nil}

Summary:       Clearwater - Fake Splunk Forwarder
AutoReq:       no

%description
Fake Splunk Forwarder

%install
mkdir --parents %{buildroot}/opt/splunkforwarder/bin/
mkdir --parents %{buildroot}/opt/splunkforwarder/etc/apps/search/local/
mkdir --parents %{buildroot}/opt/splunkforwarder/etc/system/local/
touch %{buildroot}/opt/splunkforwarder/bin/splunk
touch %{buildroot}/opt/splunkforwarder/etc/apps/search/local/inputs.conf
touch %{buildroot}/opt/splunkforwarder/etc/apps/search/local/outputs.conf
touch %{buildroot}/opt/splunkforwarder/etc/system/local/outputs.conf
chmod +x %{buildroot}/opt/splunkforwarder/bin/splunk

%files
/opt/splunkforwarder/
