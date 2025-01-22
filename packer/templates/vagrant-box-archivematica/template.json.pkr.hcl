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

variable "mirror" {
  type    = string
  default = "http://releases.ubuntu.com"
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
      "../../scripts/ubuntu/ansible-focal.sh"
    ]
  }

  provisioner "ansible-local" {
    galaxy_file      = "requirements.yml"
    group_vars       = "./provisioning/group_vars/"
    inventory_groups = [
      "servers"
    ]
    playbook_file    = "./provisioning/singlenode.yml"
  }

  provisioner "shell" {
    execute_command = "echo 'vagrant'|{{ .Vars }} sudo -S -E bash '{{ .Path }}'"
    scripts         = [
      "./motd.sh",
      "../../scripts/ubuntu/cleanup.sh",
      "../../scripts/common/minimize.sh"
    ]
  }

  post-processor "vagrant" {
    output               = "../../builds/{{ .Provider }}/vagrant-am.box"
    vagrantfile_template = "./Vagrantfile"
  }
}
