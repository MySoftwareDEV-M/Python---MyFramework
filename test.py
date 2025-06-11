# import html
import html

s = '<html><head></head><body><h1>This is python</h1></body></html>'
# Using html.escape() method
gfg = html.escape(s)

print(gfg)

ret = html.unescape(gfg)
print(ret)