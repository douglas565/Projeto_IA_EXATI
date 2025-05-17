from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from core.back_end.web_capture.crawler_exati import ExatiCrawler
import os

app = FastAPI()

# Configuração básica
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/api/analyze")
async def analyze(id_saac: str):
    crawler = ExatiCrawler()
    try:
        crawler.login()
        img_path = crawler.search_by_id(id_saac)
        return {
            "status": "success",
            "image": img_path,
            "id": id_saac
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        crawler.close()