Deploy Clearwater on OpenStack Using Ansible
============================================

First, install Ansible and the requirements for the modules we will use. The least intrusive way is
to use a Python virtualenv. You will also need SELinux extensions for Python. On Fedora:

    sudo dnf install python3-virtualenv libselinux-python3
    virtualenv --system-site-packages env
    . env/bin/activate
    pip install --requirement requirements.txt

Then, you will need to create a
`clouds.yaml` file
([documentation](https://docs.openstack.org/python-openstackclient/pike/configuration/)).
You can use `clouds.yaml.sample` as an template for deploying on Rackspace. For Rackspace you will
also need:

    pip install rackspaceauth

Finally, you will need to create a `topology.yaml`  file, using `topology.yaml.sample` as a template. The
`prefix` will be prepended to all your server names, and will also be used as the keypair name.
You can choose different prefixes to support multiple deployments.
You can also choose the OpenStack image and flavors to use per server. (See Rackspace
[flavors](https://developer.rackspace.com/docs/cloud-servers/v2/general-api-info/flavors/)).

You can now deploy Clearwater:

    ansible-playbook deploy.yaml

The playbook will create a keypair for you and write keys to `.key` and `.pub` files. Note that the
private key cannot be retrieved after creation, so make sure not to lose the private key file.


TODO
----

Because there are so many interdependencies, it's best to put the RPMs in a repository. The
`install-local-repository` script will do it locally, using the filesystem. Make sure to re-run it if you
rebuild any of the RPMs. You can then use `yum install` for any of the components, e.g.
`yum install clearwater-sprout`.

### Required

*Before* installing any Clearwater component, make sure you have `/etc/clearwater/local_config` and
`/etc/clearwater/shared_config`. The clearwater-auto-config-* packages come with templates for these
files.

nodes:

1. vellum (cassandra storage + memcached with astaire/rogers)
2. chronos (timer)
3. smtp
4. bono (sip edge proxy)
5. sprout (sip router)
6. homestead (hss cache)
7. ralf (ctf)
8. homer (xdms)
9. ellis (provisioning on mysql)

all of them have:

infrastructure (configuration scripts)
monit (monitors and restarts services)
etcd (cluster manager, at least 3 nodes must be masters, first node must be master)

phase 1: provision

provision all VMs, get their public IP address and append to a file

phase 2: configure

on each VM:

update hostname: sprout-<site name>-<zone>
update /etc/hosts
create /etc/clearwater/local_config
create /etc/clearwater/shared_config

phase 3: install

on each VM:

install RPMs

https://blog.cloudandheat.com/index.php/en/2017/09/01/manage-openstack-vms-with-ansible/
https://github.com/msolberg/openstack-ansible-demo/tree/master/tutorial
https://dmsimard.com/2016/01/08/selinux-python-virtualenv-chroot-and-ansible-dont-play-nice/
