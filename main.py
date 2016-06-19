#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)



def convert(x):
    ''' convert x or y into integer '''
    if x == "":
        return ""
    try:
        x = float(x)
        return x
    except ValueError:  # user entered non-numeric value
        return "invalid input"


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")


class RezultatHandler(BaseHandler):
    def post(self):
        x = self.request.get("vnos1")
        osnovnaenota = self.request.get("vnos2")
        novaenota = self.request.get("vnos3")
        x1 = convert(x)
        if x1 == "invalid input":
            rezultat = "Not valid input"
        elif osnovnaenota == "m" and novaenota == "dm":
            rezultat = x1 * 10
        elif osnovnaenota == "dm" and novaenota == "cm":
            rezultat = x1 * 10
        elif osnovnaenota == "cm" and novaenota == "mm":
            rezultat = x1 *10
        elif osnovnaenota == "dm" and novaenota == "m":
            rezultat = x1 / 10
        elif osnovnaenota == "cm" and novaenota == "dm":
            rezultat = x1 / 10
        elif osnovnaenota == "mm" and novaenota == "cm":
            rezultat = x1 / 10
        elif osnovnaenota == "m" and novaenota == "cm":
            rezultat = x1 * 100
        elif osnovnaenota == "dm" and novaenota == "mm":
            rezultat = x1 * 100
        elif osnovnaenota == "cm" and novaenota == "m":
            rezultat = x1 / 100
        elif osnovnaenota == "mm" and novaenota == "dm":
            rezultat = x1 / 100
        elif osnovnaenota == "m" and novaenota == "mm":
            rezultat = x1 * 1000
        elif osnovnaenota == "mm" and novaenota == "m":
            rezultat = x1 / 1000


        else:
            rezultat = "Not working - choosen units don't exist."

        parametri = {"rezultat": rezultat, "vnos3": novaenota, "vnos2": osnovnaenota, "vnos1": x}
        return self.render_template("rezultat.html", params=parametri)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
], debug=True)
