"""Seleciona entradas do holdout que produzem detecções reais para a demonstração."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from detect import CLASS_NAMES, load_model  # noqa: E402


def main() -> None:
    image_dir = ROOT / "dataset" / "ppe_3_classes_fixed" / "images" / "test"
    if not image_dir.is_dir():
        raise FileNotFoundError(f"Holdout ausente: {image_dir}")
    model = load_model()
    candidates: dict[str, list[dict]] = {name: [] for name in CLASS_NAMES}
    multi: list[dict] = []
    for image in sorted(image_dir.glob("*.*")):
        result = model.predict(source=str(image), conf=0.25, imgsz=416, device=0, verbose=False)[0]
        detections = [
            {"class_name": CLASS_NAMES[int(box.cls.item())], "confidence": round(float(box.conf.item()), 4)}
            for box in result.boxes
        ]
        item = {"file": image.name, "detections": detections}
        found = {det["class_name"] for det in detections}
        for name in found:
            candidates[name].append(item)
        if len(found) > 1:
            multi.append(item)
    def confidence_for(item: dict, name: str) -> float:
        return max(det["confidence"] for det in item["detections"] if det["class_name"] == name)

    selected = {}
    for name, values in candidates.items():
        if not values:
            continue
        if name == "oculos":
            selected[name] = min(values, key=lambda item: (len(item["detections"]), -confidence_for(item, name)))
        else:
            selected[name] = max(values, key=lambda item: confidence_for(item, name))
    if multi:
        selected["multiplos_objetos"] = multi[0]
    missing = [name for name in CLASS_NAMES if name not in selected]
    if missing:
        raise RuntimeError(f"Nenhuma detecção >=0,25 encontrada para: {', '.join(missing)}")
    output = ROOT / "entrega" / "inputs_demonstracao.json"
    output.write_text(json.dumps({"confidence": 0.25, "selected": selected}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)
    print(json.dumps(selected, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
