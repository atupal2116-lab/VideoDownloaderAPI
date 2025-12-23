from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

@app.get("/")
def ana_sayfa():
    return {"mesaj": "Video İndirici API'ye Hoş Geldiniz! /download?url=... kullanarak test edin."}

@app.get("/download")
def video_bilgisi_getir(url: str):
    """
    Verilen YouTube/Instagram/TikTok linkini analiz eder 
    ve indirme bağlantısını döner.
    """
    try:
        # Ayarlar: Videoyu sunucuya indirme, sadece linkini bul.
        ydl_opts = {
            'format': 'best',  # En iyi kaliteyi bul
            'quiet': True,     # Gereksiz log yapma
            'no_warnings': True,
        }

        # yt-dlp motorunu çalıştır
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Bilgileri çek (Ama indirme yapma: download=False)
            info = ydl.extract_info(url, download=False)
            
            # Gerekli bilgileri ayıkla
            video_baslik = info.get('title', 'Bilinmeyen Başlık')
            video_resmi = info.get('thumbnail', '')
            video_linki = info.get('url', '') # İşte asıl hazine bu!
            
            return {
                "baslik": video_baslik,
                "resim": video_resmi,
                "indirme_linki": video_linki,
                "platform": info.get('extractor_key', 'Bilinmiyor')
            }

    except Exception as hata:
        # Eğer bir sorun çıkarsa (Link bozuksa vs.)
        return {"hata": str(hata), "durum": "Video bulunamadi veya link hatali."}