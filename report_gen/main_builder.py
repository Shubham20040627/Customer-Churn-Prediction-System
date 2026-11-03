"""
Master Builder: Compiles and generates both NoSQL_Project_Report.docx and PROJECT_REPORT.md.
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from report_gen.doc_utils import add_header_footer
from report_gen.cover_and_intro import build_cover_page, build_front_matter, build_chapter_1
from report_gen.literature_and_objectives import build_chapter_2, build_chapter_3
from report_gen.dataset_and_design import build_chapter_4, build_chapter_5
from report_gen.code_and_results import build_chapter_6, build_chapter_7
from report_gen.conclusion_viva_refs import build_chapter_8, build_chapter_9, build_chapter_10
from report_gen.md_generator import generate_markdown

def generate_docx():
    print("=" * 65)
    print("GENERATING 30+ PAGE WORD REPORT: NoSQL_Project_Report.docx")
    print("=" * 65)
    
    doc = Document()
    add_header_footer(doc)
    
    print("[1/10] Building Cover Page...")
    build_cover_page(doc)
    
    print("[2/10] Building Front Matter (Certificate, Declaration, Abstract, TOC)...")
    build_front_matter(doc)
    
    print("[3/10] Building Chapter 1: Introduction...")
    build_chapter_1(doc)
    
    print("[4/10] Building Chapter 2: Literature Survey...")
    build_chapter_2(doc)
    
    print("[5/10] Building Chapter 3: Project Objectives (5 SMART Objectives)...")
    build_chapter_3(doc)
    
    print("[6/10] Building Chapter 4: Dataset Analysis & NoSQL Schema Design...")
    build_chapter_4(doc)
    
    print("[7/10] Building Chapter 5: System Design & Methodology...")
    build_chapter_5(doc)
    
    print("[8/10] Building Chapter 6: Implementation & Code Listings (8 Visual Figures)...")
    build_chapter_6(doc)
    
    print("[9/10] Building Chapter 7: Results, Console Logs, and Discussion...")
    build_chapter_7(doc)
    
    print("[10/10] Building Chapter 8, 9, 10 (Conclusion, Viva Guide, References)...")
    build_chapter_8(doc)
    build_chapter_9(doc)
    build_chapter_10(doc)
    
    docx_path = os.path.join(BASE_DIR, "NoSQL_Project_Report_Final.docx")
    doc.save(docx_path)
    print(f"\n[SUCCESS] Word Document saved to: {docx_path}")
    print(f"File size: {os.path.getsize(docx_path):,} bytes")
    
    # Also attempt to save/overwrite NoSQL_Project_Report.docx if unlocked
    primary_path = os.path.join(BASE_DIR, "NoSQL_Project_Report.docx")
    try:
        doc.save(primary_path)
        print(f"[SUCCESS] Also updated primary Word Document: {primary_path}")
    except PermissionError:
        print(f"[NOTE] '{primary_path}' is currently locked by a viewer. Final version saved at: '{docx_path}'")
    
    return docx_path

if __name__ == "__main__":
    generate_docx()
    generate_markdown()
    print("\n" + "=" * 65)
    print("ALL REPORTS SUCCESSFULLY GENERATED (DOCX & MARKDOWN)!")
    print("=" * 65)
