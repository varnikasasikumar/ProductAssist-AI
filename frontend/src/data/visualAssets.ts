export interface ComponentLocation {
  componentId: string;
  name: string;
  location: string;
  accessDoor?: string;
  diagramUrl: string;
  description: string;
  troubleshootingKeywords: string[];
}

export interface VisualDiagram {
  id: string;
  title: string;
  model: string;
  type: 'FLOWCHART' | 'SCHEMATIC' | 'LAYOUT' | 'HMI';
  svgPath: string;
  description: string;
}

export const VISUAL_DIAGRAMS: Record<string, VisualDiagram> = {
  coolant_system: {
    id: 'coolant_system',
    title: 'CNC-X100 Coolant Subsystem & Intake Screen Diagram',
    model: 'CNC-X100',
    type: 'SCHEMATIC',
    svgPath: '/assets/coolant-system-diagram.svg',
    description: 'Schematic illustrating the 50L coolant reservoir tank, mesh filter intake screen, P-101 pump, and FM-1 flow sensor.',
  },
  e105_flowchart: {
    id: 'e105_flowchart',
    title: 'Alarm E105 Agentic Troubleshooting Flowchart',
    model: 'CNC-X100',
    type: 'FLOWCHART',
    svgPath: '/assets/e105-troubleshooting-flowchart.svg',
    description: '4-step agentic diagnostic flowchart for clearing Alarm E105 Coolant Flow Low.',
  },
  hmi_panel: {
    id: 'hmi_panel',
    title: 'CNC-X100 Front Swing Arm HMI Control Panel',
    model: 'CNC-X100',
    type: 'HMI',
    svgPath: '/assets/hmi-control-panel.svg',
    description: 'Touchscreen HMI layout showing Alarm E105 indicator, RESET FAULT button, E-STOP, and Mode Selector.',
  },
};

export const COMPONENT_LOCATIONS: ComponentLocation[] = [
  {
    componentId: 'COMP-INTAKE-MESH',
    name: 'Coolant Intake Screen (Mesh Filter)',
    location: 'Inside coolant reservoir tank at lower suction line',
    accessDoor: 'Rear Service Enclosure Access Panel B',
    diagramUrl: '/assets/coolant-system-diagram.svg',
    description: 'Fine stainless steel mesh screen preventing metal chips from entering coolant pump P-101.',
    troubleshootingKeywords: ['e105', 'coolant flow', 'mesh', 'intake screen', 'clog', 'pump intake'],
  },
  {
    componentId: 'COMP-FLOW-SENSOR-FM1',
    name: 'Flow Meter Sensor FM-1',
    location: 'Inline with main coolant return line before manifold',
    accessDoor: 'Rear Service Enclosure Access Panel B',
    diagramUrl: '/assets/coolant-system-diagram.svg',
    description: 'Digital inline flow rate sensor emitting 4-20mA pulse signal to CNC PLC.',
    troubleshootingKeywords: ['e105', 'fm-1', 'flow sensor', 'signal', 'cn7 connector'],
  },
  {
    componentId: 'COMP-HMI-PANEL',
    name: 'Main Touchscreen HMI Panel',
    location: 'Front Right Swing Arm Enclosure',
    accessDoor: 'Operator Station',
    diagramUrl: '/assets/hmi-control-panel.svg',
    description: '15-inch touch HMI for running programs, reviewing active alarms, and clearing faults.',
    troubleshootingKeywords: ['hmi', 'reset', 'alarm', 'display', 'screen', 'alarm e105'],
  },
  {
    componentId: 'COMP-AIR-FILTER',
    name: 'Cabinet Ventilation Air Filter',
    location: 'Right door panel of main electrical cabinet',
    accessDoor: 'Side Cabinet Door A',
    diagramUrl: '/assets/hmi-control-panel.svg',
    description: 'Washable dual-density foam filter protecting internal drive electronics from dust.',
    troubleshootingKeywords: ['e315', 'air filter', 'cabinet temp', 'overheat', 'ventilation'],
  },
  {
    componentId: 'COMP-ESTOP',
    name: 'Emergency Stop Mushroom Switch (E-Stop)',
    location: 'HMI Console Front Right & Machine Front Left',
    accessDoor: 'Exterior Operator Access',
    diagramUrl: '/assets/hmi-control-panel.svg',
    description: 'Twist-to-release safety kill switch cutting 24V emergency control loop power.',
    troubleshootingKeywords: ['e-stop', 'emergency stop', 'red button', 'safety shutoff'],
  },
];

export function getVisualAssetForQuery(query: string): VisualDiagram | null {
  const q = query.toLowerCase();
  if (q.includes('e105') || q.includes('coolant') || q.includes('flow')) {
    return VISUAL_DIAGRAMS.coolant_system;
  }
  if (q.includes('hmi') || q.includes('screen') || q.includes('display') || q.includes('panel')) {
    return VISUAL_DIAGRAMS.hmi_panel;
  }
  return null;
}

export function getComponentLocationForQuery(query: string): ComponentLocation | null {
  const q = query.toLowerCase();
  for (const comp of COMPONENT_LOCATIONS) {
    if (comp.troubleshootingKeywords.some(kw => q.includes(kw))) {
      return comp;
    }
  }
  return null;
}
