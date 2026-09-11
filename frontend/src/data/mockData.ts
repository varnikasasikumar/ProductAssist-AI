import { Product, KnowledgeDocument, MaintenanceRecord, ChatMessage, TroubleshootingState, SystemStat } from '../types';

export const mockStats: SystemStat[] = [
  { title: 'Monitored Assets', value: 24, change: '+2', isPositive: true, period: 'this month' },
  { title: 'Active Health Score', value: '98.4%', change: '+1.2%', isPositive: true, period: 'vs last week' },
  { title: 'Indexed Documents', value: 142, change: '+18', isPositive: true, period: 'this week' },
  { title: 'Open Maintenance Tasks', value: 3, change: '-2', isPositive: true, period: 'vs yesterday' },
];

export const mockProducts: Product[] = [
  {
    id: 'prod-1',
    name: '3-Axis High-Precision CNC Machining Center',
    model: 'CNC-X100',
    serialNumber: 'SN-2024-X100-8891',
    status: 'warning',
    location: 'Bay A - Assembly Line 1',
    category: 'Milling & Machining',
    lastMaintained: '2026-08-15',
    nextMaintenance: '2026-09-15',
    operatingHours: 3420,
    temperature: '24°C',
    pressure: '6.5 bar',
    vibration: '0.8 mm/s',
    specs: {
      'Spindle Speed': '12,000 RPM',
      'Axis Travel (X/Y/Z)': '800 / 450 / 500 mm',
      'Coolant Reservoir': '200 Liters',
      'Control System': 'ProductAssist HMI (15" Touchscreen)'
    },
    description: 'High-precision 3-axis vertical machining center designed for enterprise production lines.'
  },
  {
    id: 'prod-2',
    name: 'Industrial Hydraulic Stamping Press',
    model: 'HYD-PRESS-500',
    serialNumber: 'SN-2023-HP50-3302',
    status: 'operational',
    location: 'Bay B - Heavy Stamping',
    category: 'Metal Forming',
    lastMaintained: '2026-09-01',
    nextMaintenance: '2026-10-01',
    operatingHours: 6180,
    temperature: '48°C',
    pressure: '210 bar',
    vibration: '0.8 mm/s',
    specs: {
      'Max Force': '500 Tons',
      'Stroke Length': '800 mm',
      'Oil Tank Capacity': '600 Liters',
      'Safety Curtain': 'Category 4 Optical Light Guard'
    },
    description: 'Heavy-duty hydraulic press for precision sheet metal drawing, forming, and blanking operations.'
  },
  {
    id: 'prod-3',
    name: '6-Axis Articulated Industrial Robot',
    model: 'ROBO-ARM-6X',
    serialNumber: 'SN-2025-RA6X-1044',
    status: 'operational',
    location: 'Bay A - Automated Cell 3',
    category: 'Robotics & Automation',
    lastMaintained: '2026-08-28',
    nextMaintenance: '2026-11-28',
    operatingHours: 1890,
    temperature: '39°C',
    pressure: 'N/A',
    vibration: '0.3 mm/s',
    specs: {
      'Payload Capacity': '160 kg',
      'Max Reach': '3100 mm',
      'Repeatability': '±0.05 mm',
      'IP Rating': 'IP67 Enclosure'
    },
    description: 'High-payload articulated robot arm used for automated spot welding and heavy part handling.'
  },
  {
    id: 'prod-4',
    name: 'Heavy Industrial Gas Turbine Generator',
    model: 'TURBO-GEN-2000',
    serialNumber: 'SN-2022-TG2K-0012',
    status: 'maintenance',
    location: 'Power Station - Auxiliary Bay',
    category: 'Power Generation',
    lastMaintained: '2026-09-05',
    nextMaintenance: '2026-09-12',
    operatingHours: 14200,
    temperature: '840°C',
    pressure: '18.5 bar',
    vibration: '3.1 mm/s',
    specs: {
      'Power Output': '2.4 MW',
      'Rotor Speed': '15,000 RPM',
      'Fuel Type': 'Natural Gas / Dual Fuel',
      'Thermal Efficiency': '41.5%'
    },
    description: 'Continuous duty industrial gas turbine power module currently undergoing scheduled combustor inspection.'
  }
];

