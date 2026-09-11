import os
import sys

# Ensure local module import works
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_knowledge_base import SimplePDFWriter

BASE_KB_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------
# CNC-X100 DOCS
# ----------------------------------------------------------------------
CNC_DIR = os.path.join(BASE_KB_DIR, "CNC-X100")

def build_cnc_operation_manual():
    pdf = SimplePDFWriter("Operation Manual", doc_type="OPERATION_MANUAL", product="CNC Machine", model="CNC-X100")
    pdf.add_title("CNC-X100 Vertical Machining Center Operation Manual")
    
    pdf.add_h1("1. System Overview & Control Panel Usage")
    pdf.add_paragraph("The CNC-X100 is a high-precision 3-axis vertical machining center engineered for heavy-duty production milling and drilling operations in industrial enterprise facilities. The machine is controlled via a 15-inch Touchscreen HMI panel running the ProductAssist OS interface.")
    pdf.add_paragraph("The control panel consists of the primary touch display, emergency stop button, cycle start/hold buttons, manual pulse generator (MPG), mode selector dial (AUTO / MDA / JOG), and spindle speed override dial (0% to 150%).")
    pdf.add_bullet("Touchscreen HMI: Displays real-time axis positions (G54-G59), active modal G-codes, tool offset table, coolant flow rate telemetry, and system alarm logs.")
    pdf.add_bullet("Cycle Start Button (Green): Initiates automatic execution of loaded G-code programs.")
    pdf.add_bullet("Feed Hold Button (Red): Pauses axis feed motion immediately without stopping spindle rotation or turning off coolant flow.")
    pdf.add_bullet("Spindle Speed Override Dial: Allows real-time operator adjustment of spindle RPM between 0% and 150% during cutting cycles.")

    pdf.add_h1("2. Network Configuration & Connectivity")
    pdf.add_paragraph("The CNC-X100 features dual 1000BASE-T Ethernet ports located on the rear electrical cabinet door for integration with enterprise shopfloor networks and ProductAssist AI monitoring agents.")
    pdf.add_paragraph("To configure network settings, navigate to Menu > Settings > System > Network Configuration on the control panel:")
    pdf.add_bullet("IP Allocation: Static IP (Recommended for automated telemetry monitoring).")
    pdf.add_bullet("Default Static IP Address: 192.168.1.150  |  Subnet Mask: 255.255.255.0")
    pdf.add_bullet("Gateway Address: 192.168.1.1  |  DNS Server: 192.168.1.10")
    pdf.add_bullet("Modbus TCP (Port 502): Transmits real-time sensor telemetry including spindle load, coolant pressure, and axis vibration to PLC monitoring hubs.")
    pdf.add_bullet("OPC UA Server (Port 4840): Provides standardized machine state, operational mode, and fault alarm history to shopfloor SCADA applications.")
    pdf.add_bullet("MTConnect Agent (Port 5000): Streams XML execution metrics and part completion counts for manufacturing execution tracking.")

    pdf.add_h1("3. Pre-Start Inspection & Daily Startup Procedure")
    pdf.add_paragraph("Operators must complete the standard 5-step daily startup routine prior to machining production parts:")
    pdf.add_bullet("Step 1: Perform visual pre-start check of machine enclosure, clean chips from way covers, and verify coolant fluid level sight glass reads above 75% capacity.")
    pdf.add_bullet("Step 2: Turn ON main power circuit disconnect switch located on the rear electrical cabinet.")
    pdf.add_bullet("Step 3: Release the red mushroom Emergency Stop button on the operator panel by twisting clockwise.")
    pdf.add_bullet("Step 4: Press the Power On button on the control panel and wait 45 seconds for system boot.")
    pdf.add_bullet("Step 5: Perform Axis Homing routine by selecting HOME mode and pressing CYCLE START to establish reference zero for X, Y, and Z axes (G28).")

    pdf.add_h1("4. Machine Operation, Program Execution & Tooling")
    pdf.add_paragraph("Standard workpiece setup, tool management, and program execution procedure:")
    pdf.add_bullet("1. Load G-code program via USB drive or network share into memory location /NC_PROG/PART_01.NC.")
    pdf.add_bullet("2. Mount workpiece securely in pneumatic vise and probe work coordinate origin using edge finder or touch probe (G54).")
    pdf.add_bullet("3. Perform tool length offset measurement using laser tool setter for active tools in 24-pocket BT40 ATC magazine.")
    pdf.add_bullet("4. Select AUTO mode, enable single-block mode for initial dry-run verification, and press CYCLE START.")
    pdf.add_bullet("5. Monitor spindle load meter and coolant flow rate during initial cutting pass.")

    pdf.add_h1("5. Shutdown Procedures & Alarm Recording")
    pdf.add_paragraph("Standard Shutdown Procedure:")
    pdf.add_bullet("Move axes to safe home position (G28 X0 Y0 Z0). Stop spindle and turn OFF coolant pump.")
    pdf.add_bullet("Navigate to Menu > System > Shutdown on HMI and select Confirm. Turn OFF main electrical disconnect breaker.")
    pdf.add_paragraph("Alarm Recording Protocol:")
    pdf.add_bullet("Whenever an alarm code (e.g. E105, E210, E315, E420) triggers during operation, the operator must log the alarm code, active tool number, G-code line, and axis positions into the shift maintenance log.")

    pdf.add_warning_box("In case of tool crash, severe vibration, or coolant line rupture, hit the red Emergency Stop button immediately. Never reach inside enclosure while spindle is rotating.")

    pdf.save(os.path.join(CNC_DIR, "operation-manual.pdf"))


