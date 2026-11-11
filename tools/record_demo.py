r"""Grava automaticamente uma demonstração real do Streamlit em MP4.

O navegador faz upload de imagens reais do holdout e aciona a inferência; slides apenas
contextualizam o material e não simulam resultados. Processos Streamlit preexistentes nunca
são encerrados. Execute com: .\.venv-cv\Scripts\python.exe tools\record_demo.py
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import date
from pathlib import Path
from urllib.request import urlopen

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
APP_URL = "http://127.0.0.1:8501"
FINAL_VIDEO = ROOT / "entrega" / "VIDEO_DEMONSTRACAO_APPLIED_COMPUTER_VISION.mp4"
RAW_VIDEO = ROOT / "entrega" / "VIDEO_DEMONSTRACAO_ORIGINAL.webm"
REPORT = ROOT / "entrega" / "RELATORIO_GRAVACAO.md"
INPUTS = ROOT / "entrega" / "inputs_demonstracao.json"
VIEWPORT = {"width": 1280, "height": 720}


def app_is_ready() -> bool:
    try:
        with urlopen(APP_URL, timeout=3) as response:
            return response.status == 200
    except OSError:
        return False


def start_app_if_needed() -> subprocess.Popen | None:
    if app_is_ready():
        return None
    command = [sys.executable, "-m", "streamlit", "run", "src/app.py", "--server.headless", "true", "--server.port", "8501"]
    process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    for _ in range(30):
        if app_is_ready():
            return process
        time.sleep(1)
    process.terminate()
    raise RuntimeError("Streamlit não respondeu em http://127.0.0.1:8501")


def edge_path() -> Path:
    options = [Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"), Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe")]
    found = next((item for item in options if item.is_file()), None)
    if not found:
        raise FileNotFoundError("Microsoft Edge não encontrado para a automação Playwright.")
    return found


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path(r"C:\Windows\Fonts") / name), size)


def make_card(path: Path, title: str, lines: list[str]) -> None:
    image = Image.new("RGB", (1280, 720), "#071C2C")
    draw = ImageDraw.Draw(image)
    draw.rectangle((50, 50, 1230, 670), outline="#28B6E6", width=3)
    draw.text((95, 100), title, fill="#FFFFFF", font=font(38, True))
    y = 200
    for line in lines:
        draw.text((105, y), line, fill="#D9F3FF", font=font(23), spacing=7)
        y += 46
    image.save(path)


def run_ffmpeg(arguments: list[str]) -> None:
    executable = imageio_ffmpeg.get_ffmpeg_exe()
    completed = subprocess.run([executable, "-y", *arguments], text=True, capture_output=True)
    if completed.returncode:
        raise RuntimeError(f"FFmpeg falhou: {completed.stderr[-2000:]}")


def capture_browser(raw_dir: Path, screenshots: Path, selected: dict) -> Path:
    scenes = [("capacete", "Detecção de capacete"), ("colete", "Detecção de colete"), ("oculos", "Detecção de óculos"), ("multiplos_objetos", "Múltiplos objetos")]
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=str(edge_path()), headless=True)
        context = browser.new_context(viewport=VIEWPORT, record_video_dir=str(raw_dir), record_video_size=VIEWPORT)
        page = context.new_page()
        for key, label in scenes:
            item = selected[key]
            image = ROOT / "dataset" / "ppe_3_classes_fixed" / "images" / "test" / item["file"]
            if not image.is_file():
                raise FileNotFoundError(image)
            page.goto(APP_URL, wait_until="networkidle", timeout=60000)
            page.get_by_text("Modelo carregado: best.pt").wait_for(timeout=30000)
            page.evaluate("document.body.style.zoom = '0.75'")
            page.locator("input[type=file]").first.set_input_files(str(image))
            page.get_by_role("button", name="Detectar EPIs").click()
            result_count = page.get_by_text(re.compile(r"^\d+ detecção\(ões\)"))
            result_count.wait_for(timeout=60000)
            result_count.scroll_into_view_if_needed()
            page.wait_for_timeout(1200)
            page.screenshot(path=str(screenshots / f"{key}.png"), full_page=False)
            page.wait_for_timeout(22000)
            print(f"Cena real registrada: {label} | {image.name}")
        video = page.video
        context.close()
        browser.close()
        if video is None:
            raise RuntimeError("Playwright não forneceu arquivo de vídeo.")
        return Path(video.path())


def main() -> None:
    if not INPUTS.is_file():
        raise FileNotFoundError(f"Execute tools/find_demo_inputs.py antes: {INPUTS}")
    selected = json.loads(INPUTS.read_text(encoding="utf-8"))["selected"]
    missing = {"capacete", "colete", "oculos", "multiplos_objetos"} - set(selected)
    if missing:
        raise RuntimeError(f"Cenas ausentes: {', '.join(sorted(missing))}")
    started = start_app_if_needed()
    screenshots = ROOT / "entrega" / "evidencias_video"
    screenshots.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="quem_faz_record_") as temporary:
        work = Path(temporary)
        raw_dir = work / "raw"
        raw_dir.mkdir()
        intro, results, outro = work / "intro.png", work / "resultados.png", work / "outro.png"
        make_card(intro, "GLOBAL SOLUTION FIAP 2026.2", ["Applied Computer Vision", "Detecção Inteligente de Equipamentos de Proteção Individual", "", "Enzo Vazquez Sartorelli - RM 94618", "Kaue Pastori Teixeira - RM 98501", "Nicolas Nogueira Boni - RM 551965", "Guilherme Brazioli - RM 98237", "Pedro Oliveira Valotto - RM 551445"])
        make_card(results, "RESULTADOS EXPERIMENTAIS REAIS", ["YOLO11n customizado | Construction-PPE", "Precision: 0,8892 | Recall: 0,7177", "mAP@50: 0,7691 | mAP@50-95: 0,4991", "", "A seguir: inferências realizadas na interface Streamlit."])
        make_card(outro, "CONCLUSÃO", ["Demonstração local com imagens reais do holdout.", "A solução apoia inspeção visual; não certifica segurança.", "Limitações: oclusão, iluminação, distância e treino curto.", "", "Professores: Arnaldo Viana e Paulo Rodrigues"])
        raw = capture_browser(raw_dir, screenshots, selected)
        shutil.copy2(raw, RAW_VIDEO)
        intro_mp4, results_mp4, outro_mp4, app_mp4 = (work / "intro.mp4", work / "resultados.mp4", work / "outro.mp4", work / "app.mp4")
        for card, output, duration in [(intro, intro_mp4, 20), (results, results_mp4, 20), (outro, outro_mp4, 20)]:
            run_ffmpeg(["-loop", "1", "-i", str(card), "-t", str(duration), "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-vf", "scale=1280:720", str(output)])
        run_ffmpeg(["-i", str(RAW_VIDEO), "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-vf", "scale=1280:720", str(app_mp4)])
        listing = work / "concat.txt"
        listing.write_text("\n".join(f"file '{item.as_posix()}'" for item in [intro_mp4, results_mp4, app_mp4, outro_mp4]), encoding="utf-8")
        run_ffmpeg(["-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", "-movflags", "+faststart", str(FINAL_VIDEO)])
    if started and started.poll() is None:
        started.terminate()
        started.wait(timeout=10)
    if not FINAL_VIDEO.is_file() or FINAL_VIDEO.stat().st_size == 0:
        raise RuntimeError("MP4 final não foi criado.")
    probe = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", str(FINAL_VIDEO), "-f", "null", "-"], text=True, capture_output=True)
    if probe.returncode:
        raise RuntimeError(f"Validação de decodificação falhou: {probe.stderr}")
    report = f"""# Relatório de gravação\n\n- Data: {date.today().strftime('%d/%m/%Y')}\n- Aplicação: {APP_URL}\n- Ferramentas: Streamlit, Playwright com Microsoft Edge e FFmpeg (imageio-ffmpeg).\n- Modelo: `models/best.pt`, YOLO11n treinado para capacete, colete e oculos.\n- Entradas: {', '.join(item['file'] for item in selected.values())}.\n- Execução: uploads reais no Streamlit e clique automatizado em **Detectar EPIs**; screenshots e vídeo foram produzidos após a inferência.\n- Arquivo final: `entrega/VIDEO_DEMONSTRACAO_APPLIED_COMPUTER_VISION.mp4` ({FINAL_VIDEO.stat().st_size} bytes).\n- Evidência bruta: `entrega/VIDEO_DEMONSTRACAO_ORIGINAL.webm`.\n- Validação: FFmpeg conseguiu abrir o MP4. Saída resumida: `{probe.stderr.splitlines()[-1] if probe.stderr else 'sem mensagens'}`.\n- Limitações: vídeo sem narração; os textos em cards contextualizam a execução e as detecções são produzidas pela interface real.\n"""
    REPORT.write_text(report, encoding="utf-8")
    print(FINAL_VIDEO)
    print(RAW_VIDEO)
    print(REPORT)


if __name__ == "__main__":
    main()
