RPM Packaging for Clearwater IMS
================================

The [Clearwater IMS](https://www.projectclearwater.org/) is officially packaged for Ubuntu 14.04.
Here we are re-packaging it for RHEL, CentOS, and other RPM-based Linux distributions. We support
the x86_64 platform only.


How To
------

You must use [CentOS](https://www.centos.org/) to build the RPMs. There are three ways to satisfy
this requirement:

1. Install CentOS yourself.
2. Use our included [Vagrant](https://www.vagrantup.com/) configuration to quickly bring up a CentOS
   virtual machine. Just change to this directory and run `vagrant up`, and then `vagrant ssh` to login.
3. On any Linux, use [mock](https://github.com/rpm-software-management/mock) to emulate CentOS in a
   chroot environment. For this, use `build-via-mock` instead of `build`.

From within CentOS, run `build`, and go make yourself a cup of tea, because it's going to take a
while. The process comprises cloning all the Clearwater git repositories for the specified
release tag, installing the build dependencies, building the code, and finally packaging the files
into RPMs.

When finished (phew!) your RPMs will be available under `RPMS/x86_64`.
