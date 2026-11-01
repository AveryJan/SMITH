# fullstack_developer_capstone — Best Cars Dealership Review Application

**Assignment repository name:** `xrwvm-fullstack_developer_capstone` (rename your GitHub repository or move these files into your course fork to match the grader).

**Project name:** `fullstack_developer_capstone`.

This archive provides corrected static pages, the React registration form, a GitHub Actions workflow and a validator aligned with rubric items Q1, Q3, Q4 and Q7. It is **not a functioning replacement for the IBM course's Django/React/Node application**. Integrate these files into the actual IBM starter and implement or connect the original backend, dealer data, authentication, sentiment service and deployment.

## Verification
Run `python scripts/validate_submission.py` to check the supplied files. Run `.github/workflows/cicd.yml` in GitHub Actions after uploading the archive to the repository. This checks structural requirements only and does not certify full application functionality.

## Required work not solved by static patch
* Implement and run the original Django backend and Node dealership/sentiment services.
* Capture the **actual** outputs of the APIs with `bash scripts/collect_api_evidence.sh`. Verify dealer and model record counts against the course dataset; do not substitute fabricated examples.
* Replace the team demonstration descriptions with authorized names, roles, emails, and actual photos; replace example contact information with verified details, or clearly state no organization contact exists.
* Record Django root admin login and logout screenshots from real browser sessions. Never upload illustrative mockups as operational evidence.
* Capture real logged-out, logged-in, state-filtered, review and deployment screenshots with the browser address bar visible.
* Publish a real deployment URL and copy an actual successful GitHub Actions job log rather than the workflow source.

## Corrected paths
* `server/frontend/static/About.html`
* `server/frontend/static/Contact.html`
* `server/frontend/src/components/Register/Register.jsx`
* `.github/workflows/cicd.yml`

**Caution:** `bootstrap.min.css` in this patch is an offline layout fallback, **not** the official Bootstrap distribution. If the assignment requires Bootstrap, copy the actual Bootstrap CSS from the IBM template into that path.
