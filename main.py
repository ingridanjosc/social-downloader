from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

# Configuração reforçada de CORS para liberar totalmente o acesso do seu site
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Servidor rodando perfeitamente!"}

@app.get("/download")
def get_download_url(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="URL inválida")
        
    # Configurações otimizadas do yt-dlp
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'add_header': [
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Tenta pegar o link direto do vídeo
            video_url = info.get('url')
            
            # Se for uma playlist ou múltiplos formatos, pega o primeiro item válido
            if not video_url and 'entries' in info:
                video_url = info['entries'][0]['url']
                
            if not video_url:
                return {"success": False, "error": "Não foi possível extrair a URL direta do vídeo."}
            
            return {
                "success": True,
                "downloadUrl": video_url
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
