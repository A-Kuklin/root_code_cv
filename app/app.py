import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from settings import settings
from chart_generator import generate_chart


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/chart")
async def get_chart():
    chart = await generate_chart()
    return StreamingResponse(chart, media_type="image/png")


if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(app, host=settings.app_host, port=settings.app_port)
