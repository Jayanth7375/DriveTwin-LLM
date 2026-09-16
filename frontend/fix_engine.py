import os
import re

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\TelemetryUploader.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

bad_image_code = """      {/* CENTER: 3D ENGINE */}
      <div className="flex-1 flex justify-center relative hidden lg:flex pointer-events-none">
        <div className="absolute inset-0 bg-gradient-to-t from-[#090c10] via-transparent to-transparent z-10 rounded-3xl mix-blend-multiply"></div>
        <img 
          src="/engine-render.jpg" 
          alt="3D Engine Render" 
          className="max-w-[120%] lg:max-w-[140%] object-contain scale-110 drop-shadow-[0_0_50px_rgba(34,211,238,0.15)]"
          style={{ mixBlendMode: 'screen' }}
        />
      </div>"""

good_image_code = """      {/* CENTER: 3D ENGINE */}
      <div className="flex-1 flex justify-center relative hidden lg:flex pointer-events-none items-center">
        {/* We use a radial mask to softly fade the edges of the image into the background, and invert + multiply in light mode to make the black background disappear! */}
        <img 
          src="/engine-render.jpg" 
          alt="3D Engine Render" 
          className="max-w-[120%] lg:max-w-[140%] object-contain scale-110 dark:invert-0 invert dark:mix-blend-screen mix-blend-multiply opacity-90 dark:opacity-100"
          style={{
            WebkitMaskImage: 'radial-gradient(circle at center, black 40%, transparent 70%)',
            maskImage: 'radial-gradient(circle at center, black 40%, transparent 70%)'
          }}
        />
      </div>"""

text = text.replace(bad_image_code, good_image_code)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

