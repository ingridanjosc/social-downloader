from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

# Permite que o seu site no GitHub acesse este servidor com segurança
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # No futuro, você pode trocar pelo link do seu GitHub Pages
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/download")
def get_download_url(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="URL inválida")
        
    # Configurações do yt-dlp para pegar apenas o link direto do vídeo
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Retorna o link direto do vídeo hospedado nos servidores da rede social
            video_url = info.get('url')
            
            return {
                "success": True,
                "downloadUrl": video_url
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
