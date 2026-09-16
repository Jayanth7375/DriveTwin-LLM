import os

# 1. Update sidebar.tsx
sidebar_tsx_path = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\ui\sidebar.tsx"
with open(sidebar_tsx_path, 'r', encoding='utf-8') as f:
    tsx_text = f.read()

# Replace the text-neutral-700 with inheriting color or applying the light mode colors if no custom class is passed
# Actually, the simplest is to just let the parent (Sidebar.jsx) pass a class that controls text color.
# Let's see if we can append `className` to the span.
tsx_text = tsx_text.replace(
    'className="text-neutral-700 dark:text-neutral-200 text-sm group-hover/sidebar:translate-x-1 transition duration-150 whitespace-pre inline-block !p-0 !m-0"',
    'className={`dark:text-neutral-200 text-sm group-hover/sidebar:translate-x-1 transition duration-150 whitespace-pre inline-block !p-0 !m-0 ${className?.includes("text-") ? "" : "text-[#3264AD] group-hover/sidebar:text-[#00008b]"}`}'
)
with open(sidebar_tsx_path, 'w', encoding='utf-8') as f:
    f.write(tsx_text)


# 2. Update Sidebar.jsx
sidebar_jsx_path = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\Sidebar.jsx"
with open(sidebar_jsx_path, 'r', encoding='utf-8') as f:
    jsx_text = f.read()

# Update Active Tab icon and text color
# Currently: className={`h-5 w-5 flex-shrink-0 ${activeTab === item.id ? 'text-cyan-600 dark:text-cyan-400' : 'text-gray-500 dark:text-neutral-400'}`}
# We want light mode: active = text-red-600, inactive = text-[#3264AD], hover = group-hover/sidebar:text-[#00008b]
old_icon_class = "className: `h-5 w-5 flex-shrink-0 ${activeTab === item.id ? 'text-cyan-600 dark:text-cyan-400' : 'text-gray-500 dark:text-neutral-400'}`"
new_icon_class = "className: `h-5 w-5 flex-shrink-0 transition-colors ${activeTab === item.id ? 'text-red-600 dark:text-cyan-400' : 'text-[#3264AD] group-hover/sidebar:text-[#00008b] dark:text-neutral-400'}`"
jsx_text = jsx_text.replace(old_icon_class, new_icon_class)

# Update the SidebarLink className to also set the text color for the label
old_link_class = "className={activeTab === item.id ? \"bg-gray-100 dark:bg-[#21262d] rounded-lg\" : \"rounded-lg\"}"
new_link_class = "className={activeTab === item.id ? \"bg-gray-100 dark:bg-[#21262d] rounded-lg text-red-600 dark:text-cyan-400\" : \"rounded-lg text-[#3264AD] hover:text-[#00008b] dark:text-neutral-400\"}"
jsx_text = jsx_text.replace(old_link_class, new_link_class)

# Also update the Logo text to use the gradient or the M colors
old_logo = "<h1 className=\"text-sm font-bold tracking-wide text-gray-900 dark:text-white leading-tight\">DIESEL I6 ENGINE</h1>"
new_logo = "<h1 className=\"text-sm font-bold tracking-wide dark:text-white leading-tight bg-clip-text text-transparent bg-[linear-gradient(to_right,#3264AD,#00008b,red)] dark:bg-none dark:text-white dark:bg-transparent\">DIESEL I6 ENGINE</h1>"
jsx_text = jsx_text.replace(old_logo, new_logo)

with open(sidebar_jsx_path, 'w', encoding='utf-8') as f:
    f.write(jsx_text)

