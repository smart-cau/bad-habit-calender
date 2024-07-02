class Route:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    # import and register blueprints
    @app.route("/")
    def hello_world():
        return render_template("index.html")

    @app.route("/login")
    def login_page():
        return render_template("login.html")

    @app.route("/signup")
    def signup_page():
        return render_template("signup.html")
