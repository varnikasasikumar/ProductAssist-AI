import zipfile
from pathlib import Path

kb_dir = Path("../knowledge-base/CNC-X100")
kb_dir.mkdir(parents=True, exist_ok=True)

# 1. Create DOCX
docx_path = kb_dir / "spindle-assembly-guide.docx"
doc_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p><w:r><w:t>CNC-X100 Spindle Assembly Quick Reference Guide. Spindle taper BT40 requires periodic cleaning with ISO VG 32 oil.</w:t></w:r></w:p>
    <w:p><w:r><w:t>Tightening torque for spindle retaining collar bolts is 45 Nm.</w:t></w:r></w:p>
  </w:body>
</w:document>"""

with zipfile.ZipFile(docx_path, "w") as z:
    z.writestr("word/document.xml", doc_xml.encode("utf-8"))
    z.writestr("[Content_Types].xml", '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"></Types>')

# 2. Create HTML
html_path = kb_dir / "operator-safety-cheatsheet.html"
html_content = """<!DOCTYPE html>
<html>
<head><title>CNC-X100 Operator Safety Cheatsheet</title></head>
<body>
<h1>CNC-X100 Operator Safety Cheatsheet</h1>
<p>Emergency Stop (E-Stop): Push mushroom head button on front right console to immediately drop 24V control power.</p>
<p>Protective Eye Wear (ANSI Z87.1) must be worn at all times near Bay A assembly line.</p>
</body>
</html>"""
html_path.write_text(html_content, encoding="utf-8")

# 3. Create CSV
csv_path = kb_dir / "spare-parts-inventory.csv"
csv_content = """Part Number,Description,Location,Replacement Interval
X100-FLT-002,Cabinet Air Filter Mat,Side Cabinet Door A,Monthly
X100-SEN-315,Temperature Sensor Probe,Spindle Housing,Annual
X100-PMP-101,Coolant Circulation Pump,Lower Rear Enclosure,2 Years
"""
csv_path.write_text(csv_content, encoding="utf-8")

print("Generated DOCX, HTML, and CSV multi-format knowledge files!")
