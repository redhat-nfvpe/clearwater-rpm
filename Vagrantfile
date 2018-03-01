# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "centos/7"
  config.vm.synced_folder ".", "/home/vagrant/host"

  config.vm.provider "virtualbox" do |virtualbox, override|
    virtualbox.memory = 4096
    virtualbox.cpus = 4
  end

end
