#!/usr/bin/env ruby

require 'bundler/setup'
require 'net/http'
require 'vagrant_cloud'

ORG = 'artefactual'
PROVIDER = 'virtualbox'

if ARGV.length != 5
    abort("USAGE: ./upload.rb [BOX] [PATH] [VAGRANT_CLOUD_ACCESS_TOKEN] [VERSION] [DESCRIPTION]")
end

box = ARGV[0]
path = ARGV[1]
token = ARGV[2]
version = ARGV[3]
description = ARGV[4]

client = VagrantCloud::Client.new(access_token: token)

client.box_version_create(
    username: ORG,
    name: box,
    version: version,
    description: description
)

client.box_version_provider_create(
    username: ORG,
    name: box,
    version: version,
    provider: PROVIDER
)

upload_url = client.box_version_provider_upload(
    username: ORG,
    name: box,
    version: version,
    provider: PROVIDER
)

uri = URI.parse(upload_url[:upload_path])
request = Net::HTTP::Put.new(uri)
box_file = File.open(path, 'rb')
request.set_form([['file', box_file]], 'multipart/form-data')
response = Net::HTTP.start(
    uri.hostname,
    uri.port,
    use_ssl: uri.scheme.eql?('https')
) do |http|
    http.request(request)
end

if response.is_a?(Net::HTTPSuccess)
    client.box_version_release(
        username: ORG,
        name: box,
        version: version,
    )
else
    abort('ABORTED! Vagrant box could not be uploaded.')
end
