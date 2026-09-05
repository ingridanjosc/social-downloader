from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import yt_dlp

app = FastAPI()

# Permissão total e explícita para qualquer site conectar
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
        return JSONResponse(status_code=400, content={"success": False, "error": "URL inválida"})
        
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
            video_url = info.get('url')
            
            if not video_url and 'entries' in info:
                video_url = info['entries'][0]['url']
                
            if not video_url:
                return {"success": False, "error": "Não foi possível extrair o link direto."}
            
            # Retorna uma resposta HTTP explícita com cabeçalhos limpos
            return JSONResponse(content={
                "success": True,
                "downloadUrl": video_url
            })
    except Exception as e:
        return JSONResponse(content={
            "success": False,
            "error": str(e)
        })
