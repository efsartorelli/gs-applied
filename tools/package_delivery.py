"""Cria e valida o ZIP definitivo da entrega Applied Computer Vision."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "GS_APPLIED_COMPUTER_VISION_FIAP_2026"
OUT = ROOT / "entrega_final"
ZIP = OUT / "GS_APPLIED_COMPUTER_VISION_FIAP_2026_ENTREGA_FINAL.zip"

AUTHORS = [
    "Enzo Vazquez Sartorelli — RM 94618",
    "Kaue Pastori Teixeira — RM 98501",
    "Nicolas Nogueira Boni — RM 551965",
    "Guilherme Brazioli — RM 98237",
    "Pedro Oliveira Valotto — RM 551445",
]


def copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def copy_tree(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"))


def text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def command(args: list[str], cwd: Path, timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, timeout=timeout)


def create_cover(path: Path, commit: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    cover = ParagraphStyle("cover", parent=styles["BodyText"], alignment=TA_CENTER, fontSize=12, leading=18)
    title = ParagraphStyle("title", parent=styles["Title"], alignment=TA_CENTER, fontSize=24, leading=30)
    body = [Spacer(1, 2.5 * cm), Paragraph("FIAP", title), Paragraph("GLOBAL SOLUTION 2026.2 — CitizenTech", cover), Spacer(1, 0.8 * cm), Paragraph("APPLIED COMPUTER VISION", title), Paragraph("Detecção Inteligente de Equipamentos de Proteção Individual", cover), Spacer(1, 0.8 * cm), Paragraph("Disciplina: Applied Computer Vision — Enxergando o Mundo Real", cover), Paragraph("Curso: Engenharia de Software", cover), Paragraph("Professores: Arnaldo Viana e Paulo Rodrigues", cover), Spacer(1, 0.6 * cm)]
    body += [Paragraph(author, cover) for author in AUTHORS]
    body += [Spacer(1, 0.7 * cm), Paragraph("Este pacote contém relatório acadêmico, vídeo real, modelo YOLO11n treinado, código, métricas e evidências.", cover), Paragraph("O modelo detecta visualmente capacete, colete e óculos. A saída não certifica conformidade de segurança e não substitui inspeção humana.", cover), Spacer(1, 0.5 * cm), Paragraph("Navegação: relatório em 01_RELATORIO_ACADEMICO; vídeo em 02_VIDEO_DEMONSTRACAO; código em 03_CODIGO_FONTE; modelo em 04_MODELO_TREINADO; resultados em 05_RESULTADOS_E_METRICAS.", cover), Paragraph(f"GitHub: https://github.com/efsartorelli/gs-applied | branch main | commit {commit}", cover)]
    SimpleDocTemplate(str(path), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=1.8 * cm, title="Leia Primeiro").build(body)


def source_checks() -> dict:
    required = [ROOT / "entrega" / "RELATORIO_APPLIED_COMPUTER_VISION.pdf", ROOT / "entrega" / "VIDEO_DEMONSTRACAO_APPLIED_COMPUTER_VISION.mp4", ROOT / "models" / "best.pt", ROOT / "results" / "metrics" / "test_metrics.json", ROOT / "examples" / "demo_input.jpg"]
    missing = [str(item) for item in required if not item.is_file()]
    if missing:
        raise FileNotFoundError("Arquivos obrigatórios ausentes: " + ", ".join(missing))
    return {"report": required[0], "video": required[1], "model": required[2]}


def assemble(stage: Path, commit: str) -> Path:
    package = stage / PACKAGE
    create_cover(package / "00_LEIA_PRIMEIRO.pdf", commit)
    copy(ROOT / "entrega" / "RELATORIO_APPLIED_COMPUTER_VISION.pdf", package / "01_RELATORIO_ACADEMICO" / "RELATORIO_APPLIED_COMPUTER_VISION.pdf")
    copy(ROOT / "entrega" / "VIDEO_DEMONSTRACAO_APPLIED_COMPUTER_VISION.mp4", package / "02_VIDEO_DEMONSTRACAO" / "VIDEO_DEMONSTRACAO_APPLIED_COMPUTER_VISION.mp4")
    text(package / "02_VIDEO_DEMONSTRACAO" / "INFORMACOES_VIDEO.md", "# Informações do vídeo\n\nDemonstração real automatizada com Playwright e Microsoft Edge. Duração validada: 2min47s; H.264, 1280×720, 30 fps. O vídeo envia imagens reais do holdout ao Streamlit e mostra capacete, colete, óculos e múltiplos objetos. Não há narração. Consulte `07_EVIDENCIAS_E_TESTES/validacao_video/VALIDACAO_VIDEO.json`.\n")
    code = package / "03_CODIGO_FONTE"
    for item in ["README.md", "requirements.txt", "LICENSE", ".gitattributes"]:
        copy(ROOT / item, code / item)
    for folder in ["src", "training", "tests", "tools", "examples"]:
        copy_tree(ROOT / folder, code / folder)
    copy(ROOT / "models" / "best.pt", package / "04_MODELO_TREINADO" / "best.pt")
    text(package / "04_MODELO_TREINADO" / "README_MODELO.md", "# Modelo treinado\n\nPeso: `best.pt`, produzido pelo experimento válido `yolo11n_ppe3_fixed`. Arquitetura: YOLO11n pré-treinada com fine-tuning customizado. Classes: 0 capacete, 1 colete, 2 oculos. Dataset: Construction-PPE (CC BY 4.0), com classes helmet, vest e goggles remapeadas. Configuração: 5 épocas, 416 px, batch 2, seed 42, AMP, GPU RTX 3060. No pacote, o código encontra o peso em `../04_MODELO_TREINADO/best.pt`.\n")
    results = package / "05_RESULTADOS_E_METRICAS"
    copy(ROOT / "results" / "metrics" / "test_metrics.json", results / "metricas" / "test_metrics.json")
    for file in (ROOT / "results" / "plots").glob("*.png"):
        copy(file, results / "graficos" / file.name)
    for file in [ROOT / "results" / "predictions" / "example_test_annotated.jpg", ROOT / "results" / "predictions" / "validation_example_pred.jpg"]:
        copy(file, results / "exemplos_inferencia" / file.name)
    docs = package / "06_DOCUMENTACAO_TECNICA"
    for file in ["ARQUITETURA.md", "TREINAMENTO.md", "RESULTADOS.md", "INSTRUCOES_EXECUCAO.md", "CONFORMIDADE.md", "AUTORES.md"]:
        copy(ROOT / "docs" / file, docs / file)
    copy(ROOT / "dataset" / "README.md", docs / "DATASET_E_LICENCA.md")
    evidence = package / "07_EVIDENCIAS_E_TESTES"
    copy(ROOT / "entrega" / "VALIDACAO_VIDEO.json", evidence / "validacao_video" / "VALIDACAO_VIDEO.json")
    for file in (ROOT / "entrega" / "evidencias_video").glob("*.png"):
        copy(file, evidence / "evidencias_reais" / file.name)
    text(evidence / "resultados_testes" / "RESULTADOS_TESTES.md", "# Testes executados antes do empacotamento\n\n`python -m unittest discover -s tests -v`: 3 testes aprovados. Foram validados: existência/classes do peso, rejeição de imagem inválida e inferência real. A validação independente do ZIP reexecuta essa suíte a partir da cópia extraída.\n")
    links = f"""# Links oficiais\n\n- Repositório: https://github.com/efsartorelli/gs-applied\n- Branch: `main`\n- Commit do pacote: `{commit}`\n- PDF público: https://github.com/efsartorelli/gs-applied/blob/{commit}/entrega/RELATORIO_APPLIED_COMPUTER_VISION.pdf\n- Vídeo público: https://github.com/efsartorelli/gs-applied/blob/{commit}/entrega/VIDEO_DEMONSTRACAO_APPLIED_COMPUTER_VISION.mp4\n- Dataset: https://docs.ultralytics.com/datasets/detect/construction-ppe/\n- Licença do dataset: https://creativecommons.org/licenses/by/4.0/\n- Ultralytics: https://docs.ultralytics.com/\n- Treinamento Ultralytics: https://docs.ultralytics.com/modes/train/\n- PyTorch: https://pytorch.org/get-started/locally/\n"""
    text(package / "08_REFERENCIAS_E_LINKS" / "LINKS_OFICIAIS.md", links)
    text(package / "README_ENTREGA.md", "# Entrega final — Applied Computer Vision\n\nComece por `00_LEIA_PRIMEIRO.pdf`. O código e a reprodução estão em `03_CODIGO_FONTE`; o modelo real está em `04_MODELO_TREINADO`; o relatório e o vídeo estão nas pastas 01 e 02. O dataset completo não acompanha o pacote; siga `06_DOCUMENTACAO_TECNICA/INSTRUCOES_EXECUCAO.md` para obtê-lo de fonte oficial.\n")
    files = [item for item in package.rglob("*") if item.is_file()]
    total = sum(item.stat().st_size for item in files)
    text(package / "MANIFESTO_ENTREGA.md", f"# Manifesto interno da entrega\n\n- Gerado: {datetime.now().isoformat(timespec='seconds')}\n- Arquivos antes deste manifesto: {len(files)}\n- Tamanho antes deste manifesto: {total} bytes\n- Commit: {commit}\n- Integridade: CRC do ZIP, extração, testes, inferência real, inicialização Streamlit, PDF e vídeo são verificados pelo processo de empacotamento.\n- O hash do ZIP é registrado apenas no manifesto externo para evitar referência circular.\n")
    return package


