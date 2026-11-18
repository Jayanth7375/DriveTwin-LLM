import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether, PageBreak
)
from reportlab.pdfgen import canvas

PDF_PATH = "d:/LLM Forge/I6_Engine_Physics_Formulas_and_Calculations.pdf"

class NumberedCanvas(canvas.Canvas):
    """
    Canvas to dynamically calculate and render page numbers (Page X of Y) and running header.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#4A5568"))

        # Header (Only on page 2 and later)
        if self._pageNumber > 1:
            self.drawString(54, 750, "I6 ENGINE DIAGNOSTIC SYSTEM — PHYSICS FORMULATION & MATHEMATICAL SPECIFICATION")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)

        # Footer (All pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)

        self.drawString(54, 32, "Confidential — Automotive Engineering & RAG PINN Architecture Specification")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_text)

        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    c_primary = colors.HexColor("#1A365D")    # Deep Navy
    c_secondary = colors.HexColor("#0D9488")  # Teal Accent
    c_dark = colors.HexColor("#2D3748")       # Body Text
    c_light = colors.HexColor("#F7FAFC")      # Table BG
    c_border = colors.HexColor("#E2E8F0")     # Border
    c_alert = colors.HexColor("#C53030")      # Red Alert

    # Custom Typography Styles
    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=c_primary,
        spaceAfter=6
    )

    style_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceAfter=15
    )

    style_h1 = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark,
        spaceAfter=6
    )

    style_formula = ParagraphStyle(
        'FormulaBox',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F1F5F9"),
        borderColor=colors.HexColor("#CBD5E1"),
        borderWidth=1,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6,
        borderRadius=4
    )

    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )

    style_table_cell_code = ParagraphStyle(
        'TableCellCode',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0D9488")
    )

    story = []

    # Title Block
    story.append(Paragraph("Inline-6 Engine Physics & Kinematics Specification", style_title))
    story.append(Paragraph("Comprehensive Mathematical Formulations, Kinematics, Thermodynamics & PyTorch PINN Loss Architecture", style_subtitle))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=0, spaceAfter=12))

    # Introduction / Overview Callout
    intro_text = (
        "<b>System Scope:</b> This document details all mathematical formulations, kinematic laws, "
        "fluid thermodynamic equations, and Physics-Informed Neural Network (PINN) loss metrics "
        "implemented in the 6.7L Diesel Inline 6-Cylinder (I6) Engine Diagnostic System. "
        "These formulas are processed in real-time by the Python physics feature extraction engine "
        "to compute a 14-dimensional feature vector for machine learning classification and RAG synthesis."
    )
    story.append(Paragraph(intro_text, style_body))
    story.append(Spacer(1, 8))

    # SECTION 1
    story.append(Paragraph("1. Crankshaft Kinematics & 120° Stroke Balance", style_h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=c_secondary, spaceBefore=0, spaceAfter=8))
    
    kinematic_intro = (
        "In a 4-stroke Inline-6 diesel engine, the crankshaft completes a full engine cycle over <b>720° of crank rotation</b>. "
        "Power strokes occur every <b>120° interval</b> across the firing order: <b>1 — 5 — 3 — 6 — 2 — 4</b>. "
        "Angular velocity fluctuations are measured per cylinder expansion stroke to evaluate torque contribution balance."
    )
    story.append(Paragraph(kinematic_intro, style_body))

    story.append(Paragraph("Cylinder Power Index (CPI) Formulation:", style_h2))
    story.append(Paragraph("CPI_i = ( Mean_Accel_Cyl_i - Mean_Accel_Overall ) / ( Std_Accel_Overall + 1e-6 )", style_formula))

    cpi_exp = (
        "Where <b>Mean_Accel_Cyl_i</b> is the mean crankshaft angular acceleration derivative "
        "<i>dω / dt</i> during Cylinder <i>i</i>'s expansion stroke window. "
        "A cylinder with normal combustion yields <b>CPI_i ≈ 0.0 to +1.0</b>. "
        "A misfiring or power-deficient cylinder yields <b>CPI_i < -1.5</b>."
    )
    story.append(Paragraph(cpi_exp, style_body))

    story.append(Paragraph("Overall Speed Fluctuation Index (SFI %):", style_h2))
    story.append(Paragraph("SFI (%) = ( StdDev(RPM) / ( Mean(RPM) + 1e-6 ) ) * 100", style_formula))
    
    sfi_exp = (
        "<b>Threshold Condition:</b> If <b>SFI < 8.0%</b>, primary crankshaft balance is nominal. "
        "If <b>SFI ≥ 8.0%</b>, an <code>UNBALANCED_VIBRATION</code> state is triggered."
    )
    story.append(Paragraph(sfi_exp, style_body))
    story.append(Spacer(1, 8))

    # SECTION 2
    story.append(Paragraph("2. Fluid Thermodynamics & Mass Airflow Modeling", style_h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=c_secondary, spaceBefore=0, spaceAfter=8))

    thermo_intro = (
        "Engine airflow dynamics are modeled using the Ideal Gas Law coupled with an empirical "
        "volumetric efficiency curve tailored for 6.7L turbocharged diesel engine platforms."
    )
    story.append(Paragraph(thermo_intro, style_body))

    story.append(Paragraph("Theoretical Ideal Mass Air Flow Rate (g/s):", style_h2))
    story.append(Paragraph("m_dot_theoretical (g/s) = [ ( V_d * (RPM / 60) * P_MAP * VE ) / ( 2 * R_air * T_IAT ) ] * 1000", style_formula))

    thermo_vars = (
        "• <b>V_d = 6.7 × 10⁻³ m³</b> (6.7 Liter Engine Displacement)<br/>"
        "• <b>P_MAP</b> = Manifold Absolute Pressure (Pa = kPa × 1000)<br/>"
        "• <b>T_IAT</b> = Intake Air Temperature in Kelvin (K = °C + 273.15)<br/>"
        "• <b>R_air = 287.05 J/(kg·K)</b> (Specific Gas Constant for dry air)<br/>"
        "• <b>VE (η_v)</b> = Non-linear Empirical Volumetric Efficiency"
    )
    story.append(Paragraph(thermo_vars, style_body))

    story.append(Paragraph("Empirical Volumetric Efficiency (VE / η_v) Map:", style_h2))
    story.append(Paragraph("VE = clip( 0.85 * exp( -0.5 * ( (RPM/4000) - 1.0 )² ) * [ 0.8 + 0.2 * tanh( (MAP/100) - 1.0 ) ], 0.40, 0.98 )", style_formula))

    story.append(Paragraph("Mass Airflow Residual Ratio (MAF Residual):", style_h2))
    story.append(Paragraph("MAF_Residual_Ratio = Mean( ( MAF_actual - m_dot_theoretical ) / ( m_dot_theoretical + 1e-6 ) )", style_formula))

    maf_diag = (
        "<b>Diagnostic Signatures:</b><br/>"
        "• <b>MAF_Residual > +0.15</b> (+15% overflow) → MAF Sensor Drift / Dirt Build-up (DTC P0101).<br/>"
        "• <b>MAF_Residual < -0.15</b> (-15% underflow) → Turbo Boost Air Leak / Charge Pipe Crack (DTC P0299)."
    )
    story.append(Paragraph(maf_diag, style_body))
    story.append(Spacer(1, 8))

    # SECTION 3
    story.append(Paragraph("3. Dual-Bank Lambda & Turbocharger Pressure Ratio", style_h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=c_secondary, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph("Dual-Bank Lambda Delta (Δλ):", style_h2))
    story.append(Paragraph("Lambda_Bank_Delta = Mean( | Lambda_Bank1 - Lambda_Bank2 | )", style_formula))
    
    lambda_info = (
        "Bank 1 monitors Cylinders 1–3; Bank 2 monitors Cylinders 4–6. "
        "Diesel engines operate lean (nominal λ between 1.2 and 2.2). "
        "A <b>Δλ > 0.15</b> indicates severe bank imbalance caused by clogged fuel injectors (DTC P0171/P0174)."
    )
    story.append(Paragraph(lambda_info, style_body))

    story.append(Paragraph("Turbocharger Boost Pressure Residual:", style_h2))
    story.append(Paragraph("Pressure_Ratio = P_MAP / 101.3 kPa\nExpected_PR = 1.0 + 1.2 * ( Wastegate_Duty / 100 )\nBoost_Residual = Mean( Pressure_Ratio - Expected_PR )", style_formula))

    story.append(Paragraph("Thermal Differential & Overheating Flag:", style_h2))
    story.append(Paragraph("Thermal_Delta (°C) = Mean( Oil_Temp - Coolant_Temp )\nOverheating_Flag = 1.0  IF  Max(Coolant_Temp) > 110.0°C  ELSE  0.0", style_formula))
    story.append(Spacer(1, 8))

    # SECTION 4
    story.append(Paragraph("4. 14-Dimensional Physics Feature Vector (X_physics)", style_h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=c_secondary, spaceBefore=0, spaceAfter=8))

    vector_desc = (
        "The unified physics extractor maps raw ECU log dataframes into a standardized "
        "14-element feature vector passed into the XGBoost/Random Forest ensemble and PyTorch PINN Transformer."
    )
    story.append(Paragraph(vector_desc, style_body))

    table_data = [
        [Paragraph("Index", style_table_header), Paragraph("Feature Name", style_table_header), Paragraph("Formula / Origin", style_table_header), Paragraph("Nominal Bounds", style_table_header)],
        [Paragraph("X₁", style_table_cell_code), Paragraph("CPI_Cyl_1", style_table_cell), Paragraph("Cylinder 1 Acceleration Deviation", style_table_cell), Paragraph("-1.0 to +1.0", style_table_cell)],
        [Paragraph("X₂", style_table_cell_code), Paragraph("CPI_Cyl_2", style_table_cell), Paragraph("Cylinder 2 Acceleration Deviation", style_table_cell), Paragraph("-1.0 to +1.0", style_table_cell)],
        [Paragraph("X₃", style_table_cell_code), Paragraph("CPI_Cyl_3", style_table_cell), Paragraph("Cylinder 3 Acceleration Deviation", style_table_cell), Paragraph("-1.0 to +1.0", style_table_cell)],
        [Paragraph("X₄", style_table_cell_code), Paragraph("CPI_Cyl_4", style_table_cell), Paragraph("Cylinder 4 Acceleration Deviation", style_table_cell), Paragraph("-1.0 to +1.0", style_table_cell)],
        [Paragraph("X₅", style_table_cell_code), Paragraph("CPI_Cyl_5", style_table_cell), Paragraph("Cylinder 5 Acceleration Deviation", style_table_cell), Paragraph("-1.0 to +1.0", style_table_cell)],
        [Paragraph("X₆", style_table_cell_code), Paragraph("CPI_Cyl_6", style_table_cell), Paragraph("Cylinder 6 Acceleration Deviation", style_table_cell), Paragraph("-1.0 to +1.0", style_table_cell)],
        [Paragraph("X₇", style_table_cell_code), Paragraph("Speed_Fluct_Index", style_table_cell), Paragraph("( StdDev(RPM) / Mean(RPM) ) * 100", style_table_cell), Paragraph("< 8.0%", style_table_cell)],
        [Paragraph("X₈", style_table_cell_code), Paragraph("MAF_Residual_Ratio", style_table_cell), Paragraph("( MAF_actual - m_dot_ideal ) / m_dot_ideal", style_table_cell), Paragraph("-0.15 to +0.15", style_table_cell)],
        [Paragraph("X₉", style_table_cell_code), Paragraph("Lambda_Bank_Delta", style_table_cell), Paragraph("Mean( | λ_B1 - λ_B2 | )", style_table_cell), Paragraph("< 0.15", style_table_cell)],
        [Paragraph("X₁₀", style_table_cell_code), Paragraph("Lambda_Bank1_Mean", style_table_cell), Paragraph("Mean( λ_B1 )", style_table_cell), Paragraph("1.20 to 2.20", style_table_cell)],
        [Paragraph("X₁₁", style_table_cell_code), Paragraph("Lambda_Bank2_Mean", style_table_cell), Paragraph("Mean( λ_B2 )", style_table_cell), Paragraph("1.20 to 2.20", style_table_cell)],
        [Paragraph("X₁₂", style_table_cell_code), Paragraph("Boost_Residual", style_table_cell), Paragraph("Pressure_Ratio - Expected_PR", style_table_cell), Paragraph("-0.20 to +0.20", style_table_cell)],
        [Paragraph("X₁₃", style_table_cell_code), Paragraph("Thermal_Delta_C", style_table_cell), Paragraph("Mean( Oil_Temp - Coolant_Temp )", style_table_cell), Paragraph("5.0°C to 15.0°C", style_table_cell)],
        [Paragraph("X₁₄", style_table_cell_code), Paragraph("Overheating_Flag", style_table_cell), Paragraph("1.0 IF Max(Coolant_Temp) > 110°C ELSE 0.0", style_table_cell), Paragraph("0.0 (Nominal)", style_table_cell)],
    ]

    t = Table(table_data, colWidths=[36, 110, 220, 138])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
    ]))

    story.append(t)
    story.append(Spacer(1, 10))

    # SECTION 5
    story.append(Paragraph("5. PyTorch Physics-Informed Loss Function (PINN Loss)", style_h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=c_secondary, spaceBefore=0, spaceAfter=8))

    pinn_math = (
        "The PyTorch PINN Transformer combines standard Cross-Entropy multi-class loss with "
        "physical conservation residual constraints during gradient optimization:"
    )
    story.append(Paragraph(pinn_math, style_body))

    story.append(Paragraph("L_PINN = L_CrossEntropy( y, y_hat ) + λ_air * L_airflow_residual + λ_torque * L_torque_balance", style_formula))

    pinn_details = (
        "• <b>L_CrossEntropy</b>: Multi-class classification loss across 8 diagnostic target classes.<br/>"
        "• <b>L_airflow_residual</b> = ‖ MAF_norm - ( MAP * RPM )_norm ‖₂² (Enforces ideal gas mass conservation).<br/>"
        "• <b>L_torque_balance</b> = ‖ ∑ᵢ₌₁⁶ CPI_i - 0.0 ‖₂² (Enforces zero net momentum angular impulse deviation)."
    )
    story.append(Paragraph(pinn_details, style_body))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated Physics PDF document:\n  -> {os.path.abspath(PDF_PATH)}")

if __name__ == "__main__":
    build_pdf()
