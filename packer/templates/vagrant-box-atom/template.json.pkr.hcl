packer {
  required_plugins {
    ansible = {
      source  = "github.com/hashicorp/ansible"
      version = "~> 1"
    }
    vagrant = {
      source  = "github.com/hashicorp/vagrant"
      version = "~> 1"
    }
    virtualbox = {
      source  = "github.com/hashicorp/virtualbox"
      version = "~> 1"
    }
  }
}

source "virtualbox-ovf" "ubuntu" {
  headless         = "true"
  shutdown_command = "echo 'vagrant' | sudo -S shutdown -P now"
  source_path      = "../../builds/virtualbox/vagrant-base-ubuntu-20.04-amd64/vagrant-base-ubuntu-20.04-amd64.ovf"
  ssh_password     = "vagrant"
  ssh_username     = "vagrant"
  ssh_wait_timeout = "30s"
}

build {
  sources = [
    "source.virtualbox-ovf.ubuntu"
  ]

  provisioner "shell" {
    execute_command = "echo 'vagrant'|{{ .Vars }} sudo -S -E bash '{{ .Path }}'"
    scripts         = [
      "../../scripts/ubuntu/ansible.sh"
    ]
  }

  provisioner "ansible-local" {
    extra_arguments = [
      "--extra-vars=@./host_vars/all"
    ]
    galaxy_file     = "requirements.yml"
    host_vars       = "./provisioning/host_vars/"
    playbook_file   = "./provisioning/singlenode.yml"
  }

  provisioner "shell" {
    execute_command = "echo 'vagrant'|{{ .Vars }} sudo -S -E bash '{{ .Path }}'"
    scripts         = [
      "../../scripts/ubuntu/cleanup.sh",
      "../../scripts/common/minimize.sh"
    ]
  }

  post-processor "vagrant" {
    output               = "../../builds/{{ .Provider }}/vagrant-atom.box"
    vagrantfile_template = "./Vagrantfile"
  }
}
