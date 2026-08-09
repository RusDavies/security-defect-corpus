# APP-RAILS-SQLI-001 fixed-version fixture for patch-diff evaluation.
class UsersController
  def index
    User.where(email: params[:email].to_s)
  end
end
