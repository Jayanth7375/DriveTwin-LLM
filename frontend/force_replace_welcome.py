import os
import re

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\InteractiveChat.jsx"

with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# We will use regex to replace the entire useState block for messages
pattern = re.compile(r'const \[messages, setMessages\] = useState\(\[.*?\]\);', re.DOTALL)

clean_state = """const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: `### Welcome to the Inline-6 RAG AI Diagnostic Assistant!\\n\\nI am your domain-trained automotive AI diagnostic expert. Ask me anything about:\\n- **Fastener & Bolt Torque Specs** (Spark plugs, cylinder head, manifold, fuel rail, clamps)\\n- **SAE OBD-II Fault Codes** (P0300-P0306 misfires, P0299 boost leak, P0101 MAF drift, P0401 EGR, P0087 HPFP, P0217 head gasket)\\n- **Diagnostic Procedures** (Compression tests, electrical pinout resistance, component swap tests, smoke leak testing)\\n- **I6 Kinematic Physics & Equations** (120-degree firing order balance, CPI index, ideal gas volume airflow, stoichiometry)\\n- **AI Hardware & Execution Stack** (PyTorch CUDA GPU acceleration, Hugging Face LLM, XGBoost ensemble)`
    }
  ]);"""

if pattern.search(text):
    text = pattern.sub(clean_state, text)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced successfully.")
else:
    print("Could not find the pattern.")

