import webapp2, json, re
from google.appengine.api import mail

f = open('secret.txt','r')
secret_endpoint = f.read()
f.close()

def blast_mail(locale,date,chemical):
    pretty_locale = re.sub(r'_', ' ', locale)
    pretty_chemical = re.sub(r'_', ' ', chemical)
    report_url = "http://www.airwatchbayarea.org/reports/archived/%s/%s.html" % (date,locale)
    mail.send_mail(sender="AirWatch BayArea <airwatchbayarea@gmail.com>",
                   to="AirWatchBayArea <airwatchbayarea@googlegroups.com>",
                   subject="Air Pollution Alert for %s" % date,
                   body="""Hello from Air Watch: Bay Area!

Monitors in %s picked up elevated levels of %s yesterday. Print or download the data summary at:

%s

or explore the data in depth with wind info and smell reports at www.airwatchbayarea.org
""" % (pretty_locale,pretty_chemical,report_url))
    # [END send_mail]

class MailHandler(webapp2.RequestHandler):
    def post(self):
        jsonstring = self.request.body
        params = json.loads(jsonstring)
        locale = params['locale']
        date = params['date']
        chemical = params['chemical']
        blast_mail(locale,date,chemical)
        self.response.write("Sent mail to group")


app = webapp2.WSGIApplication([
    webapp2.Route(secret_endpoint, handler=MailHandler)
], debug=True)
