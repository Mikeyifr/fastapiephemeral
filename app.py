from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# pip install fastapi
# pip install uvicorn
# pip install jinja 2
# pip install python-multipart

companies = {"name": name, "field": field, "manager": manager, "phone": phone}

def add_to_companies(name, field, manager, phone):
    companies[len(companies)] = {"name": name, "field": field, "manager": manager, "phone": phone}

def find_comapny(name):
    for company in companies:
        if name == companies[company]["name"]:
            return companies[company]
    return 404

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get('/', response_class = HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('homepage.html', {'request': request})

@app.get('/post', response_class = HTMLResponse)
def addcopmany(request: Request):
    return templates.TemplateResponse('addcompany.html', {'request': request})

@app.post('/post', response_class = HTMLResponse)
def addedcopmany(request: Request, name: str = Form(...), 
                 field: str = Form(...), manager: str = Form(...), phone: str = Form(...)):
    add_to_companies(name, field, manager, phone)
    print(companies)
    print(find_comapny(name))
    return templates.TemplateResponse('addcompany.html', {'request': request})

@app.get('/get', response_class = HTMLResponse)
def getcompany(request: Request):
    return templates.TemplateResponse('getcompany.html', {'request': request})

@app.post('/get', response_class = HTMLResponse)
def companyinfo(request: Request, findname: str = Form(...)):
    company = find_comapny(findname)
    if company != 404:
        return templates.TemplateResponse('companyinfo.html', {'request': request,  "name": company["name"],
                                            "field": company["field"], "manager": company["manager"], "phone": company["phone"]})
    else:
        return "The company you are looking for does not exist in our records"
