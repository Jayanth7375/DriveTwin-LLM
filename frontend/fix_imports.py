import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\EngineSchematicI6.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

bad_imports = """import { 
  Activity, Flame, ShieldAlert, CheckCircle2, Wind, Droplets,
  Settings, Gauge, ActivitySquare, Zap, Cpu, AlertTriangle
  Activity, Wind, Droplets, Zap, ShieldAlert, CheckCircle2, AlertTriangle, 
  Settings, Gauge, Box, ArrowRight, PlayCircle, FileText, ChevronRight
} from 'lucide-react';"""

good_imports = """import { 
  Activity, Wind, Droplets, Zap, ShieldAlert, CheckCircle2, AlertTriangle, 
  Settings, Gauge, Box, ArrowRight, PlayCircle, FileText, ChevronRight, ActivitySquare, BarChart3
} from 'lucide-react';"""

text = text.replace(bad_imports, good_imports)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

