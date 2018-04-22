Helper Packages
===============

You should never have to install these directly.


### `clearwater-crest`

A custom, extensible HTTP-RESTful interface to [Cassandra](http://cassandra.apache.org/) written in
Python 2, based on
[Zope](http://www.zope.org/)/[Cyclone](http://cyclone.io/)/[Twisted](https://twistedmatrix.com/).
Python code accesses cpp-common via [CFFI](https://cffi.readthedocs.io/).

### `clearwater-crest-prov`

### `clearwater-debian`

Clearwater's init scripts assume a Debian/LSB environment, which unfortunately diverges from
Red Hat's interpretation. Here we fill in the gaps.

### `clearwater-sprout-libs`

Shared libraries for Sprout and Bono.

### `clearwater-nginx`

[Nginx](https://www.nginx.com/) (as a dependency, not a fork) with Clearwater-specific
configurations.
