Build Architecture
==================

Each RPM spec is devoted to a single git repository and most generate several RPMs.

A crucial build architecture decision is a preference to include and build specific versions of
upstream C/C++ libraries rather than use those packaged for the operating system. It adds much
complexity to the build process, but it does ensure runtime consistency, though at the cost of
losing security fixes provided by the operating system, which could lead to worse stability. This
preference is applied inconsistently: e.g. Sprout builds its own libcurl, while Ralf/Homestead use
the operating system's.

Note that these upstream libraries have diverse open source licenses, and some are normally not
compatible with the GPL license. However, Clearwater's
[license](http://www.projectclearwater.org/download/license/) includes a "Special Exception" for
OpenSSL's license.

Another quirk of the repository design is the use of git submodules, for both the upstream libraries
mentioned above as well as Clearwater's modules, such as `cpp-common` and `cleatwater-etcd-modules`.
Unfortunately, we found that git tags (for versions) are not used consistently across all Clearwater
repositories, thus we make sure to use each repository with the exact commit hashes used for
all submodules. (Otherwise, there will be build errors.)


`clearwater-astaire`
--------------------

* `clearwater-astaire`
* `clearwater-rogers`


`clearwater-cassandra`
----------------------

* `clearwater-cassandra`


`clearwater-chronos`
--------------------

* `clearwater-chronos`


`clearwater-crest`
------------------

Note that Homestead itself has its own repository (see below).

* `clearwater-crest`
* `clearwater-crest-prov`
* `clearwater-homer`
* `clearwater-homer-cassandra`
* `clearwater-homestead-prov`
* `clearwater-homestead-prov-cassandra`


`clearwater-debian`
-------------------

* `clearwater-debian`


`clearwater-ellis`
------------------

* `clearwater-ellis`
* `clearwater-prov-tools`


`clearwater-etcd`
-----------------

There already is an effort in this repository to create RPMs.

* `clearwater-etcd`
* `clearwater-cluster-manager`
* `clearwater-queue-manager`
* `clearwater-config-manager`


`clearwater-homestead`
----------------------

* `clearwater-homestead`
* `clearwater-homestead-cassandra`


`clearwater-infrastructure`
---------------------------

Lots of miscellaneous packages.

* `clearwater-infrastructure`
* `clearwater-tcp-scalability`
* `clearwater-secure-connections`
* `clearwater-snmpd`
* `clearwater-socket-factory`
* `clearwater-auto-upgrade`
* `clearwater-radius-auth`
* `clearwater-log-cleanup`
* `clearwater-diags-monitor`
* `clearwater-auto-config-generic`
* `clearwater-auto-config-aws`
* `clearwater-auto-config-docker`


`clearwater-logging`
--------------------

* `clearwater-logging`


`clearwater-memento`
--------------------

* `clearwater-memento`
* `clearwater-memento-nginx`
* `clearwater-memento-cassandra`


`clearwater-monit`
------------------

* `clearwater-monit`


`clearwater-nginx`
------------------

* `clearwater-nginx`


`clearwater-ralf`
-----------------

Similar architecture to that of Homestead, but uses Diameter/Rf instead. The two repositories might
be better off combined.

* `clearwater-ralf`


`clearwater-splunkforwarder-fake`
---------------------------------

* `clearwater-splunkforwarder-fake`


`clearwater-sprout`
-------------------

Note that Memento itself has its own repository (see aboe).

* `clearwater-sprout`
* `clearwater-sprout-libs`
* `clearwater-bono`
* `clearwater-sprout-plugin-scscf`
* `clearwater-sprout-plugin-icscf`
* `clearwater-sprout-plugin-bgcf`
* `clearwater-sprout-as-plugin-mmtel`
* `clearwater-sprout-as-plugin-gemini`
* `clearwater-sprout-as-plugin-memento`
* `clearwater-sprout-as-plugin-call-diversion`
* `clearwater-sprout-as-plugin-mangelwurzel`