def build_cnc_installation_guide():
    pdf = SimplePDFWriter("Installation Guide", doc_type="INSTALLATION_GUIDE", product="CNC Machine", model="CNC-X100")
    pdf.add_title("CNC-X100 Vertical Machining Center Installation Guide")

    pdf.add_h1("1. Site Preparation & Environmental Requirements")
    pdf.add_paragraph("Proper site preparation ensures long-term machining positioning accuracy, operator safety, and structural machine stability.")
    pdf.add_bullet("Foundation Requirement: Heavy-duty reinforced concrete pad with minimum thickness of 200 mm (8 inches).")
    pdf.add_bullet("Floor Load Rating: Minimum load-bearing capacity of 3,500 kg/m^2.")
    pdf.add_bullet("Service Access Clearance: Minimum 1.0 meter (3.3 feet) open clearance around machine rear and sides for maintenance access.")
    pdf.add_bullet("Operating Ambient Temperature: +15°C to +35°C (+59°F to +95°F). Optimal operating temperature: 20°C ±2°C.")
    pdf.add_bullet("Relative Humidity: 30% to 80% non-condensing.")
    pdf.add_bullet("Vibration Isolation: Keep machine at least 15 meters away from stamping presses, forging hammers, or heavy overhead cranes.")

    pdf.add_h1("2. Uncrating, Rigging & Machine Leveling")
    pdf.add_paragraph("Unpacking and hoisting procedures must be performed by certified industrial rigging personnel:")
    pdf.add_paragraph("1. Use an overhead crane (minimum 5-ton capacity) or 5-ton forklift to position machine over concrete pad.")
    pdf.add_paragraph("2. Install six heavy-duty steel leveling pads beneath base casting adjustment bolts.")
    pdf.add_paragraph("3. Place precision spirit level (0.02 mm/m sensitivity) on ground table surface.")
    pdf.add_paragraph("4. Adjust leveling bolts until table is level within 0.02 mm/m across both X and Y directions.")

    pdf.add_h1("3. Electrical Installation & Grounding Requirements")
    pdf.add_paragraph("Electrical installation must comply with national electrical codes and industrial facility safety standards:")
    pdf.add_bullet("Input Power Supply: 3-Phase AC 400V ±10%, 50/60 Hz.")
    pdf.add_bullet("Total Connected Electrical Load: 35 kVA. Full load current rating: 48 Amps.")
    pdf.add_bullet("Main Power Cable: 4-core copper cable, minimum cross-section 16 mm^2.")
    pdf.add_bullet("Circuit Breaker Rating: Recommended 63 Amp 3-pole circuit breaker with residual current circuit breaker (RCCB).")
    pdf.add_bullet("Control Voltage: 24V DC regulated internal power supply.")
    pdf.add_bullet("Earth Grounding: Dedicated ground rod with ground resistance less than 5 Ohms. Do not share ground line with arc welders.")

    pdf.add_h1("4. Compressed Air & Coolant System Setup")
    pdf.add_paragraph("Connect facility compressed air line to pneumatic regulator FRL unit at rear of machine:")
    pdf.add_bullet("Pneumatic Operating Pressure Range: 6.0 bar to 8.0 bar (87 psi to 116 psi). Recommended nominal pressure: 6.5 bar.")
    pdf.add_bullet("Air Flow Rate: Minimum 250 Liters/minute continuous clean flow.")
    pdf.add_bullet("Air Quality & Filtration: 5-micron filter with automatic water condensate drain.")
    pdf.add_bullet("Air Pressure Warning: Pressure below 6.0 bar will trigger pneumatic interlock fault and prevent tool unclamping cycles.")
    pdf.add_bullet("Coolant Tank Setup: Fill 200-Liter tank with 6% water-soluble synthetic coolant emulsion to 80% fill mark.")

    pdf.add_h1("5. Initial Setup & Post-Installation Commissioning")
    pdf.add_paragraph("Before applying axis drive power, complete initial calibration checks:")
    pdf.add_bullet("Remove red shipping transit locking brackets from Z-axis ball screw and tool changer arm.")
    pdf.add_bullet("Fill automatic central lubrication reservoir with ISO VG 68 slide-way oil.")
    pdf.add_bullet("Perform spindle runout check using dial test indicator (maximum allowable runout 0.003 mm).")
    pdf.add_bullet("Execute laser interferometer pitch error compensation calibration routine.")

    pdf.add_warning_box("Verify correct 3-phase phase rotation before turning on spindle. Incorrect phase rotation will reverse coolant pump and chip conveyor motors.")

    pdf.save(os.path.join(CNC_DIR, "installation-guide.pdf"))


