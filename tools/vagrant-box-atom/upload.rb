#!/usr/bin/env ruby

require 'bundler/setup'
require 'net/http'
require 'vagrant_cloud'

ORG = 'artefactual'
BOX = 'atom'
PROVIDER = 'virtualbox'

path = ARGV[0]
token = ARGV[1]
version = ARGV[2]
description = ARGV[3]

client = VagrantCloud::Client.new(access_token: token)

client.box_version_create(
    username: ORG,
    name: BOX,
    version: version,
    description: description
)

client.box_version_provider_create(
    username: ORG,
    name: BOX,
    version: version,
    provider: PROVIDER
)

upload_url = client.box_version_provider_upload(
    username: ORG,
    name: BOX,
    version: version,
    provider: PROVIDER
)

uri = URI.parse(upload_url[:upload_path])
request = Net::HTTP::Put.new(uri)
box = File.open(path, 'rb')
request.set_form([['file', box]], 'multipart/form-data')
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
        name: BOX,
        version: version,
    )
else
    abort('ABORTED! Vagrant box could not be uploaded.')
end
