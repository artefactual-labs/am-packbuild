iso_url      = "https://www.releases.ubuntu.com/24.04/ubuntu-24.04.1-live-server-amd64.iso"
iso_checksum = "file:https://releases.ubuntu.com/24.04/SHA256SUMS"
boot_command = [
    # Edit the boot command.
    "e<wait2>",
    # Look for the kernel line.
    "<down><down><down><wait2>",
    # Go to the end of the line.
    "<end><wait>",
    # Set the source URL for autoinstallation.
    " autoinstall ds=nocloud-net\\;s=http://{{ .HTTPIP }}:{{ .HTTPPort }}/<wait>",
    # Boot.
    "<f10>"
]
