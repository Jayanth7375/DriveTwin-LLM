content = base64.b64decode(b'aW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JzsKaW1wb3J0IHsgCiAgRmlsZVNwcmVhZHNoZWV0LCAKICBBY3Rpdml0eSwgCiAgQmFyQ2hhcnQzLCAKICBTcGFya2xlcywgCiAgTWVzc2FnZVNxdWFyZSwgCiAgR2F1Z2UsIAogIEJveCwKICBDaGV2cm9uTGVmdCwKICBDaGV2cm9uUmlnaHQsCiAgU3VuLAogIE1vb24KfSBmcm9tICdsdWNpZGUtcmVhY3QnOwoKZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gU2lkZWJhcih7IGFjdGl2ZVRhYiwgc2V0QWN0aXZlVGFiLCBoYXJkd2FyZUluZm8sIGlzQ29sbGFwc2VkLCBzZXRJc0NvbGxhcHNlZCwgaXNEYXJrTW9kZSwgc2V0SXNEYXJrTW9kZSB9KSB7CiAgY29uc3QgbmF2SXRlbXMgPSBbCiAgICB7IGlkOiAnb3ZlcnZpZXcnLCBsYWJlbDogJ0RpYWdub3N0aWNzIE92ZXJ2aWV3JywgaWNvbjogRmlsZVNwcmVhZHNoZWV0LCBiYWRnZTogJ01haW4nIH0sCiAgICB7IGlkOiAnbGxtJywgbGFiZWw6ICdSQUcgTExNIFJlcGFpciBSZXBvcnQnLCBpY29uOiBTcGFya2xlcywgYmFkZ2U6ICdBSSBSZXBvcnQnIH0sCiAgICB7IGlkOiAnZGlnaXRhbHR3aW4nLCBsYWJlbDogJzNEIEVuZ2luZSBEaWdpdGFsIFR3aW4nLCBpY29uOiBCb3gsIGJhZGdlOiAnM0QgV2ViR0wnIH0sCiAgICB7IGlkOiAnc2NoZW1hdGljJywgbGFiZWw6ICdFbmdpbmUgVmlzdWFsIEhVRCcsIGljb246IEFjdGl2aXR5LCBiYWRnZTogJ0ludGVyYWN0aXZlJyB9LAogICAgeyBpZDogJ3BoeXNpY3MnLCBsYWJlbDogJ1BoeXNpY3MgJiBQSU5OIE1ldHJpY3MnLCBpY29uOiBCYXJDaGFydDMsIGJhZGdlOiAnUHlUb3JjaCcgfSwKICAgIHsgaWQ6ICdjaGF0JywgbGFiZWw6ICdNZWNoYW5pYyBBSSBDaGF0JywgaWNvbjogTWVzc2FnZVNxdWFyZSwgYmFkZ2U6ICdRJkEnIH0sCiAgXTsKCiAgcmV0dXJuICgKICAgIDxhc2lkZSBjbGFzc05hbWU9InctNjQgYmctWyMxNjFiMjJdIGJvcmRlci1yIGJvcmRlci1bIzMwMzYzZF0gZmxleCBmbGV4LWNvbCBqdXN0aWZ5LWJldHdlZW4gaC1zY3JlZW4gc3RpY2t5IHRvcC0wIHNocmluay0wIHNlbGVjdC1ub25lIHNoYWRvdy14bCB6LTUwIHJvdW5kZWQtbm9uZSI+CiAgICA8YXNpZGUgY2xhc3NOYW1lPXtgdHJhbnNpdGlvbi1hbGwgZHVyYXRpb24tMzAwIGVhc2UtaW4tb3V0IGJvcmRlci1yIGZsZXggZmxleC1jb2wganVzdGlmeS1iZXR3ZWVuIGgtc2NyZWVuIHN0aWNreSB0b3AtMCBzaHJpbmstMCBzZWxlY3Qtbm9uZSBzaGFkb3cteGwgei01MCAkewogICAgICBpc0NvbGxhcHNlZCA/ICd3LTIwJyA6ICd3LTY0JwogICAgfSAkewogICAgICBpc0RhcmtNb2RlIAogICAgICAgID8gJ2JnLVsjMTYxYjIyXSBib3JkZXItWyMzMDM2M2RdJyAKICAgICAgICA6ICdiZy13aGl0ZSBib3JkZXItZ3JheS0yMDAnCiAgICB9YH0+CiAgICAgIDxkaXY+CiAgICAgICAgey8qIFRvcCBBcHAgQnJhbmRpbmcgKi99CiAgICAgICAgPGRpdiBjbGFzc05hbWU9InAtNCBib3JkZXItYiBib3JkZXItWyMzMDM2M2RdIGZsZXggaXRlbXMtY2VudGVyIGdhcC0zIGJnLVsjMGQxMTE3XS81MCByb3VuZGVkLW5vbmUiPgogICAgICAgICAgPGRpdiBjbGFzc05hbWU9InAtMiBiZy1jeWFuLTUwMC8xMCBib3JkZXIgYm9yZGVyLWN5YW4tNTAwLzMwIHRleHQtY3lhbi00MDAgc2hyaW5rLTAgcm91bmRlZC1ub25lIj4KICAgICAgICA8ZGl2IGNsYXNzTmFtZT17YHAtNCBib3JkZXItYiBmbGV4IGl0ZW1zLWNlbnRlciBnYXAtMyByZWxhdGl2ZSAke2lzRGFya01vZGUgPyAnYm9yZGVyLVsjMzAzNjNkXSBiZy1bIzBkMTExN10vNTAnIDogJ2JvcmRlci1ncmF5LTIwMCBiZy1ncmF5LTUwJ31gfT4KICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPXtgcC0yIHNocmluay0wIHJvdW5kZWQtbGcgJHtpc0RhcmtNb2RlID8gJ2JnLWN5YW4tNTAwLzEwIGJvcmRlci1jeWFuLTUwMC8zMCB0ZXh0LWN5YW4tNDAwJyA6ICdiZy1jeWFuLTEwMCBib3JkZXItY3lhbi0yMDAgdGV4dC1jeWFuLTYwMCd9YH0+CiAgICAgICAgICAgIDxHYXVnZSBjbGFzc05hbWU9InctNiBoLTYgYW5pbWF0ZS1wdWxzZSIgLz4KICAgICAgICAgIDwvZGl2PgogICAgICAgICAgPGRpdj4KICAgICAgICAgICAgPGgxIGNsYXNzTmFtZT0idGV4dC1zbSBmb250LWJvbGQgdHJhY2tpbmctd2lkZSB0ZXh0LXdoaXRlIGxlYWRpbmctdGlnaHQiPgogICAgICAgICAgICAgIERJRVNFTCBJNiBFTkdJTkUKICAgICAgICAgICAgPC9oMT4KICAgICAgICAgICAgPHAgY2xhc3NOYW1lPSJ0ZXh0LVsxMHB4XSB0ZXh0LWN5YW4tNDAwIGZvbnQtbW9ubyBmb250LXNlbWlib2xkIj4KICAgICAgICAgICAgICBMTE0gRGlhZ25vc3RpYyBTdWl0ZQogICAgICAgICAgICA8L3A+CiAgICAgICAgICA8L2Rpdj4KICAgICAgICAgIAogICAgICAgICAgeyFpc0NvbGxhcHNlZCAmJiAoCiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPSJvdmVyZmxvdy1oaWRkZW4gd2hpdGVzcGFjZS1ub3dyYXAiPgogICAgICAgICAgICAgIDxoMSBjbGFzc05hbWU9e2B0ZXh0LXNtIGZvbnQtYm9sZCB0cmFja2luZy13aWRlIGxlYWRpbmctdGlnaHQgJHtpc0RhcmtNb2RlID8gJ3RleHQtd2hpdGUnIDogJ3RleHQtZ3JheS05MDAnfWB9PgogICAgICAgICAgICAgICAgRElFU0VMIEk2IEVOR0lORQogICAgICAgICAgICAgIDwvaDE+CiAgICAgICAgICAgICAgPHAgY2xhc3NOYW1lPXtgdGV4dC1bMTBweF0gZm9udC1tb25vIGZvbnQtc2VtaWJvbGQgJHtpc0RhcmtNb2RlID8gJ3RleHQtY3lhbi00MDAnIDogJ3RleHQtY3lhbi02MDAnfWB9PgogICAgICAgICAgICAgICAgTExNIERpYWdub3N0aWMgU3VpdGUKICAgICAgICAgICAgICA8L3A+CiAgICAgICAgICAgIDwvZGl2PgogICAgICAgICAgKX0KCiAgICAgICAgICB7LyogQ29sbGFwc2UgVG9nZ2xlICovfQogICAgICAgICAgPGJ1dHRvbiAKICAgICAgICAgICAgb25DbGljaz17KCkgPT4gc2V0SXNDb2xsYXBzZWQoIWlzQ29sbGFwc2VkKX0KICAgICAgICAgICAgY2xhc3NOYW1lPXtgYWJzb2x1dGUgLXJpZ2h0LTMgdG9wLTYgcC0xIHJvdW5kZWQtZnVsbCBib3JkZXIgc2hhZG93LXNtICR7CiAgICAgICAgICAgICAgaXNEYXJrTW9kZSAKICAgICAgICAgICAgICAgID8gJ2JnLVsjMGQxMTE3XSBib3JkZXItWyMzMDM2M2RdIHRleHQtZ3JheS00MDAgaG92ZXI6dGV4dC13aGl0ZScgCiAgICAgICAgICAgICAgICA6ICdiZy13aGl0ZSBib3JkZXItZ3JheS0zMDAgdGV4dC1ncmF5LTUwMCBob3Zlcjp0ZXh0LWdyYXktODAwJwogICAgICAgICAgICB9YH0KICAgICAgICAgID4KICAgICAgICAgICAge2lzQ29sbGFwc2VkID8gPENoZXZyb25SaWdodCBjbGFzc05hbWU9InctMyBoLTMiIC8+IDogPENoZXZyb25MZWZ0IGNsYXNzTmFtZT0idy0zIGgtMyIgLz59CiAgICAgICAgICA8L2J1dHRvbj4KICAgICAgICA8L2Rpdj4KCiAgICAgICAgey8qIFZlcnRpY2FsIE5hdmlnYXRpb24gSXRlbXMgKi99CiAgICAgICAgPG5hdiBjbGFzc05hbWU9InAtMyBzcGFjZS15LTEgbXQtMiByb3VuZGVkLW5vbmUiPgogICAgICAgICAgPGRpdiBjbGFzc05hbWU9InRleHQtWzEwcHhdIGZvbnQtYm9sZCB0ZXh0LWdyYXktNTAwIHB4LTMgbWItMSB1cHBlcmNhc2UgdHJhY2tpbmctd2lkZXIiPgogICAgICAgICAgICBEaWFnbm9zdGljIE1vZHVsZXMKICAgICAgICAgIDwvZGl2PgogICAgICAgIDxuYXYgY2xhc3NOYW1lPSJwLTMgc3BhY2UteS0xIG10LTIiPgogICAgICAgICAgeyFpc0NvbGxhcHNlZCAmJiAoCiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPSJ0ZXh0LVsxMHB4XSBmb250LWJvbGQgcHgtMyBtYi0xIHVwcGVyY2FzZSB0cmFja2luZy13aWRlciB0ZXh0LWdyYXktNTAwIj4KICAgICAgICAgICAgICBEaWFnbm9zdGljIE1vZHVsZXMKICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICApfQogICAgICAgICAge25hdkl0ZW1zLm1hcCgoaXRlbSkgPT4gewogICAgICAgICAgICBjb25zdCBJY29uID0gaXRlbS5pY29uOwogICAgICAgICAgICBjb25zdCBpc0FjdGl2ZSA9IGFjdGl2ZVRhYiA9PT0gaXRlbS5pZDsKICAgICAgICAgICAgcmV0dXJuICgKICAgICAgICAgICAgICA8YnV0dG9uCiAgICAgICAgICAgICAgICBrZXk9e2l0ZW0uaWR9CiAgICAgICAgICAgICAgICBvbkNsaWNrPXsoKSA9PiBzZXRBY3RpdmVUYWIoaXRlbS5pZCl9CiAgICAgICAgICAgICAgICBjbGFzc05hbWU9e2B3LWZ1bGwgZmxleCBpdGVtcy1jZW50ZXIganVzdGlmeS1iZXR3ZWVuIHB4LTMgcHktMi41IHRleHQteHMgZm9udC1zZW1pYm9sZCB0cmFuc2l0aW9uLWFsbCByb3VuZGVkLW5vbmUgJHsKICAgICAgICAgICAgICAgIHRpdGxlPXtpc0NvbGxhcHNlZCA/IGl0ZW0ubGFiZWwgOiB1bmRlZmluZWR9CiAgICAgICAgICAgICAgICBjbGFzc05hbWU9e2B3LWZ1bGwgZmxleCBpdGVtcy1jZW50ZXIgdHJhbnNpdGlvbi1hbGwgcm91bmRlZC1sZyBvdmVyZmxvdy1oaWRkZW4gJHsKICAgICAgICAgICAgICAgICAgaXNDb2xsYXBzZWQgPyAnanVzdGlmeS1jZW50ZXIgcC0zJyA6ICdqdXN0aWZ5LWJldHdlZW4gcHgtMyBweS0yLjUnCiAgICAgICAgICAgICAgICB9IHRleHQteHMgZm9udC1zZW1pYm9sZCAkewogICAgICAgICAgICAgICAgICBpc0FjdGl2ZQogICAgICAgICAgICAgICAgICAgID8gJ2JnLWN5YW4tNjAwIHRleHQtd2hpdGUgc2hhZG93LW1kIGJvcmRlciBib3JkZXItY3lhbi00MDAnCiAgICAgICAgICAgICAgICAgICAgOiAndGV4dC1ncmF5LTQwMCBob3Zlcjp0ZXh0LXdoaXRlIGhvdmVyOmJnLVsjMjEyNjJkXScKICAgICAgICAgICAgICAgICAgICA6IGlzRGFya01vZGUgCiAgICAgICAgICAgICAgICAgICAgICA/ICd0ZXh0LWdyYXktNDAwIGhvdmVyOnRleHQtd2hpdGUgaG92ZXI6YmctWyMyMTI2MmRdIGJvcmRlciBib3JkZXItdHJhbnNwYXJlbnQnCiAgICAgICAgICAgICAgICAgICAgICA6ICd0ZXh0LWdyYXktNjAwIGhvdmVyOnRleHQtZ3JheS05MDAgaG92ZXI6YmctZ3JheS0xMDAgYm9yZGVyIGJvcmRlci10cmFuc3BhcmVudCcKICAgICAgICAgICAgICAgIH1gfQogICAgICAgICAgICAgID4KICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPSJmbGV4IGl0ZW1zLWNlbnRlciBnYXAtMi41Ij4KICAgICAgICAgICAgICAgICAgPEljb24gY2xhc3NOYW1lPXtgdy00IGgtNCAke2lzQWN0aXZlID8gJ3RleHQtd2hpdGUnIDogJ3RleHQtY3lhbi00MDAnfWB9IC8+CiAgICAgICAgICAgICAgICAgIDxzcGFuPntpdGVtLmxhYmVsfTwvc3Bhbj4KICAgICAgICAgICAgICAgICAgPEljb24gY2xhc3NOYW1lPXtgdy00IGgtNCAke2lzQWN0aXZlID8gJ3RleHQtd2hpdGUnIDogKGlzRGFya01vZGUgPyAndGV4dC1jeWFuLTQwMCcgOiAndGV4dC1jeWFuLTYwMCcpfWB9IC8+CiAgICAgICAgICAgICAgICAgIHshaXNDb2xsYXBzZWQgJiYgPHNwYW4gY2xhc3NOYW1lPSJ3aGl0ZXNwYWNlLW5vd3JhcCI+e2l0ZW0ubGFiZWx9PC9zcGFuPn0KICAgICAgICAgICAgICAgIDwvZGl2PgogICAgICAgICAgICAgICAge2l0ZW0uYmFkZ2UgJiYgKAogICAgICAgICAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9e2B0ZXh0LVs5cHhdIGZvbnQtbW9ubyBweC0xLjUgcHktMC41IHJvdW5kZWQtbm9uZSAkewogICAgICAgICAgICAgICAgeyFpc0NvbGxhcHNlZCAmJiBpdGVtLmJhZGdlICYmICgKICAgICAgICAgICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPXtgdGV4dC1bOXB4XSBmb250LW1vbm8gcHgtMS41IHB5LTAuNSByb3VuZGVkLW1kICR7CiAgICAgICAgICAgICAgICAgICAgaXNBY3RpdmUKICAgICAgICAgICAgICAgICAgICAgID8gJ2JnLXdoaXRlLzIwIHRleHQtd2hpdGUnCiAgICAgICAgICAgICAgICAgICAgICA6ICdiZy1bIzBkMTExN10gdGV4dC1ncmF5LTQwMCBib3JkZXIgYm9yZGVyLVsjMzAzNjNkXScKICAgICAgICAgICAgICAgICAgICAgIDogaXNEYXJrTW9kZQogICAgICAgICAgICAgICAgICAgICAgICA/ICdiZy1bIzBkMTExN10gdGV4dC1ncmF5LTQwMCBib3JkZXIgYm9yZGVyLVsjMzAzNjNkXScKICAgICAgICAgICAgICAgICAgICAgICAgOiAnYmctZ3JheS0xMDAgdGV4dC1ncmF5LTUwMCBib3JkZXIgYm9yZGVyLWdyYXktMjAwJwogICAgICAgICAgICAgICAgICB9YH0+CiAgICAgICAgICAgICAgICAgICAge2l0ZW0uYmFkZ2V9CiAgICAgICAgICAgICAgICAgIDwvc3Bhbj4KICAgICAgICAgICAgICAgICl9CiAgICAgICAgICAgICAgPC9idXR0b24+CiAgICAgICAgICAgICk7CiAgICAgICAgICB9KX0KICAgICAgICA8L25hdj4KICAgICAgPC9kaXY+CgogICAgICB7LyogRm9vdGVyIEJyYW5kaW5nICovfQogICAgICA8ZGl2IGNsYXNzTmFtZT0icC00IGJvcmRlci10IGJvcmRlci1bIzMwMzYzZF0gYmctWyMwZDExMTddLzUwIHRleHQtY2VudGVyIHRleHQtWzEwcHhdIGZvbnQtbW9ubyB0ZXh0LWdyYXktNTAwIHJvdW5kZWQtbm9uZSI+CiAgICAgICAgRGllc2VsIEk2IERpYWdub3N0aWMgU3VpdGUgdjEuMAogICAgICB7LyogRm9vdGVyIEJyYW5kaW5nICYgVGhlbWUgVG9nZ2xlICovfQogICAgICA8ZGl2PgogICAgICAgIDxkaXYgY2xhc3NOYW1lPSJweC00IHB5LTMgZmxleCBqdXN0aWZ5LWNlbnRlciI+CiAgICAgICAgICA8YnV0dG9uIAogICAgICAgICAgICBvbkNsaWNrPXsoKSA9PiBzZXRJc0RhcmtNb2RlKCFpc0RhcmtNb2RlKX0KICAgICAgICAgICAgY2xhc3NOYW1lPXtgdy1mdWxsIGZsZXggaXRlbXMtY2VudGVyIGp1c3RpZnktY2VudGVyIGdhcC0yIHAtMiByb3VuZGVkLWxnIGJvcmRlciB0cmFuc2l0aW9uLWNvbG9ycyAkewogICAgICAgICAgICAgIGlzRGFya01vZGUgCiAgICAgICAgICAgICAgICA/ICdiZy1bIzBkMTExN10gYm9yZGVyLVsjMzAzNjNkXSB0ZXh0LWdyYXktNDAwIGhvdmVyOnRleHQtd2hpdGUnIAogICAgICAgICAgICAgICAgOiAnYmctZ3JheS0xMDAgYm9yZGVyLWdyYXktMjAwIHRleHQtZ3JheS02MDAgaG92ZXI6dGV4dC1ncmF5LTkwMCcKICAgICAgICAgICAgfWB9CiAgICAgICAgICA+CiAgICAgICAgICAgIHtpc0RhcmtNb2RlID8gPFN1biBjbGFzc05hbWU9InctNCBoLTQiIC8+IDogPE1vb24gY2xhc3NOYW1lPSJ3LTQgaC00IiAvPn0KICAgICAgICAgICAgeyFpc0NvbGxhcHNlZCAmJiA8c3BhbiBjbGFzc05hbWU9InRleHQteHMgZm9udC1zZW1pYm9sZCI+e2lzRGFya01vZGUgPyAnTGlnaHQgTW9kZScgOiAnRGFyayBNb2RlJ308L3NwYW4+fQogICAgICAgICAgPC9idXR0b24+CiAgICAgICAgPC9kaXY+CiAgICAgICAgeyFpc0NvbGxhcHNlZCAmJiAoCiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT17YHAtNCBib3JkZXItdCB0ZXh0LWNlbnRlciB0ZXh0LVsxMHB4XSBmb250LW1vbm8gJHsKICAgICAgICAgICAgaXNEYXJrTW9kZSA/ICdib3JkZXItWyMzMDM2M2RdIGJnLVsjMGQxMTE3XS81MCB0ZXh0LWdyYXktNTAwJyA6ICdib3JkZXItZ3JheS0yMDAgYmctZ3JheS01MCB0ZXh0LWdyYXktNDAwJwogICAgICAgICAgfWB9PgogICAgICAgICAgICBEaWVzZWwgSTYgRGlhZ25vc3RpYyBTdWl0ZSB2MS4wCiAgICAgICAgICA8L2Rpdj4KICAgICAgICApfQogICAgICA8L2Rpdj4KICAgIDwvYXNpZGU+CiAgKTsKfQo='); print(content[:10])
with open('src/components/Sidebar.jsx', 'r', encoding='utf-8') as f:
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

