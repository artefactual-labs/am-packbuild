# AtoM Vagrant box upload

Ruby script to release a new AtoM Vagrant box version in Vagrant Cloud.

## Requirements

[Ruby](https://www.ruby-lang.org/) and [Bundler](https://bundler.io/).

## Usage

```
bundle install
ruby upload.rb \
  /path/to/atom-vagrant-2.7.0.2.box \
  vagrant_cloud_secret \
  2.7.0.2 \
  'AtoM qa/2.x on Ubuntu 20.04.<br/><br/>Add PHP PCOV extension.'
```
