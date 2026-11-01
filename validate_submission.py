from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
required = [
    'README.md', 'server/frontend/static/About.html', 'server/frontend/static/Contact.html',
    'server/frontend/static/style.css', 'server/frontend/static/bootstrap.min.css',
    'server/frontend/static/cars.jpeg', 'server/frontend/static/contactus.png',
    'server/frontend/src/components/Register/Register.jsx', '.github/workflows/cicd.yml'
]
for name in required:
    assert (ROOT/name).is_file(), f'Missing required project file: {name}'
about = (ROOT/'server/frontend/static/About.html').read_text()
contact = (ROOT/'server/frontend/static/Contact.html').read_text()
register=(ROOT/'server/frontend/src/components/Register/Register.jsx').read_text()
assert 'Welcome to Best Cars dealership, home to the best cars in North America. We deal in sale of domestic and imported cars at reasonable prices.' in about
for content in (about,contact):
    for stylesheet in ('/static/style.css','/static/bootstrap.min.css'):
        assert stylesheet in content
for field in ('Username','First Name','Last Name','Email','Password'):
    assert f"label: '{field}'" in register
assert 'placeholder={label}' in register
assert 'Register</button>' in register
print('Static files, form placeholders, paths and required description: PASSED')
print('NOTE: Real Django backend, React build, images of actual team, API responses and deployed browser screenshots are not verified by this check.')
