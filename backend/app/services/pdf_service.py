"""
PDF Report Generation Service using ReportLab.
Generates professional forensic reports for deepfake analysis.
"""
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

from app.core.config import settings


# Color palette
COLORS = {
    'primary': colors.HexColor('#6366F1'),      # Indigo
    'success': colors.HexColor('#10B981'),      # Green
    'warning': colors.HexColor('#F59E0B'),      # Amber
    'error': colors.HexColor('#EF4444'),        # Red
    'dark': colors.HexColor('#1E293B'),         # Slate
    'muted': colors.HexColor('#64748B'),        # Slate muted
    'light': colors.HexColor('#F1F5F9'),        # Light gray
}


def get_verdict_color(score: float) -> colors.Color:
    """Get color based on suspicion score."""
    if score < 0.3:
        return COLORS['success']
    elif score < 0.7:
        return COLORS['warning']
    return COLORS['error']


def get_verdict_text(score: float, label: str) -> tuple:
    """Get verdict text and description based on score."""
    if score < 0.3:
        return "LIKELY AUTHENTIC", "No significant manipulation indicators detected."
    elif score < 0.7:
        return "SUSPICIOUS", "Some anomalies detected. Manual review recommended."
    return "HIGHLY LIKELY FAKE", "Strong evidence of manipulation found."