def build_cnc_troubleshooting_guide():
    pdf = SimplePDFWriter("Troubleshooting Guide", doc_type="TROUBLESHOOTING", product="CNC Machine", model="CNC-X100")
    pdf.add_title("CNC-X100 Diagnostic & Troubleshooting Guide")

    pdf.add_h1("1. Diagnostic Overview & Alarm System")
    pdf.add_paragraph("The CNC-X100 control unit monitors telemetry sensors continuously. When abnormal operating conditions occur, an alarm code is generated on the touchscreen HMI and logged into the system diagnostics table.")

    pdf.add_h1("2. Error Code Diagnostic & Resolution Procedures")

    # Error E105
    pdf.add_h2("Error Code E105 - Cooling System Malfunction")
    pdf.add_paragraph("Description: Coolant flow sensor detects flow rate below 8.0 L/min, or coolant pump thermal overload relay Q4 has tripped.")
    pdf.add_bullet("Symptoms: Alarm banner on HMI, coolant pump stops, spindle power output limited, high temperature warning.")
    pdf.add_bullet("Possible Causes: Low coolant level in 200L reservoir, clogged intake screen basket, damaged pump impeller, kinked delivery hose, or tripped Q4 circuit breaker.")
    pdf.add_bullet("Diagnostic Checks: Inspect coolant sight glass on reservoir tank; check flow meter FM-1 output on diagnostic screen; inspect circuit breaker Q4 in electrical cabinet.")
    pdf.add_bullet("Recommended Corrective Actions: 1. Top up coolant emulsion to 80% level. 2. Remove intake screen filter basket and flush debris with compressed air. 3. Reset thermal relay Q4. 4. Replace pump motor if winding resistance is unbalanced.")
    pdf.add_warning_box("SAFETY: Turn OFF electrical power before opening cabinet or servicing coolant pump. Wear chemical-resistant safety gloves and safety goggles.")

    # Error E210
    pdf.add_h2("Error Code E210 - Spindle Overload Warning")
    pdf.add_paragraph("Description: Main spindle motor current exceeds 120% of rated continuous output for greater than 5 consecutive seconds.")
    pdf.add_bullet("Symptoms: Spindle speed drops under heavy load, chatter marks on workpiece, E210 alarm displays on screen.")
    pdf.add_bullet("Possible Causes: Excessive depth of cut, dull or chipped cutting inserts, hard spots in workpiece material, spindle bearing mechanical binding, or incorrect feed rate.")
    pdf.add_bullet("Diagnostic Checks: Check spindle load meter on HMI; inspect cutting tool for chip welding or edge wear; manually rotate spindle shaft (power OFF) to feel for mechanical drag.")
    pdf.add_bullet("Recommended Corrective Actions: 1. Press Feed Hold and inspect cutting tool. 2. Replace worn inserts or tool assembly. 3. Reduce axial depth of cut by 25%. 4. Increase spindle speed by 15% or reduce feed rate.")
    pdf.add_warning_box("SAFETY: Ensure spindle has come to a COMPLETE STOP before opening enclosure door. Do not touch hot cutting tools with bare hands.")

    # Error E315
    pdf.add_h2("Error Code E315 - Temperature Sensor Fault")
    pdf.add_paragraph("Description: Thermal compensation sensor RTD-1 (Spindle Housing) or RTD-2 (Z-Axis Nut) signal out of valid range (-20°C to +120°C).")
    pdf.add_bullet("Symptoms: Incorrect temperature readout on screen, thermal compensation disabled, E315 alarm active.")
    pdf.add_bullet("Possible Causes: Loose wiring connector at CN7 board, severed thermistor wire, defective PT100 sensor probe, or strong electromagnetic interference.")
    pdf.add_bullet("Diagnostic Checks: Inspect terminal block CN7 on I/O board; measure resistance of PT100 probe (nominal 108.4 Ohms at 21°C); check cable shield ground continuity.")
    pdf.add_bullet("Recommended Corrective Actions: 1. Re-seat connector CN7 securely. 2. Replace defective temperature sensor probe assembly (Part # X100-SEN-315). 3. Repair loose ground shield wire.")
    pdf.add_warning_box("SAFETY: Disconnect main power breaker prior to probing electrical terminal blocks or measuring wiring resistance.")

    # Error E420
    pdf.add_h2("Error Code E420 - Lubrication System Pressure Warning")
    pdf.add_paragraph("Description: Lubrication pressure switch PS-2 fails to detect 15 bar pressure within 30 seconds of automatic lube pump cycle start.")
    pdf.add_bullet("Symptoms: Dry linear guide ways, lube pump runs continuously, E420 alarm active.")
    pdf.add_bullet("Possible Causes: Empty slide-way oil tank, air trapped in lube supply lines, damaged distributor metering valve, clogged 10-micron oil filter, or faulty pressure switch PS-2.")
    pdf.add_bullet("Diagnostic Checks: Check ISO VG 68 oil reservoir level; press manual lube prime button and observe pressure gauge; check linear guide ways for oil film.")
    pdf.add_bullet("Recommended Corrective Actions: 1. Fill lube reservoir with clean ISO VG 68 slide-way oil. 2. Loosen air bleed screw on pump manifold until bubble-free oil flows. 3. Replace clogged oil filter element (Part # X100-LUB-010).")
    pdf.add_warning_box("SAFETY: Immediately clean up any spilled slide-way oil on floor around machine to prevent slipping hazards.")

    pdf.add_h1("3. Additional Machine Symptom Diagnostics")
    pdf.add_bullet("Pneumatic Pressure Low (<6.0 bar): Verify shop supply air pressure; inspect pneumatic FRL moisture drain; adjust regulator knob to 6.5 bar.")
    pdf.add_bullet("Spindle Vibration / Overheating: Inspect spindle oil chiller unit; clean cooling fins; check BT40 tool holder pull stud torque (45 Nm).")
    pdf.add_bullet("Safety Door Interlock Lockout: Inspect door proximity switch alignment; clear chips from door track; verify 24V DC signal at door switch.")
    pdf.add_bullet("Emergency Stop Recovery: Twist red mushroom button clockwise to reset; press Power On button on HMI; home all 3 axes.")

    pdf.save(os.path.join(CNC_DIR, "troubleshooting-guide.pdf"))


