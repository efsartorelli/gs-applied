"""Gera o relatório PDF do experimento Applied Computer Vision a partir das métricas reais."""
from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "entrega" / "RELATORIO_APPLIED_COMPUTER_VISION.pdf"
METRICS = json.loads((ROOT / "results" / "metrics" / "test_metrics.json").read_text(encoding="utf-8"))

SUMMARY = """Este relatório apresenta o MVP Quem Faz - Applied Computer Vision, desenvolvido para demonstrar detecção visual de equipamentos de proteção individual em imagens de contexto de construção. O problema abordado é a dificuldade de observar, de forma escalável, indícios de uso de capacete, colete e óculos, sem transformar a solução em certificação de segurança. Foi realizado fine-tuning local de YOLO11n pré-treinado com um subconjunto de três classes do Construction-PPE. As classes helmet, vest e goggles foram remapeadas para capacete, colete e oculos. O conjunto original possui 1.000 imagens; a preparação usou 800 imagens de treino e dividiu deterministicamente as 200 imagens de validação originais em validação e teste, com 100 imagens cada e seed 42. O treinamento válido executou cinco épocas em Windows, Python 3.12, PyTorch 2.7.1+cu118, Ultralytics 8.4.210 e GPU NVIDIA RTX 3060, com imagens de 416 pixels, batch 2, AMP e workers zero. No holdout de 100 imagens e 390 instâncias, nunca empregado no treinamento, foram obtidos precisão 0,8892, recall 0,7177, mAP@50 0,7691 e mAP@50-95 0,4991. A classe colete teve o melhor mAP@50-95, 0,6141; capacete atingiu 0,4762 e oculos 0,4068. O MVP Streamlit aceita imagens, desenha caixas, mostra confiança e oferece processamento local de vídeo por script. As evidências incluem peso treinado, métricas JSON, curvas, matriz de confusão, exemplo anotado e testes automatizados. A solução exige validação adicional em câmeras e cenários reais, sobretudo por oclusão, iluminação, distância e pelo treinamento curto; portanto, deve apoiar, e não substituir, inspeção humana e procedimentos de segurança."""

OBJECTIVE = """Desenvolver e validar um MVP de visão computacional que detecte capacete, colete e óculos de proteção em imagens, usando treinamento customizado de YOLO e inferência local. O objetivo é demonstrar apoio rastreável à inspeção visual de EPI, com métricas reais, interface utilizável e limites explícitos de responsabilidade."""


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(escape(text).replace("\n", "<br/>"), style)


def figure(path: Path, width: float, caption: str, styles: dict) -> list:
    if not path.is_file():
        return [p(f"Figura indisponível no momento da geração: {path.name}.", styles["BodyText"])]
    image = Image(str(path))
    image._restrictSize(width, 14 * cm)
    return [image, Spacer(1, 0.1 * cm), Paragraph(caption, styles["Caption"]), Spacer(1, 0.35 * cm)]


def footer(canvas, document):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#52606D"))
    canvas.drawString(2 * cm, 1.15 * cm, "Quem Faz | Global Solution FIAP 2026.2 | Applied Computer Vision")
    canvas.drawRightString(A4[0] - 2 * cm, 1.15 * cm, f"Página {document.page}")
    canvas.restoreState()


