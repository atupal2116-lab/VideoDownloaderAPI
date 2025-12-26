import os
import yt_dlp
from fastapi import FastAPI
from fastapi.responses import FileResponse
import uuid

app = FastAPI()

@app.get("/")
def home():
    return {"message": "TikTok Downloader (Render) Calisiyor. /download?url=... kullanin."}

@app.get("/download")
async def download_video(url: str):
    # Rastgele bir dosya adı oluştur
    filename = f"{uuid.uuid4()}.mp4"
    
    # yt-dlp ayarları (Basit ve hızlı)
    ydl_opts = {
        'format': 'best',    # En iyi kaliteyi seç
        'outtmpl': filename, # Dosya adı
        'quiet': True,       # Logları gizle
        'no_warnings': True,
    }

    try:
        # Videoyu sunucuya indir
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # İndirilen dosyayı kullanıcıya gönder
        return FileResponse(path=filename, filename="tiktok_video.mp4", media_type="video/mp4")

    except Exception as e:
        # Hata olursa temizlik yap ve hatayı söyle
        if os.path.exists(filename):
            os.remove(filename)
        return {"error": str(e), "status": "Hata oluştu."}

# Render'da sunucuyu başlatmak için gerekli kısım
# (requirements.txt içinde uvicorn olduğu için burası otomatik çalışır ama dosya sonunda dursun)