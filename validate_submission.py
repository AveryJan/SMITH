from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
required = ['README.md','server/manage.py','server/djangoapp/views.py','server/djangoproj/settings.py',
            'server/database/app.js','server/microservices/app.py','server/frontend/package.json',
            'server/frontend/src/App.jsx','server/frontend/static/About.html','server/frontend/static/Contact.html',
            'server/frontend/static/style.css','server/frontend/static/bootstrap.min.css',
            'server/frontend/static/cars.jpeg','server/frontend/static/contactus.png',
            'server/frontend/src/components/Register/Register.jsx','.github/workflows/cicd.yml']
for name in required:
    assert (ROOT/name).is_file(), f'Missing required project file: {name}'
about=(ROOT/'server/frontend/static/About.html').read_text()
contact=(ROOT/'server/frontend/static/Contact.html').read_text()
register=(ROOT/'server/frontend/src/components/Register/Register.jsx').read_text()
assert 'Welcome to Best Cars dealership, home to the best cars in North America. We deal in sale of domestic and imported cars at reasonable prices.' in about
for content in (about,contact):
    for href in ('/static/style.css','/static/bootstrap.min.css'):
        assert href in content
for field in ('Username','First Name','Last Name','Email','Password'):
    assert f"label: '{field}'" in register
assert 'placeholder={label}' in register
assert 'Register</button>' in register
assert 'path(' in (ROOT/'server/djangoapp/urls.py').read_text()
print('PASS: capstone structure, pages, CSS links, React form, backend source and workflow')
