
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/msgapp'

#flask specific configuration
FLASK_CONFIG = {
    'SERVER_NAME': '0.0.0.0:8080',
    'DEBUG':True,
    'SECRET_KEY':'XAJS098hSJDNskGd567827',}


#Twilio test credentials
FROM = "+15005550006"
ASID = "ACde3d9f8915e7be40163284f38b02849b"
TOKEN = "9468671c1999c05c0e4af55bec5bdf6e"
#no retries in case of exception
RETRY = 5