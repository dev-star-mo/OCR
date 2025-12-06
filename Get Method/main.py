from fastapi import FastAPI, Request, HTTPException, status
from Routers import blog_get, blog_post, user, article, product, file, dependencies
from auth import authentication
from db import models
from client import html
from templates import templates
from db.database import engine
from exceptions import StoryException
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import time
from fastapi.websockets import WebSocket

app = FastAPI()
app.include_router(dependencies.router)
app.include_router(templates.router)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router) #include user router for user related operations
app.include_router(article.router) #include article router for article related operations
app.include_router(product.router)

#response handler for StoryException
@app.exception_handler(StoryException)
def story_exception_handler(request:Request, exc:StoryException):
    return JSONResponse(
        status_code=418, #code for doing tests
        content={'detail': exc.name}
    )

#custom response handler for general exceptions
#@app.exception_handler(HTTPException)
#def custom_http_exception_handler(request:Request, exc:HTTPException):
#    return(PlainTextResponse(str('Budaa'), status_code=status.HTTP_400_BAD_REQUEST))
    #or str(exc.detail) to return the original detail message
    # you can filter so it catches only the httpexceptions you want

@app.get("/")
async def get():
    return HTMLResponse(html)

clients =[]

@app.websocket('/chat')
async def websocket_endpoint(websocket:WebSocket):
    await websocket.accept() #accept the connection
    clients.append(websocket) #add to clients list, we want to store our connected clients
    while True:
        data = await websocket.receive_text() #receive text data from client
        for client in clients:
            await client.send_text(f"Message: {data}") #send the message to all connected clients

#add middleware. standard functionality for all endpoints can go to middlewares
@app.middleware('http')
async def add_middleware_for_timing(request:Request, call_next):
    start_time = time.time()
    #if we want we can modify the request here before passing it to the route handler
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['process_duration'] = str(duration)
    return response

origins = ['http://localhost:3000'] #list of allowed origins. just the loclhost running react

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

models.Base.metadata.create_all(bind=engine) #create the db tables

app.mount('/files', StaticFiles(directory="files"), name="files") #serve static files from 'files' directory at /files path
app.mount('/templates/static', StaticFiles(directory="templates/static"),
          name="static") #serve static files for templates like css/js