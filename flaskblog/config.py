

class Config:
    SECRET_KEY = '1f025c0224c27773ed0cce1a3dde7520'
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    MAIL_SERVER='smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = '525b5783b2187a'
    MAIL_PASSWORD = '5815d71bb0ebc3'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    DEBUG_TB_ENABLED= True
    DEBUG_TB_INTERCEPT_REDIRECTS = False