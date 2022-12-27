from fastapi import FastAPI,Depends,status,Response,HTTPException,Request
from pydantic import BaseModel
import uvicorn
import models
from database import engine,Session_local
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

#FastAPI is a class that inherits directly from Starlette.

# fastapi is based on pydantic and typehints strongs
# docs available at path docs
# pip install "fastapi[all]"

#models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# mounting the static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



models.Base.metadata.create_all(bind=engine)

def get_db():
    db=Session_local()
    try:
        yield db
    finally:
        db.close()


class Student(BaseModel):
    name: str
    roll: int



# uvicorn main:app --reload
@app.get("/")
async def hello():
    return {"hello": "world"}

# simple path operation with dynamic routing
@app.get("/next/{items}")
def get_num(items: int):
    return {"num": items}

# simple path operation with post and pydantic
# @app.post("/ap")
# def post_s(student: Student):
#     return {student.name}
# debug the entire in reload mode for faster development


# simple querying in fast Api
@app.get("/api")
def query_str(name: str,age: int):
    return {name:age}
# simply make a get request to localhost
# /api?name=Nitesh&age=10

# docs gives you the swagger ui ti test and play

# look for http status code in pytohn docs for status codes
#status_1=status.HTTP_201_CREATED

@app.post("/blog",status_code=201)
def create(request: Student,db: Session=Depends(get_db)):
    new_blog=models.Blog(title=request.name)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@app.get("/blogs_")
def all(response: Response,db: Session=Depends(get_db)):
    blogs=db.query(model.Blog).all()
    if not blogs:
        response.status_code=status.HTTP_404_NOT_FOUND
    return blogs

@app.get("/blog_get/{item}")
def get_item(item: int,db: Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==item).first()
    return blog

@app.post("/user")
def create_user(request: Student):
    pass

@app.get("/items_/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})


@app.get('/get_students',status_code=200)
def get_students(response: Response,request:Request, db:Session=Depends(get_db)):
    blog=db.query(models.Blog).all()
    
    
    
    if not blog:
        response.status_code=status.HTTP_404_NOT_FOUND
    def columns():
        return ['id','title']
    
    def getting_tup():
        for bl in blog:
            # yield {'id':bl.id,'title':bl.title}
            yield (bl.id,bl.title)

        
    return templates.TemplateResponse("table.html", {"request": request, "students": getting_tup(),"columns":columns()})
        





if __name__=='__main__':
    uvicorn.run(app,host="127.0.0.1",port=8000)

