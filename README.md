RPM Packaging for Clearwater IMS
================================

The [Clearwater IMS](https://www.projectclearwater.org/) is officially packaged for Ubuntu 14.04.
Here we are re-packaging it for RHEL, CentOS, and other RPM-based Linux distributions. We support
the x86_64 platform only.


How To
------

The build scripts are all under `scripts`.

First run `fetch-sources` to download the sources and archive them in the `SOURCES` directory.

You then have a few options for building the RPMs:

1. Are you on CentOS? Then just run `build-rpms`. (The requirements are documented in the script.)
2. On other Linuxes, use [mock](https://github.com/rpm-software-management/mock) to emulate CentOS
   in a chroot environment. The script is `mock-build-rpms`. (Note that mock will use up a lot of space
   in `/var/lib/mock` while running, so you may want to mount that directory somewhere spacious.)
3. Or, use our included [Vagrant](https://www.vagrantup.com/) configuration to quickly bring up a
   CentOS virtual machine. Just change to the `vagrant` directory and run `vagrant up`, and then
   `vagrant ssh` to login. The build scripts are in the `scripts` directory within the virtual machine.
   (Note that you will need the VirtualBox Guest Additions. Install them automatically via a plugin:
   `vagrant plugin install vagrant-vbguest`.)

When finished (phew!) your RPMs will be available under `RPMS/x86_64`.

You can also build individual spec files by providing the name as an argument, for example:
`build-rpms clearwater-ellis`.

Also useful may be the `validate-install` script, which skips the `%prepare` and `%build` sections in the
spec file.

All scripts capture their output into log files into `logs`. If you're using mock, there
will be extra logs under `RPMS/x86_64`.