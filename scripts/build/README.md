How to Build Clearwater RPMs
============================

The build scripts are all under `scripts/build`.

First run `fetch-sources` to download the sources and archive them in the `SOURCES` directory. (Note:
we must use git to fetch them, because the repositories are designed with many git submodules,
which are not packaged in GitHub's release tarballs. Also note that these submodules are tied to
specific commits, which unfortunately do not match their git release tags. In short, this is the
only way to get the correct and complete source tarball.)

You then have a few options for building the RPMs:

1. Are you on CentOS or RHEL? Then run `scripts/build/build`. (The requirements are documented in the
   scripts.) Note that the more CPU threads you have, the more RAM you will need. 8 GB of RAM
   seems to be enough for a 12 thread machine. 
2. Or, use our included [Vagrant](https://www.vagrantup.com/) configuration to quickly bring up a
   CentOS virtual machine. Run `vagrant up`, and then `vagrant ssh` to login. The directories are
   conveniently shared with the host operating system. (Note that you may need the VirtualBox Guest
   Additions. Install them automatically via a plugin: `vagrant plugin install vagrant-vbguest`.)
3. On other Linuxes, use [mock](https://github.com/rpm-software-management/mock) to emulate CentOS
   in a chroot environment. For this, run `scripts/build/mock-build`. Note that mock will use up a lot of
   space in `/var/lib/mock` while running, so you may want to mount that directory somewhere spacious.
   Also see
   [here](https://marcin.juszkiewicz.com.pl/2016/04/15/how-to-speed-up-mock/) and
   [here](http://miroslav.suchy.cz/blog/archives/2015/05/28/increase_mock_performance_-_build_packages_in_memory/index.html)
   for some tips to speed up mock.

Once the build process starts, go make yourself a cup of tea, because it's going to take a while
(25 minutes on a 6-core workstation). Though the Clearwater build scripts are not very friendly to
concurrency (`make --jobs`) we've enabled concurrent builds in the sub-modules, and that has helped
a lot (cut down from 60 minutes).

When finished (phew!) your RPMs will be available under `RPMS/x86_64`.

You can also build individual spec files by providing the name as an argument, for example:
`build-rpms clearwater-ellis`.

Also useful may be the `validate-install` script, which skips the `%prepare` and `%build` sections in the
spec file.

All scripts capture their output into log files into the `logs` directory. If you're using mock
there will be extra logs under `RPMS/x86_64`.
