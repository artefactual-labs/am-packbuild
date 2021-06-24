# AtoM Vagrant box upload

Ruby script to release a new Vagrant box version in Vagrant Cloud.

## Requirements

[Ruby](https://www.ruby-lang.org/) and [Bundler](https://bundler.io/).

## Usage

Install the dependencies:

    bundle install

Command synopsis:

    ./upload.rb [BOX] [PATH] [VAGRANT_CLOUD_ACCESS_TOKEN] [VERSION] [DESCRIPTION]

All arguments are required:

* `BOX`: use `archivematica` or `atom`,
* `PATH`: path to the box to be uploaded,
* `VAGRANT_CLOUD_ACCESS_TOKEN`: see [authentication tokens] for more details,
* `VERSION`: see [box versioning] for more details, and
* `DESCRIPTION`: a description of the box.

Full example:

    bundle install
    ./upload.rb \
        atom
        /path/to/atom-vagrant-2.7.0.2.box \
        vagrant_cloud_access_token \
        2.7.0.2 \
        'AtoM qa/2.x on Ubuntu 20.04.<br/><br/>Add PHP PCOV extension.'


[authentication tokens]: https://www.vagrantup.com/vagrant-cloud/users/authentication#authentication-tokens
[box versioning]: https://www.vagrantup.com/docs/boxes/versioning