bad_bracket = """           />
              }}
           />"""
good_bracket = """           />"""
text = text.replace(bad_bracket, good_bracket)
text = text.replace('dark:bg-[21262d]', 'dark:bg-[#21262d]')
# Add imports
if 'useSidebar' not in text:
    text = text.replace("import { Sidebar as AceternitySidebar, SidebarBody, SidebarLink } from './ui/sidebar';", "import { Sidebar as AceternitySidebar, SidebarBody, SidebarLink, useSidebar } from './ui/sidebar';\nimport { motion } from 'framer-motion';")
bad_html = """<!doctype html>
<html lang="en" class="dark">
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Diesel I6 Engine LLM Diagnostic Suite</title>
    <!-- Google Fonts: Inter & JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  </head>
  <body class="bg-[#0d1117] text-gray-100 font-sans antialiased min-h-screen">
  <body class="font-sans antialiased min-h-screen">
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>"""

bad_logo = """            {!isCollapsed && (
              <div className="overflow-hidden whitespace-nowrap font-sans">
                <h1 className="text-sm font-bold tracking-wide text-gray-900 dark:text-white leading-tight">DIESEL I6 ENGINE</h1>
                <p className="text-[10px] text-cyan-600 dark:text-cyan-400 font-mono font-semibold">LLM Diagnostic Suite</p>
              </div>
            )}"""