def main() -> None:
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCV", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=23, leading=29, alignment=TA_CENTER, textColor=colors.HexColor("#092E4D"), spaceAfter=16))
    styles.add(ParagraphStyle(name="Cover", parent=styles["BodyText"], fontSize=12, leading=18, alignment=TA_CENTER, textColor=colors.HexColor("#263238")))
    styles.add(ParagraphStyle(name="H1CV", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#092E4D"), spaceBefore=8, spaceAfter=8))
    styles.add(ParagraphStyle(name="H2CV", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=colors.HexColor("#0B5C8C"), spaceBefore=6, spaceAfter=5))
    styles.add(ParagraphStyle(name="BodyCV", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.6, leading=14, alignment=TA_JUSTIFY, spaceAfter=7))
    styles.add(ParagraphStyle(name="Caption", parent=styles["BodyText"], fontName="Helvetica-Oblique", fontSize=8, leading=10, alignment=TA_CENTER, textColor=colors.HexColor("#52606D")))
    body, h1, h2 = styles["BodyCV"], styles["H1CV"], styles["H2CV"]

    document = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=2 * cm, leftMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=1.8 * cm, title="Relatório Applied Computer Vision - Quem Faz", author="Enzo Vazquez Sartorelli; Kaue Pastori Teixeira; Nicolas Nogueira Boni; Guilherme Brazioli; Pedro Oliveira Valotto")
    authors = "Enzo Vazquez Sartorelli - RM 94618<br/>Kaue Pastori Teixeira - RM 98501<br/>Nicolas Nogueira Boni - RM 551965<br/>Guilherme Brazioli - RM 98237<br/>Pedro Oliveira Valotto - RM 551445"
    story = [Spacer(1, 3.0 * cm), Paragraph("FIAP", styles["TitleCV"]), Paragraph("GLOBAL SOLUTION 2026.2", styles["Cover"]), Spacer(1, 1.0 * cm), Paragraph("QUEM FAZ", styles["TitleCV"]), Paragraph("Applied Computer Vision - Detecção Inteligente de EPIs", styles["Cover"]), Spacer(1, 1.2 * cm), Paragraph("Professores: Arnaldo Viana e Paulo Rodrigues", styles["Cover"]), Spacer(1, 0.35 * cm), Paragraph(authors, styles["Cover"]), Spacer(1, 1.6 * cm), Paragraph("11 de novembro de 2026", styles["Cover"]), PageBreak()]

    story += [Paragraph("Resumo", h1), p(SUMMARY, body), Paragraph("Palavras-chave", h2), p("visão computacional; detecção de objetos; EPI; YOLO; segurança do trabalho; MVP.", body), Paragraph("1. Objetivo", h1), p(OBJECTIVE, body), Paragraph("2. Problema e solução", h1), p("A observação de EPIs em imagens pode apoiar triagem visual, mas não comprova que um equipamento está corretamente vestido, adequado à atividade ou em boas condições. O MVP recebe uma imagem, executa detecção local e retorna caixas delimitadoras, classe e confiança. A decisão de segurança permanece humana.", body), Paragraph("3. Arquitetura", h1), p("A interface Streamlit chama o módulo de inferência. Este carrega o peso YOLO11n validado, processa a imagem em 416 pixels e devolve a imagem anotada e uma lista estruturada de detecções. Scripts separados preparam os dados, treinam, validam e processam vídeo localmente.", body), Paragraph("4. Dados e preparação", h1), p("Foi usado o Construction-PPE da Ultralytics, licenciado em CC BY 4.0. O dataset original não é redistribuído neste repositório. O script de preparação manteve apenas as classes helmet, vest e goggles e as remapeou para capacete, colete e oculos. Foram geradas 800 imagens para treino, 100 para validação e 100 para teste, com seed 42. O teste foi separado antes do treinamento.", body), PageBreak()]

    story += [Paragraph("5. Treinamento customizado", h1)]
    config = [["Parâmetro", "Valor"], ["Modelo", "YOLO11n pré-treinado"], ["Épocas", "5"], ["Resolução", "416 px"], ["Batch", "2"], ["Seed", "42"], ["Ambiente", "Windows, Python 3.12, PyTorch 2.7.1+cu118, RTX 3060"], ["Classes", "capacete, colete, oculos"]]
    table = Table(config, colWidths=[4.2 * cm, 11.6 * cm])
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#092E4D")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTNAME", (0, 1), (-1, -1), "Helvetica"), ("FONTSIZE", (0, 0), (-1, -1), 8.8), ("LEADING", (0, 0), (-1, -1), 11), ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#B0BEC5")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F7FA")]), ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    story += [table, Spacer(1, 0.35 * cm), p("A primeira tentativa de preparação de labels foi inválida por gravar o texto literal \\n; ela resultou em zero labels e foi descartada. Após correção, o experimento yolo11n_ppe3_fixed foi reexecutado e é a única origem dos resultados apresentados.", body), Paragraph("6. Resultados no teste holdout", h1)]
    metric_rows = [["Métrica", "Resultado"], ["Precisão", f"{METRICS['precision']:.4f}"], ["Recall", f"{METRICS['recall']:.4f}"], ["mAP@50", f"{METRICS['map50']:.4f}"], ["mAP@50-95", f"{METRICS['map50_95']:.4f}"]]
    metric_table = Table(metric_rows, colWidths=[5 * cm, 4 * cm])
    metric_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B5C8C")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#B0BEC5")), ("ALIGN", (1, 1), (1, -1), "RIGHT"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F7FA")]), ("PADDING", (0, 0), (-1, -1), 6)]))
    story += [metric_table, Spacer(1, 0.35 * cm), p("Por classe, o mAP@50-95 foi 0,4762 para capacete, 0,6141 para colete e 0,4068 para oculos. A validação registrou cerca de 9,1 ms de inferência por imagem já carregada. A inferência de exemplo, incluindo carregamento inicial do modelo, retornou um colete com confiança 0,2896 em 3.661,6 ms.", body)]
    story += figure(ROOT / "results" / "plots" / "training_curves.png", 16 * cm, "Figura 1 - Curvas do treinamento válido de cinco épocas.", styles)
    story += figure(ROOT / "results" / "plots" / "test_pr_curve.png", 14 * cm, "Figura 2 - Curva Precision-Recall no teste holdout.", styles)
    story += [PageBreak(), Paragraph("7. Evidência de inferência", h1)]
    story += figure(ROOT / "results" / "predictions" / "example_test_annotated.jpg", 16 * cm, "Figura 3 - Inferência real sobre imagem do holdout; a baixa confiança exibida é preservada como evidência, não selecionada como demonstração ideal.", styles)
    story += [Paragraph("8. Limitações e uso responsável", h1), p("O conjunto é limitado, o treinamento é curto e o desempenho varia por classe. Objetos pequenos, oclusão, iluminação, distância da câmera e diferenças entre o contexto do dataset e uma obra real podem reduzir a detecção. O sistema não reconhece uso correto, ajuste, estado de conservação ou todas as exigências de segurança. A saída deve ser revisada por pessoas qualificadas e não deve acionar decisão autônoma de segurança.", body), Paragraph("9. Reprodutibilidade", h1), p("O repositório contém scripts de preparação, treinamento, validação, interface, testes, peso validado, métricas JSON, gráficos e exemplo anotado. Imagens e labels não são versionados; a obtenção do dataset e sua licença estão documentadas em dataset/README.md. Para verificar o código: python -m unittest discover -s tests -v e python -m compileall -q src training tests.", body), Paragraph("10. Referências", h1), p("ULTRALYTICS. Construction-PPE Dataset. Documentação oficial, 2026. Disponível em: https://docs.ultralytics.com/datasets/detect/construction-ppe/. Acesso em: 11 nov. 2026.\nULTRALYTICS. Train Mode e Val Mode. Documentação oficial, 2026. Disponível em: https://docs.ultralytics.com/modes/train/ e https://docs.ultralytics.com/modes/val/. Acesso em: 11 nov. 2026.\nPYTORCH. Get Started Locally. Documentação oficial, 2026. Disponível em: https://pytorch.org/get-started/locally/. Acesso em: 11 nov. 2026.", body)]
    story += [PageBreak(), Paragraph("11. Conclusão", h1), p("Curso: Engenharia de Software. O MVP atingiu o objetivo de demonstrar detecção local de capacete, colete e óculos em imagens, com treinamento customizado, métricas reproduzíveis e interface verificável. As ferramentas empregadas foram Python 3.12, PyTorch, Ultralytics YOLO11n, OpenCV, Streamlit, ReportLab e CUDA. O desempenho do holdout sustenta a demonstração acadêmica, mas a solução requer validação adicional antes de qualquer uso operacional e permanece um apoio à inspeção humana.", body)]
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"PDF gerado: {OUT}")
    print(f"Palavras do resumo: {len(SUMMARY.split())}")


if __name__ == "__main__":
    main()
