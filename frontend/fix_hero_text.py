import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\TelemetryUploader.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

bad_hero = """          <h1 className="text-[4.5rem] lg:text-[5.5rem] font-black text-gray-900 dark:text-white leading-[0.95] tracking-tighter">
            Keep Your<br />
            Engine<br />
            <span className="text-transparent bg-clip-text bg-gradient-to-b from-[#81e6b3] via-[#71d3d6] to-[#60b6e9]">
              One Step<br />
              Ahead
            </span>
          </h1>"""

good_hero = """          <h1 className="text-5xl md:text-6xl lg:text-[4rem] font-black text-gray-900 dark:text-white leading-tight tracking-tight max-w-2xl">
            Keep Your Engine <br className="hidden lg:block" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#81e6b3] via-[#71d3d6] to-[#60b6e9]">
              One Step Ahead
            </span>
          </h1>"""

text = text.replace(bad_hero, good_hero)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