def build_cnc_maintenance_manual():
    pdf = SimplePDFWriter("Maintenance Manual", doc_type="MAINTENANCE_MANUAL", product="CNC Machine", model="CNC-X100")
    pdf.add_title("CNC-X100 Vertical Machining Center Maintenance Manual")

    pdf.add_h1("1. Preventive Maintenance Philosophy & Schedule")
    pdf.add_paragraph("Adhering to routine maintenance schedules prevents costly machine downtime, preserves positioning accuracy (±0.005 mm), and extends spindle lifespan.")

    pdf.add_h1("2. Daily Inspection Tasks (Operator Duty)")
    pdf.add_bullet("Coolant Tank: Inspect fluid level sight glass (maintain 80% fill level) and check concentration using optical refractometer (5% to 8%).")
    pdf.add_bullet("Pneumatic FRL Unit: Check main regulator gauge reads 6.0 bar to 8.0 bar (nominal 6.5 bar). Drain condensate bowl.")
    pdf.add_bullet("Automatic Lubrication Tank: Verify ISO VG 68 oil level above 50% capacity.")
    pdf.add_bullet("Enclosure & Way Covers: Clean metal chips off X, Y, Z way covers and door glass using brass scraper and shop vacuum.")
    pdf.add_bullet("Safety Systems: Test Emergency Stop button and safety door interlock operation.")

    pdf.add_h1("3. Weekly Inspection Checklist (Maintenance Technician)")
    pdf.add_bullet("Coolant Intake Filter: Remove screen basket from coolant tank and clean accumulated sludge with compressed air.")
    pdf.add_bullet("Spindle Taper Inspection: Clean BT40 spindle internal taper using felt wiper tool. Check for fretting or galling.")
    pdf.add_bullet("Tool Holder Inspection: Check retention knobs (pull studs) for cracking or wear (torque specification 45 Nm).")
    pdf.add_bullet("Way Cover Wipers: Inspect rubber wipers on linear guide way covers for wear, tears, or chip embedding.")

    pdf.add_h1("4. Monthly Maintenance Tasks")
    pdf.add_bullet("Air Filter Replacement: Clean electrical cabinet intake filter mats; replace if clogged (Part # X100-FLT-002).")
    pdf.add_bullet("Axis Drive Belts: Check tension of X and Y axis timing belts using acoustic meter (nominal 115 Hz).")
    pdf.add_bullet("Automatic Tool Changer (ATC): Grease tool gripper arm pivot pins and cam box using NLGI Grade 2 lithium grease.")
    pdf.add_bullet("Pneumatic Line Dryer: Replace 5-micron coalescing air filter element.")

    pdf.add_h1("5. Cabinet Air Filter Replacement Procedure")
    pdf.add_paragraph("Step-by-step instructions for electrical cabinet air filter maintenance:")
    pdf.add_paragraph("1. Turn OFF main electrical disconnect breaker and open louver door covers on rear cabinet.")
    pdf.add_paragraph("2. Remove filter retainer clips and pull out dusty filter mat.")
    pdf.add_paragraph("3. Wash mat in mild detergent water, dry completely with compressed air hose, or insert new filter mat (Part # X100-FLT-002).")

    pdf.add_h1("6. Coolant Inspection & Complete Flush Procedure")
    pdf.add_paragraph("Every 6 months or 1,500 operating hours, perform complete coolant flush:")
    pdf.add_paragraph("1. Pump out old coolant fluid into disposal tank.")
    pdf.add_paragraph("2. Scrape metal chips and bio-sludge from 200L tank floor.")
    pdf.add_paragraph("3. Flush lines with 2% system cleaner solution for 1 hour, drain completely, and refill with fresh 6% synthetic coolant emulsion to 80% fill mark.")

    pdf.add_h1("7. Maintenance Interval Summary Matrix")
    pdf.add_table_row("Task Description", "Frequency", "Consumable / Part #", is_header=True)
    pdf.add_table_row("Check Lube & Coolant Levels", "Daily", "ISO VG 68 / Coolant")
    pdf.add_table_row("Clean Spindle Taper & Pull Studs", "Weekly", "Felt Wiper Tool")
    pdf.add_table_row("Cabinet Air Filter Mat Swap", "Monthly", "Part # X100-FLT-002")
    pdf.add_table_row("ATC Cam Box Greasing", "Every 3 Months", "NLGI Grade 2 Lithium")
    pdf.add_table_row("Coolant Tank Complete Flush", "Every 6 Months", "System Flush Cleaner")
    pdf.add_table_row("Laser Interferometer Calibration", "Annual", "Service Technician")

    pdf.save(os.path.join(CNC_DIR, "maintenance-manual.pdf"))


