import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\App.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

bad_chunk = """          {activeTab === 'llm' && (
            <div className="space-y-6 max-w-5xl mx-auto">
              <LLMReportView diagnosticReport={diagnosticReport} />"""
              
good_chunk = """          {activeTab === 'llm' && (
            <div className="space-y-6 w-full">
              <LLMReportView diagnosticReport={diagnosticReport} />"""

text = text.replace(bad_chunk, good_chunk)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