text = text.replace(bad_logo, '')
# Add LogoText component
logo_comp = """
const LogoText = () => {
  const { open, animate } = useSidebar();
  return (
    <motion.div
      animate={{
        display: animate ? (open ? "block" : "none") : "block",
        opacity: animate ? (open ? 1 : 0) : 1,
      }}
      className="overflow-hidden whitespace-nowrap font-sans"
    >
      <h1 className="text-sm font-bold tracking-wide text-gray-900 dark:text-white leading-tight">DIESEL I6 ENGINE</h1>
      <p className="text-[10px] text-cyan-600 dark:text-cyan-400 font-mono font-semibold">LLM Diagnostic Suite</p>
    </motion.div>
  );
};
"""
good_html = """<!doctype html>
<html lang="en" class="dark">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Diesel I6 Engine LLM Diagnostic Suite</title>
    <!-- Google Fonts: Inter & JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  </head>
  <body class="font-sans antialiased min-h-screen">
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>"""

if 'const LogoText' not in text:
    text = text.replace('export default function Sidebar', logo_comp + '\nexport default function Sidebar')
text = text.replace(bad_html, good_html)

# Inject LogoText into JSX
bad_logo = """        <div className="flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
          <div className="flex items-center gap-2">
            <div className="flex items-center justify-center bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 shrink-0 rounded-lg w-7 h-7">
              <Gauge className="w-5 h-5 animate-pulse" />
            </div>
          </div>"""

good_logo = """        <div className="flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
          <div className="flex items-center gap-2 px-2 py-2">
            <div className="flex items-center justify-center bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 shrink-0 rounded-lg w-7 h-7">
              <Gauge className="w-5 h-5 animate-pulse" />
            </div>
            <LogoText />
          </div>"""

text = text.replace(bad_logo, good_logo)

with open('src/components/Sidebar.jsx', 'w', encoding='utf-8') as f:
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)