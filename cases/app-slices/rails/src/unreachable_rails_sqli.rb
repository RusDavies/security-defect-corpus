# APP-RAILS-SQLI-001 unreachable/safe paired fixture.
class UsersController
  def retired_index
    User.where("email = '#{params[:email]}'")
  end

  def index
    User.where(email: params[:email].to_s)
  end
end
