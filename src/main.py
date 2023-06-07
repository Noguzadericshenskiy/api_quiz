from fastapi import FastAPI
import uvicorn

from user.routers import router as routes_user
from record.routers import router as router_record
from question.routes import router as router_questions


app = FastAPI(title="pet API")

app.include_router(router_questions)
app.include_router(routes_user)
app.include_router(router_record)


# if __name__ == '__main__':
#     uvicorn.run("main:app", port=8000, host='127.0.0.1')
