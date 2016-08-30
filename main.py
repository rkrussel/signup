import webapp2
import re
pageHead = """

<!DOCTYPE html>
<html>
    <head>
        <Title>User Sign Up</title>
        <style type="text/css">
            .error {
                color: red;
            }
        </style>
    </head
    <body>
"""
form = """
    <h1>User Sign-Up</h1>
    <form method="post">
    <label>User Name:  </label>
        <input type="text" name="username" value="%(un)s"><span class='error'>%(nn)s</span>
        <strong>%(nv)s</strong>
    <br>
    <br>
    <label>Password:  </label>
        <input type="Password" name="password" value="%(pw)s"><strong>%(pv)s</strong>
    <br>
    <br>
    <label>Verify password:  </label>
        <input type="Password" name="verify" value="%(ver)s"><strong>%(vv)s</strong>
    <br>
    <br>
    <label>Email:  </label>
        <input type="text" name="email" value="%(em)s"><strong>%(ie)s</strong>
    <br>
        <input type="submit">
    </form>
"""
pageFooter = """
</body>
</html>
"""

class Index(webapp2.RequestHandler):
    def get(self):
        response = pageHead + form % {"un": "",
                                      "pw": "",
                                      "ver": "",
                                      "em": "",
                                      "nn": "",
                                      "nv": "",
                                      "pv": "",
                                      "vv": "",
                                      "ie": ""} + pageFooter
        self.response.write(response)

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        noNameError = False
        invalidUser = False
        passMatch = False
        invalidPass = False
        invalidEmail = False
        if username == "":
            noNameError = True
        if not re.match("^[a-zA-Z0-9_-]{3,20}$", username):
            invalidUser = True
        if password != verify:
            passMatch = True
        if not re.match("^.{3,20}$", password):
            invalidPass = True
        if not re.match("^[\S]+@[\S]+.[\S]+$", email):
            invalidEmail = True


        error1 = "Please enter a user name" if noNameError else ""
        error2 = "<span class='error'>Invalid User name</span>" if invalidUser else ""
        error3 = "<span class='error'>Invalid Password</span>" if invalidPass else ""
        error4 = "<span class='error'>Passwords do not match</span>" if passMatch else ""
        error5 = "<span class='error'>Invalid Email</span>" if invalidEmail else ""
        response = pageHead + form % {"un": username,
                                      "pw": "",
                                      "ver": "",
                                      "em": "",
                                      "nn": error1,
                                      "nv": error2,
                                      "pv": error3,
                                      "vv": error4,
                                      "ie": error5} + pageFooter
        if noNameError == True or invalidUser == True or invalidPass == True or passMatch == True or invalidEmail == True:
            self.response.write(response)
        else:
            self.redirect("/welcome?username="+username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        message = "<h1>Welcome " + self.request.get("username") + "!</h1>"
        self.response.write(pageHead + message + pageFooter)

app = webapp2.WSGIApplication([
    ('/', Index),
    ("/welcome", Welcome)
], debug=True)