def build_cnc_safety_guide():
    pdf = SimplePDFWriter("Safety Guide", doc_type="SAFETY", product="CNC Machine", model="CNC-X100")
    pdf.add_title("CNC-X100 Safety Guidelines & Operator Standards")

    pdf.add_h1("1. General Operational Safety Rules")
    pdf.add_paragraph("Only trained and certified personnel are authorized to operate or service the CNC-X100 machining center.")
    pdf.add_bullet("Always read and understand all safety placards posted on the machine before operation.")
    pdf.add_bullet("Maintain a clean, non-cluttered workspace around the machine perimeter (minimum 1.0-meter clearance).")
    pdf.add_bullet("Never operate machine under influence of medication, drugs, or alcohol.")

    pdf.add_h1("2. Personal Protective Equipment (PPE) Requirements")
    pdf.add_paragraph("All operators and maintenance technicians within the machining bay must wear mandatory PPE:")
    pdf.add_bullet("Eye Protection: ANSI Z87.1 approved impact-resistant safety glasses with side shields.")
    pdf.add_bullet("Footwear: Steel-toe safety shoes with slip-resistant soles.")
    pdf.add_bullet("Hearing Protection: Noise-reduction earplugs or earmuffs when operating near cutting cycles (>85 dBA).")
    pdf.add_warning_box("PROHIBITED NEAR MACHINE: Loose clothing, ties, neck chains, rings, bracelets, and long un-tied hair are strictly prohibited near rotating spindle or chip conveyor.")

    pdf.add_h1("3. Electrical Safety & High-Voltage Standards")
    pdf.add_paragraph("The CNC-X100 operates on high-voltage 400V 3-phase electrical power.")
    pdf.add_bullet("Electrical cabinet doors must remain closed and key-locked during normal operation.")
    pdf.add_bullet("Only qualified industrial electricians may open electrical panels or perform electrical troubleshooting.")
    pdf.add_bullet("Always test electrical terminals for Zero Energy State using calibrated multimeter prior to touching wiring.")

    pdf.add_h1("4. Moving-Part Hazards & Enclosure Door Interlocks")
    pdf.add_paragraph("The machine enclosure features dual interlocked safety doors certified to ISO 13849-1 Category 4 / PL e:")
    pdf.add_bullet("Door Interlock: Automatically locks enclosure doors while spindle is rotating or axes are moving in AUTO mode.")
    pdf.add_bullet("Never bypass, defeat, or short-circuit safety door limit switches under any circumstances.")
    pdf.add_bullet("Beware of pinch points around automatic tool changer arm and chip conveyor bucket.")

    pdf.add_h1("5. Emergency Stop (E-Stop) & Lockout / Tagout (LOTO)")
    pdf.add_paragraph("Emergency Stop Procedure:")
    pdf.add_paragraph("Press red mushroom E-Stop button immediately upon collision, abnormal noise, or fire. Axis drive power is killed instantly and spindle mechanical brake engages within 0.5 seconds.")
    pdf.add_paragraph("Lockout / Tagout (LOTO) Procedure:")
    pdf.add_paragraph("Prior to entering enclosure for cleaning or maintenance, turn main electrical disconnect to OFF, attach personal padlock and warning tag, and lock pneumatic shutoff valve.")

    pdf.save(os.path.join(CNC_DIR, "safety-guide.pdf"))


