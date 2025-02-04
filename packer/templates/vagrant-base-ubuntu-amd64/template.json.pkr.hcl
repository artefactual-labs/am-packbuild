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
  default = "file:https://releases.ubuntu.com/20.04/SHA256SUMS"
}

variable "memory" {
  type    = string
  default = "4096"
}

variable "no_proxy" {
  type    = string
  default = "${env("no_proxy")}"
}

variable "vm_name" {
  type    = string
  default = "vagrant-base-ubuntu-amd64"
}

variable "iso_url" {
  type    = string
  default = "https://www.releases.ubuntu.com/20.04/ubuntu-20.04.6-live-server-amd64.iso"
}

variable "boot_command" {
  type    = list(string)
  default = [
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
}

variable "http_directory" {
  type    = string
  default = "../../http/ubuntu-cloud-init"
}

variable "output_directory" {
  type    = string
  default = "../../builds/virtualbox/vagrant-base-ubuntu-amd64"
}

variable "boot_wait" {
  type    = string
  default = "5s"
}

source "virtualbox-iso" "ubuntu" {
  boot_command            = "${var.boot_command}"
  boot_wait               = "${var.boot_wait}"
  disk_size               = "${var.disk_size}"
  guest_os_type           = "Ubuntu_64"
  hard_drive_interface    = "sata"
  headless                = "${var.headless}"
  http_directory          = "${var.http_directory}"
  iso_checksum            = "${var.iso_checksum}"
  iso_url                 = "${var.iso_url}"
  output_directory        = "${var.output_directory}"
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
  vm_name                 = "${var.vm_name}"
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
