iso_url      = "https://www.releases.ubuntu.com/20.04/ubuntu-20.04.6-live-server-amd64.iso"
iso_checksum = "file:https://releases.ubuntu.com/20.04/SHA256SUMS"
boot_command = [
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
