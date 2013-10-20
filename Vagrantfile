# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  ## Use Ubunute 12.04 (64)
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.provider :virtualbox do |vb|
    # Limit VM to 1024 mb memory
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end

  config.ssh.forward_agent = true

  ## For masterless, mount your salt file root
  config.vm.synced_folder "srv/", "/srv/"

  ## Use salt as our provisioner.
  config.vm.provision :salt do |salt|
    salt.minion_config = "srv/minion"
    salt.run_highstate = true
    salt.verbose = true
  end
end