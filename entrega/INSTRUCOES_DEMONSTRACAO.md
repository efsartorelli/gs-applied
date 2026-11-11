# Demonstração local

Integrantes: Enzo Vazquez Sartorelli (RM 94618), Kaue Pastori Teixeira (RM 98501), Nicolas Nogueira Boni (RM 551965), Guilherme Brazioli (RM 98237) e Pedro Oliveira Valotto (RM 551445).

```powershell
py -3.12 -m venv .venv-cv
.\.venv-cv\Scripts\python.exe -m pip install -r requirements.txt
# obter Construction-PPE e extrair em dataset/source/construction-ppe
.\.venv-cv\Scripts\python.exe training\prepare_dataset.py
.\.venv-cv\Scripts\python.exe training\train.py
.\.venv-cv\Scripts\python.exe training\validate.py
.\.venv-cv\Scripts\streamlit.exe run src\app.py
```

Acesse a URL local apresentada pelo Streamlit. Não exponha a interface à internet sem revisão de segurança e autorização.
