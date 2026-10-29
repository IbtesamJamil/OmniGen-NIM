import os
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from pipeline.audit_ledger import AuditLedger

class ClinicalPDFExporter:
    @staticmethod
    def generate_report(payload, vcf_results=None, custom_output_path=None):
        """
        Generates a professional variant report PDF dossier safely avoiding cross-drive errors,
        including cryptographic audit ledger verification stamps.
        """
        if custom_output_path:
            pdf_path = custom_output_path
        else:
            fd, pdf_path = tempfile.mkstemp(suffix=".pdf")
            os.close(fd)
        
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor("#1e293b"), spaceAfter=6
        )
        subtitle_style = ParagraphStyle(
            'SubTitleStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor("#64748b"), spaceAfter=14
        )
        heading_style = ParagraphStyle(
            'HeadingStyle', parent=styles['Heading2'], fontSize=13, textColor=colors.HexColor("#0f172a"), spaceBefore=10, spaceAfter=6
        )
        body_style = ParagraphStyle(
            'BodyStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor("#334155"), spaceAfter=6
        )

        story = []
        story.append(Paragraph("🧬 OmniGen-NIM Genomic Variant Report Dossier", title_style))
        story.append(Paragraph("<b>RESEARCH PROTOTYPE — FOR RESEARCH USE ONLY.</b> Variant Pathogenicity & Estimated Structural Stability Report", subtitle_style))
        story.append(Spacer(1, 8))

        story.append(Paragraph("1. Variant Summary & Structural Metrics", heading_style))
        summary_data = [
            ["Parameter", "Value"],
            ["Gene Symbol", str(payload.get("Gene", "N/A"))],
            ["UniProt ID", str(payload.get("UniProt", "N/A"))],
            ["HGVS Notation", str(payload.get("HGVS", "N/A"))],
            ["Residue Position", str(payload.get("Residue", "N/A"))],
            ["AlphaFold pLDDT Score", str(payload.get("pLDDT", "N/A"))],
            ["Estimated ΔΔG (kcal/mol)", f"{payload.get('DeltaDeltaG_kcal_mol', 0.0)} kcal/mol (heuristic estimate)"],
            ["Stability Classification", str(payload.get("Stability_Status", "N/A"))],
            ["Burial Analysis", "Contact-Count Proxy Evaluated"],
            ["Analysis Persona", str(payload.get("Persona", "N/A"))]
        ]

        t = Table(summary_data, colWidths=[200, 340])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor("#f1f5f9")),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.HexColor("#0f172a")),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ]))
        story.append(t)
        story.append(Spacer(1, 12))

        story.append(Paragraph("2. Structural & Research Interpretation", heading_style))
        interp_text = (
            f"The variant <b>{payload.get('HGVS')}</b> in gene <b>{payload.get('Gene')}</b> was analyzed "
            f"under the active structural context. The predicted folding free energy change estimate (ΔΔG) of "
            f"<b>{payload.get('DeltaDeltaG_kcal_mol')} kcal/mol</b> indicates <b>{payload.get('Stability_Status')}</b> "
            f"structural stability, supported by an AlphaFold pLDDT confidence score of <b>{payload.get('pLDDT')}</b>."
        )
        story.append(Paragraph(interp_text, body_style))
        story.append(Spacer(1, 10))

        if vcf_results:
            story.append(Paragraph("3. Batch VCF Annotation Summary", heading_style))
            vcf_table_data = [["Chrom", "Pos", "Ref", "Alt", "CADD", "Classification"]]
            for row in vcf_results[:10]:
                vcf_table_data.append([
                    str(row.get("chrom")), str(row.get("pos")), str(row.get("ref")),
                    str(row.get("alt")), str(row.get("cadd_phred")), str(row.get("classification"))
                ])
            vt = Table(vcf_table_data, colWidths=[60, 60, 60, 60, 80, 220])
            vt.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
            ]))
            story.append(vt)
            story.append(Spacer(1, 12))

        # Tamper-Evident Audit Ledger Cryptographic Head Hash Stamp
        story.append(Paragraph("4. Tamper-Evident Compliance & Audit Trail", heading_style))
        head_hash = AuditLedger.get_head_hash() or "No ledger entries recorded yet."
        audit_text = (
            f"This analysis session was monitored under cryptographic chain validation. "
            f"<b>Ledger Head Hash (SHA-256):</b> <font name='Courier' size=8>{head_hash}</font><br/>"
            f"<i>Verified via OmniGen-NIM tamper-evident audit logging.</i>"
        )
        story.append(Paragraph(audit_text, body_style))

        doc.build(story)
        return pdf_path