def build_cnc_technical_specifications():
    pdf = SimplePDFWriter("Technical Specifications", doc_type="TECHNICAL_SPECIFICATION", product="CNC Machine", model="CNC-X100")
    pdf.add_title("CNC-X100 Technical Specifications & Engineering Data")

    pdf.add_h1("1. Machine Dimensions & Physical Parameters")
    pdf.add_bullet("Machine Category: 3-Axis Vertical Machining Center.")
    pdf.add_bullet("Machine Footprint: 2,800 mm Width x 2,250 mm Depth x 2,650 mm Height.")
    pdf.add_bullet("Total Machine Weight: 4,200 kg (9,260 lbs).")
    pdf.add_bullet("Table Dimensions: 900 mm x 450 mm.")
    pdf.add_bullet("Maximum Workpiece / Table Load Capacity: 600 kg (1,320 lbs).")
    pdf.add_bullet("T-Slot Configuration: 5 slots, 18 mm width, 100 mm pitch.")

    pdf.add_h1("2. Electrical & Power Requirements")
    pdf.add_bullet("Input Voltage: 3-Phase AC 400V ±10%, 50/60 Hz.")
    pdf.add_bullet("Total Connected Load: 35 kVA.")
    pdf.add_bullet("Full Load Current: 48 Amps.")
    pdf.add_bullet("Recommended Circuit Breaker: 63 Amp 3-pole breaker with RCCB.")
    pdf.add_bullet("Control Voltage: 24V DC regulated power supply.")
    pdf.add_bullet("Grounding Requirement: Dedicated earth ground rod with ground resistance <5 Ohms.")

    pdf.add_h1("3. Operating Temperature & Environmental Limits")
    pdf.add_bullet("Operating Temperature Range: +15°C to +35°C (+59°F to +95°F).")
    pdf.add_bullet("Storage Temperature Range: -10°C to +50°C.")
    pdf.add_bullet("Relative Humidity: 30% to 80% non-condensing.")
    pdf.add_bullet("Maximum Altitude: 1,000 meters above sea level without power derating.")

    pdf.add_h1("4. Spindle Unit & Tooling Specifications")
    pdf.add_bullet("Spindle Taper: BT40 (ISO 7388-1).")
    pdf.add_bullet("Spindle Speed Range: 100 RPM to 12,000 RPM (Direct Drive).")
    pdf.add_bullet("Spindle Motor Power: 11 kW continuous / 15 kW 30-min peak duty.")
    pdf.add_bullet("Maximum Spindle Torque: 95 Nm @ 1,500 RPM.")
    pdf.add_bullet("Automatic Tool Changer (ATC): 24-tool carousel magazine.")
    pdf.add_bullet("Tool-to-Tool Change Time: 1.8 seconds.")
    pdf.add_bullet("Tool Retention Stud Torque: 45 Nm.")

    pdf.add_h1("5. Motion & Axis Parameters")
    pdf.add_bullet("X-Axis Travel: 800 mm  |  Y-Axis Travel: 450 mm  |  Z-Axis Travel: 500 mm")
    pdf.add_bullet("Rapid Traverse Rates: X: 30 m/min, Y: 30 m/min, Z: 24 m/min.")
    pdf.add_bullet("Maximum Cutting Feed Rate: 10,000 mm/min.")
    pdf.add_bullet("Positioning Accuracy (ISO 230-2): ±0.005 mm.")
    pdf.add_bullet("Repeatability (ISO 230-2): ±0.003 mm.")

    pdf.add_h1("6. Pneumatic, Coolant & Lubrication Specifications")
    pdf.add_bullet("Pneumatic Pressure Range: 6.0 bar to 8.0 bar (nominal 6.5 bar). Air flow: 250 L/min.")
    pdf.add_bullet("Coolant Tank Capacity: 200 Liters.")
    pdf.add_bullet("Recommended Coolant: 6% water-soluble synthetic coolant emulsion.")
    pdf.add_bullet("Normal Coolant Fill Level: 80% fill mark (Minimum acceptable level: 50%).")
    pdf.add_bullet("Coolant Pump Pressure & Flow: 3.5 bar @ 35 L/min.")
    pdf.add_bullet("E105 Alarm Threshold: Flow rate sensor FM-1 detects below 8.0 L/min or thermal relay Q4 trips.")
    pdf.add_bullet("Central Lubrication Oil: ISO VG 68 slide-way oil (2.0-Liter tank).")

    pdf.add_h1("7. Communication & Telemetry Protocols")
    pdf.add_bullet("Ethernet Configuration: Dual RJ45 1000BASE-T ports. Static IP: 192.168.1.150")
    pdf.add_bullet("Supported Protocols: Modbus TCP/IP (Port 502), OPC UA Server (Port 4840), MTConnect Agent (Port 5000).")

    pdf.save(os.path.join(CNC_DIR, "technical-specifications.pdf"))


