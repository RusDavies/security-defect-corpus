# APP-RAILS-SQLI-001 reachable vulnerable fixture. DO NOT DEPLOY.
class UsersController
  def index
    User.where("email = '#{params[:email]}'")
  end
end
