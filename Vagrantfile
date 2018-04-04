# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "centos/7"
  config.vm.synced_folder "scripts", "/home/vagrant/scripts"
  config.vm.synced_folder "logs", "/home/vagrant/logs"
  config.vm.synced_folder "SPECS", "/home/vagrant/SPECS"
  config.vm.synced_folder "SOURCES", "/home/vagrant/SOURCES"
  config.vm.synced_folder "RPMS", "/home/vagrant/RPMS"
  config.vm.synced_folder "SRPMS", "/home/vagrant/SRPMS"
  config.vm.provision :shell, inline: "sudo yum install --assumeyes rpm-build yum-utils epel-release"

  config.vm.provider "virtualbox" do |virtualbox, override|
    virtualbox.memory = 2048
    virtualbox.cpus = 4
  end

end
