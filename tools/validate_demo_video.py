"""Valida e extrai evidências visuais do MP4 de demonstração."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
VIDEO = ROOT / "entrega" / "VIDEO_DEMONSTRACAO_APPLIED_COMPUTER_VISION.mp4"
OUT = ROOT / "entrega" / "evidencias_video"


def main() -> None:
    if not VIDEO.is_file() or VIDEO.stat().st_size == 0:
        raise FileNotFoundError(VIDEO)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    decode = subprocess.run([ffmpeg, "-v", "error", "-i", str(VIDEO), "-f", "null", "-"], text=True, capture_output=True)
    if decode.returncode:
        raise RuntimeError(decode.stderr)
    metadata = subprocess.run([ffmpeg, "-i", str(VIDEO)], text=True, capture_output=True).stderr
    duration = re.search(r"Duration: (\d\d:\d\d:\d\d\.\d\d)", metadata)
    stream = re.search(r"Video: ([^\n]+)", metadata)
    OUT.mkdir(exist_ok=True)
    frames = []
    for second, name in [(5, "frame_abertura.png"), (48, "frame_streamlit_capacete.png"), (80, "frame_streamlit_colete.png"), (112, "frame_streamlit_oculos.png"), (140, "frame_streamlit_multiplos.png"), (160, "frame_conclusao.png")]:
        path = OUT / name
        capture = subprocess.run([ffmpeg, "-y", "-ss", str(second), "-i", str(VIDEO), "-frames:v", "1", str(path)], text=True, capture_output=True)
        if capture.returncode or not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError(f"Falha ao extrair frame {second}s: {capture.stderr[-500:]}")
        frames.append({"second": second, "file": str(path.relative_to(ROOT)).replace("\\", "/"), "bytes": path.stat().st_size})
    digest = hashlib.sha256(VIDEO.read_bytes()).hexdigest()
    payload = {"video": str(VIDEO.relative_to(ROOT)).replace("\\", "/"), "bytes": VIDEO.stat().st_size, "sha256": digest, "duration": duration.group(1) if duration else None, "stream": stream.group(1).strip() if stream else None, "decode_validation": "ok", "frames": frames}
    (ROOT / "entrega" / "VALIDACAO_VIDEO.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