def build_cnc_service_manual():
    pdf = SimplePDFWriter("Service Manual", doc_type="SERVICE_MANUAL", product="CNC Machine", model="CNC-X100")
    pdf.add_title("CNC-X100 Field Service & Overhaul Manual")

    pdf.add_h1("1. Service Overview & Certified Technician Qualification")
    pdf.add_paragraph("This Service Manual provides authorized field service procedure standards for ProductAssist technicians servicing the CNC-X100 vertical machining center.")
    pdf.add_bullet("Service Clearance: Maintain 1.0-meter open clearance around rear electrical cabinet and side pump enclosures during field servicing.")
    pdf.add_bullet("Zero Energy State: Always execute Lockout/Tagout (LOTO) and verify 400V 3-phase bus voltage reads zero with calibrated meter prior to touching internal wiring.")

    pdf.add_h1("2. Component Access & Service Inspection Points")
    pdf.add_bullet("Coolant Tank & Intake Screen: Accessible at lower rear cabinet. Screen basket mesh size 0.5 mm requires flushing when flow drops below 8.0 L/min.")
    pdf.add_bullet("Spindle Drive Motor & Bearing Chiller: Located at top headstock enclosure. Chiller unit requires annual refrigerant pressure check.")
    pdf.add_bullet("Z-Axis Ball Screw & Linear Guides: Remove upper accordion way cover. Lubricate with ISO VG 68 way oil every 500 hours.")
    pdf.add_bullet("Electrical Cabinet Breakers & Relays: Located on rear door panel. Check thermal overload relay Q4 (coolant pump) setting: 8.5 Amps.")

    pdf.add_h1("3. Major Service Procedures & Field Overhauls")
    pdf.add_bullet("Coolant Pump Replacement: Disconnect 400V 3-phase pump leads, unbolt flange bolts, replace pump assembly (Part # X100-PMP-001).")
    pdf.add_bullet("Spindle BT40 Drawbar Retention Spring Replacement: Use hydraulic spring compressor tool to replace Belleville washer stack (retention force 9.5 kN).")
    pdf.add_bullet("Axis Ball Screw Backlash Adjustment: Adjust pre-load double nut until backlash reads <0.003 mm on dial indicator.")

    pdf.add_h1("4. Field Service Escalation Conditions")
    pdf.add_paragraph("Escalate to Senior Systems Engineer immediately if:")
    pdf.add_bullet("Spindle bearing thermal runout exceeds 0.015 mm or vibration exceeds 4.5 mm/s.")
    pdf.add_bullet("Main casting structure exhibits cracking or foundation anchor bolt displacement.")
    pdf.add_bullet("Short circuit faults damage internal 24V DC I/O bus controller cards.")

    pdf.save(os.path.join(CNC_DIR, "service-manual.pdf"))


# ----------------------------------------------------------------------
# PRINTER-A200 DOCS
# ----------------------------------------------------------------------
PRINTER_DIR = os.path.join(BASE_KB_DIR, "Printer-A200")

def build_printer_docs():
    os.makedirs(PRINTER_DIR, exist_ok=True)
    
    # Operation Manual
    pdf1 = SimplePDFWriter("Operation Manual", doc_type="OPERATION_MANUAL", product="Industrial Printer", model="Printer-A200")
    pdf1.add_title("Printer-A200 Industrial 3D Printer Operation Guide")
    pdf1.add_h1("1. Printer Overview & Touch Screen")
    pdf1.add_paragraph("The Printer-A200 is an industrial additive manufacturing system designed for high-resolution thermoplastic prototype and end-use part production.")
    pdf1.add_bullet("Build Volume: 300 x 300 x 400 mm.")
    pdf1.add_bullet("Extruder Temperature: Up to 300°C. Heated Bed Temperature: Up to 120°C.")
    pdf1.add_bullet("Filament Diameter: 1.75 mm high-precision spool feed.")
    pdf1.add_h1("2. Paper / Filament Feed & Printing Setup")
    pdf1.add_bullet("Loading Filament: Heat nozzle to 215°C, feed filament through optical runout sensor into drive gear.")
    pdf1.add_bullet("Bed Leveling: Automatic 25-point capacitive matrix mesh leveling before every print cycle.")
    pdf1.add_bullet("Clearing Paper/Filament Feed Errors: If feed error occurs, press PAUSE on touchscreen, unload filament lever, and pull out clogged strand.")
    pdf1.save(os.path.join(PRINTER_DIR, "operation-manual.pdf"))

    # Troubleshooting Guide
    pdf2 = SimplePDFWriter("Troubleshooting Guide", doc_type="TROUBLESHOOTING", product="Industrial Printer", model="Printer-A200")
    pdf2.add_title("Printer-A200 Diagnostic & Troubleshooting Guide")
    pdf2.add_h1("1. Error Code P101 - Filament Jam / Feed Error")
    pdf2.add_paragraph("Description: Extruder stepper motor detects high backpressure or filament runout sensor triggers.")
    pdf2.add_bullet("Corrective Action: 1. Pause print job. 2. Heat nozzle to 230°C. 3. Use 0.4 mm acupuncture needle to clear nozzle tip orifice. 4. Reload filament.")
    pdf2.add_h1("2. Error Code P205 - Bed Thermal Runaway")
    pdf2.add_paragraph("Description: Heated bed thermistor signal drops unexpectedly during heating cycle.")
    pdf2.add_bullet("Corrective Action: Inspect bed heater thermistor wiring harness connector under heated bed plate.")
    pdf2.save(os.path.join(PRINTER_DIR, "troubleshooting-guide.pdf"))

    # Maintenance Manual
    pdf3 = SimplePDFWriter("Maintenance Manual", doc_type="MAINTENANCE_MANUAL", product="Industrial Printer", model="Printer-A200")
    pdf3.add_title("Printer-A200 Maintenance Manual")
    pdf3.add_h1("1. Routine Maintenance Schedule")
    pdf3.add_bullet("Daily: Clean PEI print surface with 99% Isopropyl Alcohol (IPA).")
    pdf3.add_bullet("Weekly: Lubricate dual Z-axis lead screws with PTFE grease.")
    pdf3.add_bullet("Monthly: Inspect X/Y timing belt tension (nominal 90 Hz). Replace HEPA air filter mat.")
    pdf3.save(os.path.join(PRINTER_DIR, "maintenance-manual.pdf"))