def validate_extracted(extracted: Path) -> dict:
    package = extracted / PACKAGE
    code = package / "03_CODIGO_FONTE"
    python = sys.executable
    test = command([python, "-m", "unittest", "discover", "-s", "tests", "-v"], code, 180)
    if test.returncode:
        raise RuntimeError("Testes extraídos falharam:\n" + test.stdout + test.stderr)
    inference = command([python, "src/run_inference.py", "--input", "examples/demo_input.jpg", "--output", "inference_package.jpg"], code, 180)
    if inference.returncode or not (code / "inference_package.jpg").is_file():
        raise RuntimeError("Inferência extraída falhou:\n" + inference.stdout + inference.stderr)
    app = subprocess.Popen([python, "-m", "streamlit", "run", "src/app.py", "--server.headless", "true", "--server.port", "8503"], cwd=code, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    ready = False
    try:
        for _ in range(30):
            try:
                ready = urllib.request.urlopen("http://127.0.0.1:8503", timeout=2).status == 200
            except OSError:
                time.sleep(1)
            if ready:
                break
    finally:
        app.terminate()
        app.wait(timeout=15)
    if not ready:
        raise RuntimeError("Streamlit extraído não respondeu na porta 8503.")
    from pypdf import PdfReader
    if len(PdfReader(str(package / "01_RELATORIO_ACADEMICO" / "RELATORIO_APPLIED_COMPUTER_VISION.pdf")).pages) != 6:
        raise RuntimeError("PDF extraído não possui as seis páginas esperadas.")
    import imageio_ffmpeg
    video = package / "02_VIDEO_DEMONSTRACAO" / "VIDEO_DEMONSTRACAO_APPLIED_COMPUTER_VISION.mp4"
    decode = command([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", str(video), "-f", "null", "-"], package, 180)
    if decode.returncode:
        raise RuntimeError("Vídeo extraído não decodificou.")
    return {"tests": "ok", "inference": "ok", "streamlit": "ok", "pdf": "ok", "video": "ok"}


def main() -> None:
    source_checks()
    commit = command(["git", "rev-parse", "HEAD"], ROOT).stdout.strip()
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="gs_applied_package_") as work:
        work_path = Path(work)
        package = assemble(work_path, commit)
        with zipfile.ZipFile(ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
            for file in sorted(package.rglob("*")):
                if file.is_file():
                    archive.write(file, file.relative_to(work_path).as_posix())
        with zipfile.ZipFile(ZIP) as archive:
            broken = archive.testzip()
            names = set(archive.namelist())
        required = {f"{PACKAGE}/00_LEIA_PRIMEIRO.pdf", f"{PACKAGE}/01_RELATORIO_ACADEMICO/RELATORIO_APPLIED_COMPUTER_VISION.pdf", f"{PACKAGE}/02_VIDEO_DEMONSTRACAO/VIDEO_DEMONSTRACAO_APPLIED_COMPUTER_VISION.mp4", f"{PACKAGE}/04_MODELO_TREINADO/best.pt", f"{PACKAGE}/03_CODIGO_FONTE/src/detect.py", f"{PACKAGE}/03_CODIGO_FONTE/training/train.py", f"{PACKAGE}/03_CODIGO_FONTE/requirements.txt"}
        if broken or not required.issubset(names):
            raise RuntimeError(f"ZIP inválido: crc={broken}, ausentes={required-names}")
        extracted = work_path / "extracted"
        with zipfile.ZipFile(ZIP) as archive:
            archive.extractall(extracted)
        checks = validate_extracted(extracted)
    external = {"zip": ZIP.name, "generated_at": datetime.now().isoformat(timespec="seconds"), "files": len(names), "zip_bytes": ZIP.stat().st_size, "zip_sha256": sha256(ZIP), "crc_test": "ok", "extraction_validation": checks, "commit": commit, "pending": []}
    text(OUT / "MANIFESTO_ENTREGA.md", "# Manifesto externo da entrega\n\n```json\n" + json.dumps(external, ensure_ascii=False, indent=2) + "\n```\n")
    print(json.dumps(external, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
