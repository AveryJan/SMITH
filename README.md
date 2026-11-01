# fullstack_developer_capstone — Best Cars Dealership Review Application

This project implements the **Best Cars** full-stack dealership review capstone using Django, an independently runnable Node.js dealer service, a sentiment endpoint, and a React/Vite frontend. It includes dealer browsing and filtering, registration, login, Django admin, car makes/models, dealer reviews, and posting reviews. The Django site also renders functional pages without requiring the React build.

**Rubric repository name:** `xrwvm-fullstack_developer_capstone`. Your existing repository `AveryJan/SMITH` must be renamed in GitHub Settings → General → Repository name, or this project must be uploaded to an appropriately named repository, to meet the specific rubric. Renaming is an account-level action, not a code change.

## What is included

- `server/manage.py`, `server/djangoproj/`, `server/djangoapp/`: Django project, authentication endpoints, admin, car models, reviews and templates
- `server/database/app.js`: dependency-free Node dealership API on port 3030 (dealers, dealer details, reviews, posting a review)
- `server/microservices/app.py`: lightweight standalone sentiment API on port 5050 with `/analyze/Fantastic%20services`
- `server/frontend/src`: React UI and five-field registration component
- `server/frontend/templates`: browser-rendered Django pages, including dealer listing, filtering, details, and review form
- `server/frontend/static`: corrected About and Contact pages, CSS and visual assets
- `.github/workflows/cicd.yml`: structure/API tests, Django tests and React build
- `tests/test_services.py`: local HTTP integration tests for the Node and sentiment services
- `scripts/import_ibm_data.py`: downloads the **real dataset** from the public IBM starter (internet required)
- `scripts/collect_api_evidence.sh`: captures actual cURL output after services are started

## Important: real IBM data versus included demo fixtures

The ZIP includes synthetic fixture records in `server/database/data/` **only to support offline development**. They are not the IBM course dataset and are **not appropriate to submit as authentic course evidence**. Before your capstone demonstration, run the IBM data import below. It downloads original `dealerships.json`, `reviews.json` and `car_records.json` from [IBM's public capstone starter](https://github.com/ibm-developer-skills-network/xrwvm-fullstack_developer_capstone). Check that the returned dealer/model count matches your lab assignment. The sentiment endpoint included here uses a simple rule-based demo classifier; replace it with the IBM VADER implementation if the grading requirements evaluate NLP beyond the example phrase.

## Set up (Linux/macOS or Git Bash with Python 3.11+ and Node 20+)

From project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r server/requirements.txt
python scripts/import_ibm_data.py
cd server
python manage.py makemigrations djangoapp
python manage.py migrate
python manage.py shell < ../scripts/seed_car_models.py
python manage.py createsuperuser
cd ..
```

Create the username **root** through `createsuperuser` if the lab specifically requires root login; choose your own secure password. Never commit the credentials or database.

### Start the services (three separate terminals)

1. `node server/database/app.js` — dealership JSON API at http://localhost:3030/fetchDealers
2. `python server/microservices/app.py` — sentiment API at http://localhost:5050/analyze/Fantastic%20services
3. `cd server && python manage.py runserver 0.0.0.0:8000` — website http://localhost:8000, admin http://localhost:8000/admin/

You can also run the React implementation (fourth terminal):

```bash
cd server/frontend
npm install
npm run dev
```

React is served by Vite (typically port 5173) and proxies its `/djangoapp` endpoints to the Django server. The React front-end and Django-rendered pages share the Django authentication session when hosted on the same origin. For demonstration, use the Django-rendered site at port 8000 to avoid cross-origin session complications.

## Run tests

```bash
python scripts/validate_submission.py
python -m unittest discover -s tests -v
cd server && python manage.py test djangoapp -v 2
cd frontend && npm install && npm run build
```

Django tests and React build require installing the dependencies. Automated checks are also defined in `.github/workflows/cicd.yml`.

## Assignment endpoint map

| What | Endpoint |
|---|---|
| Home dealer list | `/` |
| Filter by state | `/?state=Kansas` |
| Dealer details and reviews | `/dealers/1/` |
| Post a review | `/postreview/1/` |
| Django administration | `/admin/` |
| User login / logout / registration | `/djangoapp/login`, `/djangoapp/logout`, `/djangoapp/register` |
| Car makes and models | `/djangoapp/get_cars` |
| All dealers | `http://localhost:3030/fetchDealers` |
| Kansas dealers | `http://localhost:3030/fetchDealers/Kansas` |
| One dealer | `http://localhost:3030/fetchDealer/1` |
| Dealer reviews | `http://localhost:3030/fetchReviews/dealer/1` |
| Sentiment | `http://localhost:5050/analyze/Fantastic%20services` |

## Evidence and deployment

1. After importing the original IBM course dataset and starting the three services, run `bash scripts/collect_api_evidence.sh` from the repository root. Copy the actual cURL commands and their outputs for the assessment.
2. Log into `/admin/` as the actual root account and capture a real browser screenshot. Log out and capture the genuine logout screen.
3. Capture actual browser screenshots of dealers, state filter, dealer details, review entry and posted review. Include the browser address bar as the rubric requires.
4. Upload files under their paths **as directories**, including `.github/workflows/cicd.yml`. Check GitHub Actions for an actual successful run and copy the executed job logs rather than the YAML source.
5. Deployment requires a real hosting environment and URL; none is included or claimed in this project package. Configure `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, `DJANGO_ALLOWED_HOSTS`, HTTPS, static files, persistent database and the two services before deploying. A `localhost` URL or placeholder is not a live deployment URL.
6. Replace example team profiles/contact placeholders with accurate authorized details if your assignment expects real team information.

**Verification notice:** Local Node API/sentiment checks can run offline. Django and React checks require dependency installation. This project is not claimed to be cloud deployed or already graded.
