import os
import sys
import textwrap

class SimplePDFWriter:
    """
    A pure Python PDF 1.4 generator that creates clean, professional multi-page documents
    with headers, footers, page numbers, titles, headings, bullet points, and tables.
    """
    def __init__(self, title, doc_type="Manual", product="CNC Machine", model="CNC-X100"):
        self.title = title
        self.doc_type = doc_type
        self.product = product
        self.model = model
        self.pages = []
        self.current_commands = []
        self.y = 710
        self.margin_left = 54
        self.margin_right = 558
        self.page_width = 612
        self.page_height = 792

    def _start_new_page(self):
        if self.current_commands:
            self.pages.append(self.current_commands)
        self.current_commands = []
        self.y = 710

    def add_title(self, text):
        self._start_new_page()
        text_esc = self._escape_text(text)
        self.current_commands.append(f"0.1 0.25 0.55 rg BT /F2 18 Tf {self.margin_left} {self.y} Td ({text_esc}) Tj ET")
        self.y -= 26
        sub = f"Product: {self.product}  |  Model: {self.model}  |  Document Type: {self.doc_type}"
        sub_esc = self._escape_text(sub)
        self.current_commands.append(f"0.35 0.35 0.35 rg BT /F1 10 Tf {self.margin_left} {self.y} Td ({sub_esc}) Tj ET")
        self.y -= 20
        self.current_commands.append("0.8 0.8 0.85 RG 1.5 w 54 " + str(self.y) + " m 558 " + str(self.y) + " l S")
        self.y -= 25

    def add_h1(self, text):
        if self.y < 120:
            self._start_new_page()
        text_esc = self._escape_text(text)
        self.current_commands.append(f"0.1 0.2 0.5 rg BT /F2 14 Tf {self.margin_left} {self.y} Td ({text_esc}) Tj ET")
        self.y -= 20
        self.current_commands.append("0.85 0.85 0.9 RG 0.75 w 54 " + str(self.y) + " m 558 " + str(self.y) + " l S")
        self.y -= 15

    def add_h2(self, text):
        if self.y < 100:
            self._start_new_page()
        text_esc = self._escape_text(text)
        self.current_commands.append(f"0.2 0.3 0.5 rg BT /F2 11 Tf {self.margin_left} {self.y} Td ({text_esc}) Tj ET")
        self.y -= 16

    def add_paragraph(self, text):
        lines = textwrap.wrap(text, width=82)
        for line in lines:
            if self.y < 70:
                self._start_new_page()
            line_esc = self._escape_text(line)
            self.current_commands.append(f"0.15 0.15 0.15 rg BT /F1 9.5 Tf {self.margin_left} {self.y} Td ({line_esc}) Tj ET")
            self.y -= 13.5
        self.y -= 6

    def add_bullet(self, text):
        lines = textwrap.wrap(text, width=76)
        first = True
        for line in lines:
            if self.y < 70:
                self._start_new_page()
            line_esc = self._escape_text(line)
            bullet_prefix = "- " if first else "  "
            first = False
            self.current_commands.append(f"0.2 0.2 0.2 rg BT /F1 9.5 Tf {self.margin_left + 12} {self.y} Td ({bullet_prefix}{line_esc}) Tj ET")
            self.y -= 13
        self.y -= 3

    def add_warning_box(self, text):
        if self.y < 110:
            self._start_new_page()
        lines = textwrap.wrap(text, width=74)
        box_height = len(lines) * 13 + 14
        box_y = self.y - box_height + 10
        # Draw background and border
        self.current_commands.append(f"1.0 0.95 0.9 rg 54 {box_y} 504 {box_height} re f")
        self.current_commands.append(f"0.8 0.3 0.1 RG 1 w 54 {box_y} 504 {box_height} re s")
        self.current_commands.append(f"0.7 0.2 0.0 rg BT /F2 9.5 Tf 64 {self.y - 2} Td (WARNING / SAFETY PRECAUTION:) Tj ET")
        self.y -= 15
        for line in lines:
            line_esc = self._escape_text(line)
            self.current_commands.append(f"0.3 0.1 0.0 rg BT /F1 9 Tf 64 {self.y} Td ({line_esc}) Tj ET")
            self.y -= 13
        self.y -= 12

    def add_table_row(self, col1, col2, col3="", is_header=False):
        if self.y < 70:
            self._start_new_page()
        c1_esc = self._escape_text(col1[:25])
        c2_esc = self._escape_text(col2[:35])
        c3_esc = self._escape_text(col3[:35])
        
        font = "/F2" if is_header else "/F1"
        color = "0.1 0.2 0.4" if is_header else "0.15 0.15 0.15"
        
        if is_header:
            self.current_commands.append(f"0.9 0.92 0.96 rg 54 {self.y - 4} 504 16 re f")
            self.current_commands.append(f"0.7 0.75 0.85 RG 0.5 w 54 {self.y - 4} 504 16 re s")

        self.current_commands.append(f"{color} rg BT {font} 9 Tf 58 {self.y} Td ({c1_esc}) Tj ET")
        self.current_commands.append(f"{color} rg BT {font} 9 Tf 200 {self.y} Td ({c2_esc}) Tj ET")
        if col3:
            self.current_commands.append(f"{color} rg BT {font} 9 Tf 380 {self.y} Td ({c3_esc}) Tj ET")
        self.y -= 15

    def _escape_text(self, text):
        return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    def save(self, filepath):
        if self.current_commands:
            self.pages.append(self.current_commands)

        total_pages = len(self.pages)
        
        # Add headers and footers to each page
        final_pages_streams = []
        for idx, page_cmds in enumerate(self.pages, start=1):
            stream_cmds = []
            # Header
            header_text = self._escape_text(f"{self.product} {self.model} - {self.title}")
            stream_cmds.append(f"0.3 0.3 0.35 rg BT /F2 8.5 Tf 54 750 Td ({header_text}) Tj ET")
            stream_cmds.append("0.75 0.75 0.8 RG 0.5 w 54 742 m 558 742 l S")
            
            # Page content
            stream_cmds.extend(page_cmds)
            
            # Footer
            footer_page = self._escape_text(f"Page {idx} of {total_pages}")
            stream_cmds.append("0.75 0.75 0.8 RG 0.5 w 54 48 m 558 48 l S")
            stream_cmds.append(f"0.4 0.4 0.4 rg BT /F1 8.5 Tf 54 36 Td (ProductAssist AI Synthetic Knowledge Base - Demo Material Only) Tj ET")
            stream_cmds.append(f"0.4 0.4 0.4 rg BT /F1 8.5 Tf 490 36 Td ({footer_page}) Tj ET")
            
            stream_content = "\n".join(stream_cmds).encode("latin1")
            final_pages_streams.append(stream_content)

        # PDF Object structure construction
        pdf_objects = []
        
        # 1 0 obj: Catalog
        # 2 0 obj: Pages
        # 3 0 obj: Font Helvetica (F1)
        # 4 0 obj: Font Helvetica-Bold (F2)
        # 5.. 5+N-1: Page objects
        # 5+N.. 5+2N-1: Content stream objects

        num_pages = total_pages
        page_obj_start = 5
        content_obj_start = page_obj_start + num_pages

        page_refs = [f"{page_obj_start + i} 0 R" for i in range(num_pages)]
        
        catalog_obj = "1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj"
        pages_obj = f"2 0 obj\n<< /Type /Pages /Kids [{' '.join(page_refs)}] /Count {num_pages} >>\nendobj"
        f1_obj = "3 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj"
        f2_obj = "4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj"

        pdf_objects.extend([catalog_obj.encode("latin1"), pages_obj.encode("latin1"), f1_obj.encode("latin1"), f2_obj.encode("latin1")])

        for i in range(num_pages):
            p_num = page_obj_start + i
            c_num = content_obj_start + i
            p_obj = f"{p_num} 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {c_num} 0 R >>\nendobj"
            pdf_objects.append(p_obj.encode("latin1"))

        for i in range(num_pages):
            c_num = content_obj_start + i
            stream_data = final_pages_streams[i]
            c_obj = f"{c_num} 0 obj\n<< /Length {len(stream_data)} >>\nstream\n".encode("latin1") + stream_data + f"\nendstream\nendobj".encode("latin1")
            pdf_objects.append(c_obj)

        # Assemble PDF file with xref table
        header = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
        offsets = []
        current_offset = len(header)

        output_data = bytearray(header)
        for obj in pdf_objects:
            offsets.append(current_offset)
            output_data.extend(obj)
            output_data.extend(b"\n")
            current_offset = len(output_data)

        startxref = current_offset
        total_objects = len(pdf_objects) + 1

        xref = [f"xref\n0 {total_objects}\n0000000000 65535 f \n".encode("latin1")]
        for off in offsets:
            xref.append(f"{off:010d} 00000 n \n".encode("latin1"))

        trailer = f"trailer\n<< /Size {total_objects} /Root 1 0 R >>\nstartxref\n{startxref}\n%%EOF\n".encode("latin1")

        output_data.extend(b"".join(xref))
        output_data.extend(trailer)

        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(output_data)
        print(f"Generated PDF: {filepath} ({total_pages} pages)")
