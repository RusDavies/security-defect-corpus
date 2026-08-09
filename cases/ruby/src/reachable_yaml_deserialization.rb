# RUBY-YAML-DESER-001 reachable vulnerable fixture. DO NOT DEPLOY.
require 'yaml'

def load_job(payload)
  YAML.load(payload)
end
