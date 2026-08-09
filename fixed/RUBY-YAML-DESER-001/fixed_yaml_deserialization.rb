# RUBY-YAML-DESER-001 fixed-version fixture for patch-diff evaluation.
require 'yaml'

def load_job(payload)
  YAML.safe_load(payload, permitted_classes: [], aliases: false)
end
