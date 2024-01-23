import psutil
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

print(psutil.pids())

app = FastAPI()

if(__name__ == "__main__"):
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

class ButtonData(BaseModel):
    button_id: int

def butona_tiklandi_aksi(button_id):
    print(f'Buton {button_id} tıklandı!')

@app.get("/", response_class=HTMLResponse)
def index():
    
    
    button_list = psutil.pids()

    button_html = ""
    for i, button_text in enumerate(button_list, start=1):
        button_html += f'<button onclick="butonTiklandi({i})">{button_text}</button><br>'

    return f"""
    <html>
    <head>
        <title>Buton Tıklama Örneği</title>
    </head>
    <body>
        <h1>Buton Tıklanma Olayı</h1>
        {button_html}
        <script>
            function butonTiklandi(buttonId) {{
                fetch('/buton_tiklandi', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{"button_id": buttonId}})
                }}).then(response => response.json()).then(data => {{
                    console.log(data);
                }});
                butona_tiklandi_aksi(buttonId);
            }}
        </script>
    </body>
    </html>
    """

@app.post("/buton_tiklandi")
def buton_tiklandi(request: Request, button_data: ButtonData):
    butona_tiklandi_aksi(button_data.button_id)
    return {'message': f'Buton {button_data.button_id} tıklandı!'}
