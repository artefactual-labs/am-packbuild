packer {
  required_plugins {
    virtualbox = {
      source  = "github.com/hashicorp/virtualbox"
      version = "~> 1"
    }
  }
}

variable "cpus" {
  type    = string
  default = "2"
}

variable "disk_size" {
  type    = string
  default = "30720"
}

variable "headless" {
  type    = string
  default = "true"
}

variable "http_proxy" {
  type    = string
  default = "${env("http_proxy")}"
}

variable "https_proxy" {
  type    = string
  default = "${env("https_proxy")}"
}

variable "iso_checksum" {
  type    = string
  default = "b8f31413336b9393ad5d8ef0282717b2ab19f007df2e9ed5196c13d8f9153c8b"
}

variable "memory" {
  type    = string
  default = "4096"
}

variable "no_proxy" {
  type    = string
  default = "${env("no_proxy")}"
}

variable "template" {
  type    = string
  default = "vagrant-base-ubuntu-20.04-amd64"
}

source "virtualbox-iso" "ubuntu" {
  boot_command            = [
    # Display language menu.
    "<wait><enter><wait>",
    # Select English.
    "<enter><wait>",
    # Select "Other Options".
    "<f6><wait>",
    # Close "Expert mode" menu.
    "<esc><wait>",
    # Set the source URL for autoinstallation.
    " autoinstall ds=nocloud-net;seedfrom=http://{{ .HTTPIP }}:{{ .HTTPPort }}/",
    # Boot.
    "<enter><wait>"
  ]
  boot_wait               = "5s"
  disk_size               = "${var.disk_size}"
  guest_os_type           = "Ubuntu_64"
  hard_drive_interface    = "sata"
  headless                = "${var.headless}"
  http_directory          = "../../http/ubuntu-cloud-init"
  iso_checksum            = "${var.iso_checksum}"
  iso_urls                = [
    "iso/ubuntu-20.04.6-live-server-amd64.iso",
    "https://www.releases.ubuntu.com/20.04/ubuntu-20.04.6-live-server-amd64.iso"
  ]
  output_directory        = "../../builds/virtualbox/vagrant-base-ubuntu-20.04-amd64"
  shutdown_command        = "echo 'vagrant' | sudo -S shutdown -P now"
  ssh_password            = "vagrant"
  ssh_port                = 22
  ssh_username            = "vagrant"
  ssh_timeout             = "10000s"
  vboxmanage              = [
    ["modifyvm", "{{ .Name }}", "--memory", "${var.memory}"],
    ["modifyvm", "{{ .Name }}", "--cpus", "${var.cpus}"]
  ]
  virtualbox_version_file = ".vbox_version"
  vm_name                 = "${var.template}"
}

build {
  sources = [
    "source.virtualbox-iso.ubuntu"
  ]

  provisioner "shell" {
    environment_vars  = [
      "HOME_DIR=/home/vagrant",
      "http_proxy=${var.http_proxy}",
      "https_proxy=${var.https_proxy}",
      "no_proxy=${var.no_proxy}"
    ]
    execute_command   = "echo 'vagrant' | {{ .Vars }} sudo -S -E sh -eux '{{ .Path }}'"
    expect_disconnect = true
    scripts           = [
      "../../scripts/ubuntu/update.sh",
      "../../scripts/common/sshd.sh",
      "../../scripts/ubuntu/networking.sh",
      "../../scripts/ubuntu/sudoers.sh",
      "../../scripts/ubuntu/vagrant.sh",
      "../../scripts/common/virtualbox.sh",
      "../../scripts/ubuntu/cleanup.sh",
      "../../scripts/common/minimize.sh"
    ]
  }

}
