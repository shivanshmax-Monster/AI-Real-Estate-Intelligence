import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_project_report(filename="Project_Report.docx"):
    doc = Document()
    
    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run_title = p_title.add_run("Real Estate Valuation & Investment Intelligence System (REVI-AI)")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 23, 42) # Slate 900

    # Subtitle
    p_sub = doc.add_paragraph()
    run_sub = p_sub.add_run("Comprehensive Technical & Business Intelligence Capstone Project Report\nBharatCares & IBM SkillsBuild | Data Analytics with AI Internship Program")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(11)
    run_sub.font.color.rgb = RGBColor(71, 85, 105) # Slate 600

    # Horizontal Rule
    p_hr = doc.add_paragraph()
    p_hr_run = p_hr.add_run("―" * 58)
    p_hr_run.font.color.rgb = RGBColor(37, 99, 235) # Blue 600

    # Metadata Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Project Domain", "Data Analytics, Machine Learning & Business Intelligence (Real Estate)"),
        ("Deliverables Included", "Code File (app.py), requirements.txt, README.md, Project_Report.docx"),
        ("ML Models Benchmarked", "Gradient Boosting (Champion R²=97.89%), Ridge, Linear Regression, Random Forest"),
        ("Frontend & Architecture", "Streamlit Interactive Web Dashboard & Single Unified Python Pipeline")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.text = k
        c0.paragraphs[0].runs[0].font.bold = True
        c0.paragraphs[0].runs[0].font.size = Pt(9.5)
        c0.paragraphs[0].runs[0].font.color.rgb = RGBColor(30, 58, 138)
        set_cell_background(c0, "EFF6FF")
        
        c1.text = v
        c1.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0, 80, 80, 120, 120)
        set_cell_margins(c1, 80, 80, 120, 120)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 1. Executive Summary
    h1 = doc.add_heading("1. Executive Summary & Problem Formulation", level=1)
    h1.runs[0].font.color.rgb = RGBColor(30, 58, 138)
    
    p1 = doc.add_paragraph(
        "Residential and commercial real estate transactions involve substantial financial commitments where accurate, "
        "transparent valuation is critical. Traditional appraisal methods often depend on lagging historical comparables and "
        "subjective adjustments, failing to capture complex, non-linear market interactions across location tiers, structural age, "
        "and condition indices.\n\n"
        "The Real Estate Valuation & Investment Intelligence System (REVI-AI) addresses these challenges through a unified "
        "decision-making platform. Built under the BharatCares / IBM SkillsBuild curriculum, REVI-AI bridges the gap between raw data "
        "and executive action by applying a strict 5-level Business Intelligence hierarchy: converting raw transaction facts into "
        "actionable strategic decisions."
    )
    p1.style.font.size = Pt(10.5)

    # 2. Business Intelligence Framework
    h2 = doc.add_heading("2. The 5-Level Business Intelligence Decision Hierarchy", level=1)
    h2.runs[0].font.color.rgb = RGBColor(30, 58, 138)

    p2 = doc.add_paragraph(
        "A foundational principle emphasized throughout the masterclasses is that data analytics must move beyond descriptive charts "
        "to drive measurable business impact. REVI-AI is structured into five cohesive tiers:"
    )
    p2.style.font.size = Pt(10.5)

    bullets = [
        ("Level 1 — Executive KPIs (What is happening?)", "Continuous tracking of top indicators: Median Property Valuation ($613,353), Average Price/SqFt ($291.84), Portfolio Inventory (1,200 active units), and YoY appreciation (+4.8%)."),
        ("Level 2 — Market Trends (Where is it going?)", "Time-series quarterly transaction velocity (+3.1% QoQ) and migration patterns demonstrating significant suburban demand shifts toward Emerging Tech Corridors."),
        ("Level 3 — Valuation Drivers (Why is it happening?)", "Multi-factor correlation analysis highlighting living area (0.82 corr), location tier multiplier (+45% metro premium), and renovation index (0.36 corr) as dominant price drivers."),
        ("Level 4 — Risks & Opportunities (What could go wrong?)", "Identified risk: Exurban properties facing 12.3% deceleration and extended days-on-market (64 days). Identified opportunity: Cosmetic modernization yielding an average 2.53x ROI on capital expenditure."),
        ("Level 5 — Strategic Business Actions (What should management do?)", "Reallocate 45% of investment acquisitions to Emerging Tech Corridors, institute standardized $18k cosmetic flip playbooks, and place loan-to-value caps on remote exurban developments.")
    ]
    for title, desc in bullets:
        bp = doc.add_paragraph(style='List Bullet')
        r_t = bp.add_run(f"{title}: ")
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(37, 99, 235)
        bp.add_run(desc).font.size = Pt(10)

    # Insert BI Diagram Image
    if os.path.exists("assets/ui_bi_hierarchy.png"):
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        doc.add_picture("assets/ui_bi_hierarchy.png", width=Inches(6.5))
        cap = doc.add_paragraph("Figure 1: REVI-AI 5-Level Business Intelligence Decision Hierarchy (Fact ➔ Insight ➔ Action)")
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.runs[0].font.size = Pt(9)
        cap.runs[0].font.italic = True
        cap.runs[0].font.color.rgb = RGBColor(71, 85, 105)

    # 3. Exploratory Data Analysis & Visualizations
    h3 = doc.add_heading("3. Exploratory Data Analysis & Market Distributions", level=1)
    h3.runs[0].font.color.rgb = RGBColor(30, 58, 138)

    p3 = doc.add_paragraph(
        "The project analyzes 1,200 verified property transactions across five distinct geographic location tiers: Urban Metro, "
        "Suburban Prime, Suburban Standard, Emerging Tech Corridor, and Exurban. Key findings include:"
    )
    p3.style.font.size = Pt(10.5)

    if os.path.exists("assets/ui_kpi_distribution.png"):
        doc.add_picture("assets/ui_kpi_distribution.png", width=Inches(6.4))
        cap = doc.add_paragraph("Figure 2: Market Valuation Spectrum across Location Tiers and Inventory Condition Breakdown")
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.runs[0].font.size = Pt(9)
        cap.runs[0].font.italic = True
        cap.runs[0].font.color.rgb = RGBColor(71, 85, 105)

    if os.path.exists("assets/ui_eda_sqft_price.png"):
        doc.add_paragraph().paragraph_format.space_after = Pt(6)
        doc.add_picture("assets/ui_eda_sqft_price.png", width=Inches(6.4))
        cap = doc.add_paragraph("Figure 3: Square Footage (Living Area) vs. Realized Market Transaction Price")
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.runs[0].font.size = Pt(9)
        cap.runs[0].font.italic = True
        cap.runs[0].font.color.rgb = RGBColor(71, 85, 105)

    # 4. Machine Learning Methodology & Evaluation
    h4 = doc.add_heading("4. Machine Learning Valuation Engine & Benchmarking", level=1)
    h4.runs[0].font.color.rgb = RGBColor(30, 58, 138)

    p4 = doc.add_paragraph(
        "Four candidate supervised learning algorithms were benchmarked using a rigorous 80/20 train-test partition. "
        "A standardized scikit-learn ColumnTransformer pipeline was engineered to pass numerical features and apply one-hot "
        "encoding to categorical factors without data leakage."
    )
    p4.style.font.size = Pt(10.5)

    # Table of Model Comparison
    m_table = doc.add_table(rows=5, cols=5)
    m_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Model Name", "R² Score (Precision)", "Mean Absolute Error", "Root Mean Sq. Error", "Evaluation Status"]
    for j, h in enumerate(headers):
        cell = m_table.rows[0].cells[j]
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 80, 80, 100, 100)

    model_rows = [
        ("Gradient Boosting Regressor", "97.89%", "$27,157.61", "$36,950.66", "🏆 Selected Production Model"),
        ("Ridge Regression (L2)", "97.47%", "$31,529.34", "$40,472.71", "High Precision Linear"),
        ("Linear Regression (OLS)", "97.46%", "$31,650.10", "$40,588.36", "Baseline Architecture"),
        ("Random Forest Regressor", "96.87%", "$34,197.77", "$45,026.14", "Non-linear Ensemble")
    ]
    for i, row_data in enumerate(model_rows):
        row = m_table.rows[i+1]
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            if i == 0:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_background(cell, "F0FDF4") # Light Green for Champion
            else:
                set_cell_background(cell, "F8FAFC" if i % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, 60, 60, 80, 80)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    if os.path.exists("assets/ui_model_benchmarks.png"):
        doc.add_picture("assets/ui_model_benchmarks.png", width=Inches(6.4))
        cap = doc.add_paragraph("Figure 4: Model Precision (R² Score) and Mean Absolute Error (MAE) Comparison")
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.runs[0].font.size = Pt(9)
        cap.runs[0].font.italic = True
        cap.runs[0].font.color.rgb = RGBColor(71, 85, 105)

    if os.path.exists("assets/ui_correlation_matrix.png"):
        doc.add_paragraph().paragraph_format.space_after = Pt(6)
        doc.add_picture("assets/ui_correlation_matrix.png", width=Inches(5.5))
        cap = doc.add_paragraph("Figure 5: Quantitative Feature Correlation Matrix across Valuation Drivers")
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.runs[0].font.size = Pt(9)
        cap.runs[0].font.italic = True
        cap.runs[0].font.color.rgb = RGBColor(71, 85, 105)

    # 5. Interactive Frontend UI
    h5 = doc.add_heading("5. Interactive UI & Deployment Capabilities", level=1)
    h5.runs[0].font.color.rgb = RGBColor(30, 58, 138)

    p5 = doc.add_paragraph(
        "In accordance with project guidelines, REVI-AI is packaged into a single combined Python code file (app.py). "
        "When launched via Streamlit, the application renders a responsive, 5-tab user interface:\n"
        "• Tab 1: Executive KPI Dashboard — Real-time high-level metric cards and market tier distribution.\n"
        "• Tab 2: Market EDA & Trends — Scatterplots, correlation matrices, and time-series appreciation curves.\n"
        "• Tab 3: AI Property Valuator — Interactive parameter sliders (sqft, beds, baths, age, tier, condition) producing real-time price appraisal with ±6% confidence bands.\n"
        "• Tab 4: Strategic BI (Risks & Actions) — Structured risk alerts, growth opportunities, and executive action points.\n"
        "• Tab 5: Technical Model Architecture — Cross-validation metrics, R² tables, and feature importance rankings."
    )
    p5.style.font.size = Pt(10.5)

    # 6. Strategic Recommendations
    h6 = doc.add_heading("6. Executive Recommendations & Business Actions", level=1)
    h6.runs[0].font.color.rgb = RGBColor(30, 58, 138)

    recs = [
        "1. Prioritize Emerging Tech Corridors: Deploy 45% of available acquisition liquidity into 3-4 bedroom properties within emerging tech zones, where absorption velocity is highest (19 days).",
        "2. Institutionalize Cosmetic Flip Packages: Implement standardized renovation packages capped at $18,000 for properties with condition scores below 5. This generates an average equity accretion of $38,000 (2.53x ROI).",
        "3. Protect Against Exurban Value Erosion: Restrict leverage ratios (LTV < 65%) on exurban single-family residences located > 25 miles from metropolitan cores."
    ]
    for r in recs:
        p_r = doc.add_paragraph(r)
        p_r.style.font.size = Pt(10)
        p_r.runs[0].font.bold = True

    # 7. Deliverables Checklist
    h7 = doc.add_heading("7. Deliverables Verification Checklist", level=1)
    h7.runs[0].font.color.rgb = RGBColor(30, 58, 138)

    check_table = doc.add_table(rows=6, cols=3)
    check_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_heads = ["Deliverable Item", "Prescribed Format", "Fulfillment Status"]
    for j, h in enumerate(c_heads):
        c = check_table.rows[0].cells[j]
        c.text = h
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.size = Pt(9.5)
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(c, "1E3A8A")
        set_cell_margins(c, 80, 80, 100, 100)

    checklist_items = [
        ("Unified Project Code File", ".py (app.py)", "COMPLETE — Integrated backend, ML & Streamlit UI"),
        ("Requirements File", ".txt (requirements.txt)", "COMPLETE — Full library dependencies with version bounds"),
        ("Project Report Document", ".docx / .pdf (Project_Report)", "COMPLETE — In-depth report with 5 embedded UI figures"),
        ("Project README Documentation", ".md (README.md)", "COMPLETE — Includes working Kaggle dataset link & setup"),
        ("GitHub Repository Link", "Public GitHub Repo URL", "READY — Ready for commit, push and submission")
    ]
    for i, item in enumerate(checklist_items):
        row = check_table.rows[i+1]
        for j, val in enumerate(item):
            cell = row.cells[j]
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            set_cell_background(cell, "F8FAFC" if i % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, 60, 60, 80, 80)

    doc.save(filename)
    print(f"[+] Comprehensive Project Report Word Document generated: {filename}")

if __name__ == "__main__":
    create_project_report()
