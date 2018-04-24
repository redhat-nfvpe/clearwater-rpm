Deploy Clearwater on OpenStack Using Ansible
============================================

The playbook is under `scripts/deploy`. It can be easily adapted to support other clouds and also
bare metal deployments. Tested with Ansible 2.5.

First, install Ansible and the requirements for the modules we will use. The least intrusive way is
to use a Python virtualenv. You will also need SELinux extensions for Python. On Fedora:

    sudo dnf install python3-virtualenv libselinux-python3
    virtualenv --system-site-packages env
    . env/bin/activate
    pip install --requirement requirements.txt

Then, you will need to create a
`clouds.yaml` file
([documentation](https://docs.openstack.org/python-openstackclient/pike/configuration/)).
You can use `clouds.yaml.sample` as a template for deploying on Rackspace. For Rackspace you will
also need:

    pip install rackspaceauth

Next, you will need to create a `vars/topology.yaml` file, using `vars/topology.yaml.sample` as a
template. Multiple deployments in the same zone should each have their own unique `site_name`, and
each will get its own keypair with that name. In this file you can also choose the OpenStack image
and flavors to use per server. (See Rackspace
[flavors](https://developer.rackspace.com/docs/cloud-servers/v2/general-api-info/flavors/)).

You can now deploy Clearwater:

    ansible-playbook deploy.yaml

The play will provision a keypair for you and write the private and public (`.pub`) key files in
`keys/`. Note that the private key cannot be retrieved after creation, so make sure not to lose
these files. The play will then provision the servers and install the necessary packages on them.

It is safe and useful to replay the playbook, for example if you add additional nodes in
`topology.yaml`.

To manually login to the servers use the private key and disable host key checking (something you
always want to do when dealing we cloud IP addresses, which might be reused), for example:

    ssh -i keys/clearwater-1-example-org -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@192.237.176.164


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
5. sprout (sip router) - requires homestead, ralf is optional
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


sudo htpasswd /etc/nagios/passwd nagiosadmin
