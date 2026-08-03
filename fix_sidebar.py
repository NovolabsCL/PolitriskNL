content = open('dashboard/app.py').read()
content = 
content.replace('[data-testid="collapsedControl"]{background:var(--gold)!important;border-radius:0 
4px 4px 0!important;}', '')
content = content.replace('[data-testid="collapsedControl"] 
svg{fill:var(--navy)!important;}', '')
open('dashboard/app.py', 'w').write(content)
print('Listo')