export const mockDocuments: KnowledgeDocument[] = [
  {
    id: 'doc-101',
    title: 'CNC-X100 Maintenance & Troubleshooting Manual',
    category: 'Service Guide',
    targetModels: ['CNC-X100'],
    pageCount: 148,
    uploadDate: '2026-08-10',
    fileSize: '18.4 MB',
    status: 'indexed',
    chunkCount: 312,
    fileFormat: 'PDF',
    versionTag: 'v2.4'
  },
  {
    id: 'doc-105',
    title: 'CNC-X100 Authorized Technical Specifications',
    category: 'Technical Specs',
    targetModels: ['CNC-X100'],
    pageCount: 1,
    uploadDate: '2026-09-08',
    fileSize: '0.4 MB',
    status: 'indexed',
    chunkCount: 15,
    fileFormat: 'JSON',
    versionTag: 'v3.0-SPEC'
  },
  {
    id: 'doc-106',
    title: 'Printer-A200 Industrial 3D Printer Operation Manual',
    category: 'User Manual',
    targetModels: ['Printer-A200'],
    pageCount: 42,
    uploadDate: '2026-09-08',
    fileSize: '6.2 MB',
    status: 'indexed',
    chunkCount: 88,
    fileFormat: 'PDF',
    versionTag: 'v1.2'
  },
  {
    id: 'doc-107',
    title: 'HVAC-C500 Commercial HVAC Unit Service Guide',
    category: 'Service Guide',
    targetModels: ['HVAC-C500'],
    pageCount: 56,
    uploadDate: '2026-09-08',
    fileSize: '8.1 MB',
    status: 'indexed',
    chunkCount: 104,
    fileFormat: 'PDF',
    versionTag: 'v2.0'
  },
  {
    id: 'doc-102',
    title: 'HYD-PRESS-500 Hydraulic System & Safety Protocol',
    category: 'Safety Protocol',
    targetModels: ['HYD-PRESS-500'],
    pageCount: 84,
    uploadDate: '2026-08-14',
    fileSize: '9.2 MB',
    status: 'indexed',
    chunkCount: 165,
    fileFormat: 'PDF',
    versionTag: 'v1.0'
  },
  {
    id: 'doc-103',
    title: 'ROBO-ARM-6X Kinematics & Control Calibration Guide',
    category: 'User Manual',
    targetModels: ['ROBO-ARM-6X'],
    pageCount: 210,
    uploadDate: '2026-08-20',
    fileSize: '24.1 MB',
    status: 'indexed',
    chunkCount: 440,
    fileFormat: 'PDF',
    versionTag: 'v1.5'
  }
];

export const mockMaintenanceRecords: MaintenanceRecord[] = [
  {
    id: 'maint-301',
    equipmentId: 'prod-1',
    equipmentName: '3-Axis High-Precision CNC Machining Center',
    model: 'CNC-X100',
    type: 'Corrective',
    description: 'Investigate coolant low flow alert (Fault E105) and inspect intake screen filter basket.',
    status: 'Completed',
    priority: 'High',
    scheduledDate: '2026-09-08',
    technician: 'Alex Rivera (Lead Engineer)',
    notes: 'Coolant intake screen cleaned of metal chips. Reservoir topped off with 10:1 emulsion. Flow rate restored to 24.5 L/min; Alarm E105 cleared.'
  },
  {
    id: 'maint-305',
    equipmentId: 'prod-1',
    equipmentName: '3-Axis High-Precision CNC Machining Center',
    model: 'CNC-X100',
    type: 'Preventive',
    description: 'Monthly electrical cabinet air filter mat replacement (Part # X100-FLT-002) and spindle taper inspection.',
    status: 'Completed',
    priority: 'Medium',
    scheduledDate: '2026-08-15',
    technician: 'Alex Rivera (Lead Engineer)',
    notes: 'Air filter mat replaced. Spindle taper cleaned with felt wiper tool; zero fretting observed.'
  },
  {
    id: 'maint-306',
    equipmentId: 'prod-1',
    equipmentName: '3-Axis High-Precision CNC Machining Center',
    model: 'CNC-X100',
    type: 'Preventive',
    description: 'Semi-annual 200-Liter coolant tank complete flush and 2% system cleaner flush.',
    status: 'Completed',
    priority: 'Medium',
    scheduledDate: '2026-07-01',
    technician: 'Marcus Vance (Maintenance Tech)',
    notes: 'Tank flushed and refilled with fresh 6% synthetic coolant emulsion. Flow rate nominal at 35 L/min.'
  },
  {
    id: 'maint-307',
    equipmentId: 'prod-1',
    equipmentName: '3-Axis High-Precision CNC Machining Center',
    model: 'CNC-X100',
    type: 'Corrective',
    description: 'Inspect spindle overload alarm E210 during heavy roughing cut pass.',
    status: 'Completed',
    priority: 'High',
    scheduledDate: '2026-05-20',
    technician: 'Alex Rivera (Lead Engineer)',
    notes: 'Replaced worn carbide cutting inserts on BT40 facemill. Reduced axial depth of cut by 20%.'
  },
  {
    id: 'maint-308',
    equipmentId: 'prod-1',
    equipmentName: '3-Axis High-Precision CNC Machining Center',
    model: 'CNC-X100',
    type: 'Inspection',
    description: 'Annual laser interferometer pitch error compensation and axis accuracy audit.',
    status: 'Completed',
    priority: 'Low',
    scheduledDate: '2026-02-10',
    technician: 'External Precision Calibration Specialist',
    notes: 'Positioning accuracy confirmed within ±0.005 mm spec across X, Y, Z travels.'
  },
  {
    id: 'maint-302',
    equipmentId: 'prod-4',
    equipmentName: 'Heavy Industrial Gas Turbine Generator',
    model: 'TURBO-GEN-2000',
    type: 'Preventive',
    description: 'Scheduled 14,000 hour combustor nozzle inspection and thermal barrier coating audit.',
    status: 'In Progress',
    priority: 'Critical',
    scheduledDate: '2026-09-07',
    technician: 'Sarah Chen (Turbine Specialist)',
    notes: 'Nozzle assembly disassembled. Visual check shows minor soot buildup, cleaning in progress.'
  },
  {
    id: 'maint-303',
    equipmentId: 'prod-2',
    equipmentName: 'Industrial Hydraulic Stamping Press',
    model: 'HYD-PRESS-500',
    type: 'Inspection',
    description: 'Monthly hydraulic oil purity check and filter element replacement.',
    status: 'Scheduled',
    priority: 'Medium',
    scheduledDate: '2026-09-15',
    technician: 'Marcus Vance (Maintenance Tech)',
    notes: 'Filter replacement kit ready in Central Tool Crib B.'
  },
  {
    id: 'maint-304',
    equipmentId: 'prod-3',
    equipmentName: '6-Axis Articulated Industrial Robot',
    model: 'ROBO-ARM-6X',
    type: 'Calibration',
    description: 'Zero-position mastering calibration following end-effector tool head replacement.',
    status: 'Completed',
    priority: 'Low',
    scheduledDate: '2026-08-28',
    technician: 'Alex Rivera (Lead Engineer)',
    notes: 'All 6 axes zeroed with optical calibration kit. Repeatability confirmed at ±0.03mm.'
  }
];