# ----------------------------------------------------------------------
# HVAC-C500 DOCS
# ----------------------------------------------------------------------
HVAC_DIR = os.path.join(BASE_KB_DIR, "HVAC-C500")

def build_hvac_docs():
    os.makedirs(HVAC_DIR, exist_ok=True)
    
    # Operation Manual
    pdf1 = SimplePDFWriter("Operation Manual", doc_type="OPERATION_MANUAL", product="Commercial HVAC System", model="HVAC-C500")
    pdf1.add_title("HVAC-C500 Commercial Air Handling Unit Operation Guide")
    pdf1.add_h1("1. System Specifications & Controls")
    pdf1.add_paragraph("The HVAC-C500 is a commercial 50-ton rooftop air handling unit designed for industrial workshop climate control.")
    pdf1.add_bullet("Air Flow Capacity: 15,000 CFM.")
    pdf1.add_bullet("Refrigerant: R-410A dual circuit compressor system.")
    pdf1.add_h1("2. Thermostat & Airflow Settings")
    pdf1.add_bullet("Temperature Setpoint Range: +18°C to +26°C.")
    pdf1.add_bullet("Blower Speed: Variable Frequency Drive (VFD) controlled 0 to 100%.")
    pdf1.save(os.path.join(HVAC_DIR, "operation-manual.pdf"))

    # Troubleshooting Guide
    pdf2 = SimplePDFWriter("Troubleshooting Guide", doc_type="TROUBLESHOOTING", product="Commercial HVAC System", model="HVAC-C500")
    pdf2.add_title("HVAC-C500 Diagnostic & Troubleshooting Guide")
    pdf2.add_h1("1. Error Code H102 - High Refrigerant Pressure Alarm")
    pdf2.add_paragraph("Description: Compressor circuit 1 pressure switch trips above 425 psi.")
    pdf2.add_bullet("Corrective Action: Clean outdoor condenser coils with coil cleaner hose; verify condenser fan motor rotation.")
    pdf2.add_h1("2. Error Code H304 - Low Airflow / Filter Clogged Warning")
    pdf2.add_paragraph("Description: Differential pressure switch across filter bank exceeds 250 Pa.")
    pdf2.add_bullet("Corrective Action: Inspect and replace MERV 13 intake air filter elements immediately.")
    pdf2.save(os.path.join(HVAC_DIR, "troubleshooting-guide.pdf"))

    # Maintenance Manual
    pdf3 = SimplePDFWriter("Maintenance Manual", doc_type="MAINTENANCE_MANUAL", product="Commercial HVAC System", model="HVAC-C500")
    pdf3.add_title("HVAC-C500 Maintenance Manual")
    pdf3.add_h1("1. Air Filter Replacement Procedure")
    pdf3.add_paragraph("How to replace the HVAC air filter on HVAC-C500:")
    pdf3.add_bullet("1. Turn OFF main electrical disconnect switch on HVAC service panel.")
    pdf3.add_bullet("2. Unlatch side filter access door.")
    pdf3.add_bullet("3. Slide out dirty MERV 13 filter panels (Size 24x24x2 inches).")
    pdf3.add_bullet("4. Insert new MERV 13 filter panels with airflow arrows pointing toward blower fan.")
    pdf3.add_bullet("5. Latch access door and restore power.")
    pdf3.save(os.path.join(HVAC_DIR, "maintenance-manual.pdf"))


if __name__ == "__main__":
    print(f"Building synthetic knowledge base in: {BASE_KB_DIR}")
    
    # CNC-X100
    os.makedirs(CNC_DIR, exist_ok=True)
    build_cnc_operation_manual()
    build_cnc_installation_guide()
    build_cnc_troubleshooting_guide()
    build_cnc_maintenance_manual()
    build_cnc_safety_guide()
    build_cnc_technical_specifications()
    build_cnc_service_manual()
    
    # Printer-A200
    build_printer_docs()
    
    # HVAC-C500
    build_hvac_docs()
    
    print("All multi-product synthetic PDFs (CNC-X100, Printer-A200, HVAC-C500) generated successfully!")