class PDFReportGenerator:
    """Generates professional PDF reports for deepfake analysis."""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir or settings.STORAGE_PATH) / "reports"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=20,
            textColor=COLORS['dark'],
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='ReportSubtitle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=COLORS['muted'],
            alignment=TA_CENTER,
            spaceAfter=30
        ))
        
        self.styles.add(ParagraphStyle(
            name='DSSectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=COLORS['primary'],
            spaceBefore=20,
            spaceAfter=10
        ))
        
        self.styles.add(ParagraphStyle(
            name='DSBodyText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=COLORS['dark'],
            alignment=TA_JUSTIFY,
            spaceAfter=8
        ))
        
        self.styles.add(ParagraphStyle(
            name='DSVerdictText',
            parent=self.styles['Normal'],
            fontSize=18,
            alignment=TA_CENTER,
            spaceAfter=10
        ))
    
    def generate_report(
        self,
        job_id: str,
        overall_score: float,
        label: str,
        video_score: float = 0.0,
        audio_score: float = 0.0,
        lipsync_score: float = 0.0,
        segments: List[Dict] = None,
        summary_text: str = None,
        media_type: str = "video"
    ) -> str:
        """
        Generate a PDF report and return the file path.
        
        Returns:
            str: Path to the generated PDF file
        """
        segments = segments or []
        
        # Generate filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"deepfakeshield_report_{job_id[:8]}_{timestamp}.pdf"
        filepath = self.output_dir / filename
        
        # Create document
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build content
        story = []
        
        # Header
        story.extend(self._build_header(job_id))
        
        # Verdict Section
        story.extend(self._build_verdict_section(overall_score, label))
        
        # Modality Scores
        story.extend(self._build_modality_section(
            video_score, audio_score, lipsync_score, media_type
        ))
        
        # Flagged Segments
        if segments:
            story.extend(self._build_segments_section(segments))
        
        # Summary
        if summary_text:
            story.extend(self._build_summary_section(summary_text))
        
        # Recommendations
        story.extend(self._build_recommendations_section())
        
        # Limitations
        story.extend(self._build_limitations_section())
        
        # Footer
        story.extend(self._build_footer(job_id))
        
        # Build PDF
        doc.build(story)
        
        return str(filepath)
    
    def _build_header(self, job_id: str) -> List:
        """Build report header."""
        elements = []
        
        # Title
        elements.append(Paragraph(
            "🛡️ DeepFakeShield AI",
            self.styles['ReportTitle']
        ))
        
        elements.append(Paragraph(
            "Forensic Analysis Report",
            self.styles['ReportSubtitle']
        ))
        
        # Report metadata
        meta_data = [
            ["Report ID:", job_id[:8].upper()],
            ["Generated:", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")],
            ["Version:", "1.0.0"]
        ]
        
        meta_table = Table(meta_data, colWidths=[1.5*inch, 3*inch])
        meta_table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), COLORS['muted']),
            ('TEXTCOLOR', (1, 0), (1, -1), COLORS['dark']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        elements.append(meta_table)
        elements.append(Spacer(1, 20))
        elements.append(HRFlowable(width="100%", thickness=1, color=COLORS['light']))
        
        return elements
    
    def _build_verdict_section(self, score: float, label: str) -> List:
        """Build verdict section with score visualization."""
        elements = []
        
        elements.append(Paragraph("Analysis Verdict", self.styles['DSSectionHeader']))
        
        verdict_text, verdict_desc = get_verdict_text(score, label)
        verdict_color = get_verdict_color(score)
        
        # Verdict box
        verdict_style = ParagraphStyle(
            'VerdictBox',
            parent=self.styles['DSVerdictText'],
            textColor=verdict_color
        )
        
        elements.append(Paragraph(verdict_text, verdict_style))
        elements.append(Paragraph(verdict_desc, self.styles['DSBodyText']))
        elements.append(Spacer(1, 10))
        
        # Score display
        score_pct = int(score * 100)
        score_data = [
            ["Suspicion Score:", f"{score_pct}%"],
            ["Classification:", label or "N/A"]
        ]
        
        score_table = Table(score_data, colWidths=[2*inch, 2*inch])
        score_table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('TEXTCOLOR', (0, 0), (0, -1), COLORS['muted']),
            ('TEXTCOLOR', (1, 0), (1, -1), verdict_color),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(score_table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _build_modality_section(
        self,
        video_score: float,
        audio_score: float,
        lipsync_score: float,
        media_type: str
    ) -> List:
        """Build modality analysis section."""
        elements = []
        
        elements.append(Paragraph("Modality Analysis", self.styles['DSSectionHeader']))
        
        # Build table
        header = ["Modality", "Score", "Status"]
        
        def get_status(score):
            if score < 0.3:
                return "✓ Normal"
            elif score < 0.7:
                return "⚠ Suspicious"
            return "✕ Anomaly"
        
        data = [header]
        
        if media_type in ["video", "image"]:
            data.append(["🎬 Video/Image Analysis", f"{int(video_score*100)}%", get_status(video_score)])
        
        if media_type in ["video", "audio"]:
            data.append(["🔊 Audio Analysis", f"{int(audio_score*100)}%", get_status(audio_score)])
        
        if media_type == "video":
            data.append(["👄 Lip-Sync Verification", f"{int(lipsync_score*100)}%", get_status(lipsync_score)])
        
        table = Table(data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), COLORS['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            # Body
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BACKGROUND', (0, 1), (-1, -1), COLORS['light']),
            ('TEXTCOLOR', (0, 1), (-1, -1), COLORS['dark']),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _build_segments_section(self, segments: List[Dict]) -> List:
        """Build flagged segments section."""
        elements = []
        
        elements.append(Paragraph("Flagged Segments", self.styles['DSSectionHeader']))
        elements.append(Paragraph(
            "The following segments were identified as potentially manipulated:",
            self.styles['DSBodyText']
        ))
        
        header = ["Time", "Type", "Score", "Reason"]
        data = [header]
        
        for seg in segments[:10]:  # Limit to 10 segments
            start_ms = seg.get('start_ms', 0)
            end_ms = seg.get('end_ms', 0)
            time_str = f"{start_ms/1000:.1f}s - {end_ms/1000:.1f}s"
            
            data.append([
                time_str,
                seg.get('segment_type', 'unknown').capitalize(),
                f"{int(seg.get('score', 0)*100)}%",
                seg.get('reason', 'N/A')[:40]
            ])
        
        table = Table(data, colWidths=[1.2*inch, 1*inch, 0.8*inch, 3*inch])
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), COLORS['warning']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            # Body
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BACKGROUND', (0, 1), (-1, -1), COLORS['light']),
            ('TEXTCOLOR', (0, 1), (-1, -1), COLORS['dark']),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _build_summary_section(self, summary_text: str) -> List:
        """Build summary section."""
        elements = []
        
        elements.append(Paragraph("Analysis Summary", self.styles['DSSectionHeader']))
        
        # Split summary into paragraphs
        for para in summary_text.split('\n\n'):
            if para.strip():
                elements.append(Paragraph(para.strip(), self.styles['DSBodyText']))
        
        elements.append(Spacer(1, 10))
        
        return elements
    
    def _build_recommendations_section(self) -> List:
        """Build recommendations section."""
        elements = []
        
        elements.append(Paragraph("Recommended Next Steps", self.styles['DSSectionHeader']))
        
        recommendations = [
            "1. <b>Verify the source</b> - Check the original publication source and chain of custody.",
            "2. <b>Request original file</b> - Compressed versions may affect analysis accuracy.",
            "3. <b>Cross-reference</b> - Compare with known authentic media from the same source.",
            "4. <b>Consult experts</b> - For high-stakes decisions, consider professional forensic review."
        ]
        
        for rec in recommendations:
            elements.append(Paragraph(rec, self.styles['DSBodyText']))
        
        elements.append(Spacer(1, 10))
        
        return elements
    
    def _build_limitations_section(self) -> List:
        """Build limitations section."""
        elements = []
        
        elements.append(Paragraph("⚠️ Important Limitations", self.styles['DSSectionHeader']))
        
        limitations = [
            "• AI detection is not 100% accurate and should not be the sole basis for conclusions.",
            "• Results should be considered alongside other evidence and context.",
            "• Detection performance may vary with video compression, quality, and resolution.",
            "• Novel deepfake techniques may not be detected by current models.",
            "• This report is for informational purposes and does not constitute legal advice."
        ]
        
        for lim in limitations:
            elements.append(Paragraph(lim, self.styles['DSBodyText']))
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _build_footer(self, job_id: str) -> List:
        """Build report footer."""
        elements = []
        
        elements.append(HRFlowable(width="100%", thickness=1, color=COLORS['light']))
        elements.append(Spacer(1, 10))
        
        footer_text = f"""
        <para align="center">
        <font size="8" color="{COLORS['muted']}">
        Generated by DeepFakeShield AI | Report ID: {job_id[:8].upper()} | 
        {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}
        <br/>
        This report was generated automatically and should be reviewed by qualified personnel.
        </font>
        </para>
        """
        
        elements.append(Paragraph(footer_text, self.styles['Normal']))
        
        return elements


# Singleton instance
pdf_generator = PDFReportGenerator()


def generate_pdf_report(
    job_id: str,
    overall_score: float,
    label: str,
    video_score: float = 0.0,
    audio_score: float = 0.0,
    lipsync_score: float = 0.0,
    segments: List[Dict] = None,
    summary_text: str = None,
    media_type: str = "video"
) -> str:
    """
    Generate a PDF report for the given analysis results.
    
    Returns:
        str: Path to the generated PDF file
    """
    return pdf_generator.generate_report(
        job_id=job_id,
        overall_score=overall_score,
        label=label,
        video_score=video_score,
        audio_score=audio_score,
        lipsync_score=lipsync_score,
        segments=segments,
        summary_text=summary_text,
        media_type=media_type
    )
