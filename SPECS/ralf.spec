Name:          clearwater-ralf
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/ralf
BuildRequires: git, rsync, make, cmake, libtool, gcc-c++, bison, flex
BuildRequires: zeromq-devel, lksctp-tools-devel, gnutls-devel, libidn-devel

# Note: zeromq-devel requires epel-release

Summary: Clearwater - Ralf

%description
CTF

%prep
if [ ! -d ralf ]; then
  git config --global url."https://github.com/".insteadOf git@github.com:
  git clone --depth 1 --recursive --branch release-%{version} git@github.com:Metaswitch/ralf.git
fi

%install
cd %{_builddir}/ralf

# Note: the modules must be built in order, so unfortunately we can't use --jobs/-J
make

# See: debian/ralf.install
mkdir --parents %{buildroot}/usr/share/clearwater/bin/
rsync build/bin/ralf %{buildroot}/usr/share/clearwater/bin/
rsync --recursive ralf.root/* %{buildroot}/

%files
/
