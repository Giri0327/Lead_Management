
from app.api.endpoints import lead,priority,stage,statuses,users,sources,sales_pipeline
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(CORSMiddleware
                   ,allow_origins=["*"],allow_credentials=["*"],
                   allow_methods=["*"],allow_headers=["*"])


origins = ["http://localhost:5174"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,allow_credentials=True,
    allow_methods=["*"],allow_headers=["*"])

app.include_router(users.router)
app.include_router(lead.router)
app.include_router(stage.router)
app.include_router(statuses.router)
app.include_router(priority.router)
app.include_router(sources.router)
app.include_router(sales_pipeline.router)