export const mockInitialMessages: ChatMessage[] = [
  {
    id: 'msg-1',
    sender: 'assistant',
    text: 'Hello Engineer. I am ProductAssist AI, your technical operating and troubleshooting intelligence. Select a product model or ask a question directly regarding procedures, fault codes, or maintenance specs.',
    timestamp: '10:00 AM'
  },
  {
    id: 'msg-2',
    sender: 'user',
    text: 'What should I do if the CNC-X100 displays fault code E105 during spindle operation?',
    timestamp: '10:01 AM'
  },
  {
    id: 'msg-3',
    sender: 'assistant',
    text: 'Fault code **E105** on the **CNC-X100** indicates a **Spindle Cooling System Temperature Out-of-Bounds / Flow Rate Fault**.\n\nAccording to section 4.2 of the *CNC-X100 Troubleshooting Manual*:\n\n1. **Check Coolant Level**: Inspect the rear reservoir sight glass. Ensure liquid level is between the MIN and MAX indicators.\n2. **Inspect Coolant Lines**: Look for leaks or kinks in the primary supply and return hoses leading to the spindle housing.\n3. **Verify Circulation Pump Pressure**: Confirm that pump pressure gauge reads above 2.5 bar.\n\nWould you like me to initiate the interactive diagnostic workflow for E105?',
    timestamp: '10:01 AM',
    sources: [
      {
        document: 'CNC-X100 Maintenance & Troubleshooting Manual.pdf',
        page: 42,
        snippet: 'E105 Fault Code: Triggered when spindle thermal sensor detects temperature exceeds 65°C due to inadequate coolant flow or low reservoir fluid level.'
      },
      {
        document: 'Industrial Thermal Management Specification.pdf',
        page: 12,
        snippet: 'Coolant circuit must maintain minimum flow rate of 14 L/min at 3.0 bar to prevent high-speed spindle thermal expansion.'
      }
    ]
  }
];

export const mockTroubleshootingSession: TroubleshootingState = {
  sessionId: 'sess-e105-8912',
  productModel: 'CNC-X100',
  errorCode: 'E105',
  status: 'DIAGNOSING',
  currentStep: 1,
  totalSteps: 3,
  diagnosticFindings: [
    'Fault code E105 confirmed on CNC-X100 spindle controller.',
    'Possible root cause: Low coolant reservoir fluid or airlock in recirculating lines.'
  ],
  suggestedActions: [
    {
      stepNumber: 1,
      action: 'Check coolant level gauge on rear auxiliary tank.',
      expectedOutcome: 'Fluid level should sit between MIN and MAX fill lines.',
      safetyWarning: 'Ensure spindle power is locked out (LOTO) before inspecting lower cabinet rear.'
    },
    {
      stepNumber: 2,
      action: 'If fluid is below MIN line, top up with ISO VG 32 synthetic coolant blend.',
      expectedOutcome: 'Fluid level rises to MAX fill mark.'
    },
    {
      stepNumber: 3,
      action: 'Press RESET on control panel and run 60-second low-speed test cycle.',
      expectedOutcome: 'Fault E105 clears, spindle temperature stabilizes below 45°C.'
    }
  ],
  citations: [
    {
      source_document: 'CNC-X100 Maintenance & Troubleshooting Manual.pdf',
      page: 42,
      section: 'Section 4.2: Thermal Protection & Alarm Codes',
      text_snippet: 'E105: Spindle Overheat Protection. Immediate Action: Verify coolant reservoir volume and circulation pump state.'
    }
  ]
};
