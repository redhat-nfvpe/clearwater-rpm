Name:          clearwater-logging
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/clearwater-logging
BuildRequires: git, rsync

Summary: Clearwater - Logging

%description
Common logging infrastructure

%prep
if [ ! -d clearwater-logging ]; then
  git config --global url."https://github.com/".insteadOf git@github.com:
  git clone --depth 1 --recursive --branch release-%{version} git@github.com:Metaswitch/clearwater-logging.git
fi

%install
cd %{_builddir}/clearwater-logging

# See: debian/clearwater-logging.install
rsync --recursive clearwater-logging/* %{buildroot}/

%files
/
