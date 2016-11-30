import web
from web import form
import logging
import json
import time
import re

logging.basicConfig(level=logging.DEBUG)

def store_to_file(page_dict):
    ISOTIMEFORMAT='%Y%m%d%H%M%S'
    url_split_l = re.split('/', page_dict['url'])
    if len(url_split_l) >= 3:
        url_domain = url_split_l[2]
    else:
        url_domain = "not_sure"
    filename = "./result/" + url_domain + "-raw-"+ str(time.strftime(ISOTIMEFORMAT)) + ".json"
    fp = open(filename, "w")
    json.dump(page_dict, fp, indent=4, separators=(',',':'), sort_keys=True)
    fp.close()

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/hello', 'helloc'
    )
app = web.application(urls, globals())

myform = form.Form(
    form.Textbox("url"),
    form.Textbox("1-title"),
    form.Textbox("1-content"),
    form.Textbox("2-title"),
    form.Textbox("2-content"),
    form.Textbox("3-title"),
    form.Textbox("3-content"),
    form.Textbox("4-title"),
    form.Textbox("4-content"),
    form.Textbox("5-title"),
    form.Textbox("5-content"),
    form.Button("Add a column")
    )
#        form.notnull,
#        form.regexp('\d+', 'Must be a digit'),
#        form.Validator('Must be more than 5', lambda x:int(x)>5)),
    #form.Textarea('moe'),
    #form.Checkbox('curly'),
    #form.Dropdown('french', ['mustard', 'fries', 'wine']))

class index:
    def GET(self):
        form = myform()
        # make sure you create a copy of the form by calling it (line above)
        # Otherwise changes will appear globally
        return render.formtest(form)

    def POST(self):
        form = myform()
        if form.validates():
            #logging.info("form.d.url: %s" % form.d.url)
            #logging.info("form['url'].value: %s" % form["url"].value)
            page_dict = {}
            page_dict["url"] = form['url'].value
            page_dict["1-title"] = form['1-title'].value
            page_dict["1-content"] = form['1-content'].value
            page_dict["2-title"] = form['2-title'].value
            page_dict["2-content"] = form['2-content'].value
            logging.info("page_dict: %s" % page_dict)
            store_to_file(page_dict)
            result = "Good try."
            return render.formtest(form, result)

class helloc:
    def GET(self):
        #form = myform()
        # make sure you create a copy of the form by calling it (line above)
        # Otherwise changes will appear globally
        return render.hello_form(col_num=2)

    def POST(self):
        form = web.input(name="N", greet="a")
        #if form.validates():
            #logging.info("form.d.url: %s" % form.d.url)
            #logging.info("form['url'].value: %s" % form["url"].value)
            #page_dict = {}
            #page_dict["url"] = form['url'].value
            #page_dict["1-title"] = form['1-title'].value
            #page_dict["1-content"] = form['1-content'].value
            #page_dict["2-title"] = form['2-title'].value
            #page_dict["2-content"] = form['2-content'].value
            #logging.info("page_dict: %s" % page_dict)
            #store_to_file(page_dict)
            result = "Good try."
            return render.formtest(form, result)

if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()
