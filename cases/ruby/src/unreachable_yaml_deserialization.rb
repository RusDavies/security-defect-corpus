# RUBY-YAML-DESER-001 unreachable/safe paired fixture.
require 'yaml'

def retired_load_job(payload)
  YAML.load(payload)
end

def load_job(payload)
  YAML.safe_load(payload, permitted_classes: [], aliases: false)
end
