#!/usr/bin/env bash
# Run only against the actually-running application, with the REAL IBM dataset loaded.
set -euo pipefail
mkdir -p evidence
curl -fsS http://localhost:3030/fetchReviews/dealer/1 | python3 -m json.tool > evidence/getdealerreviews
curl -fsS http://localhost:3030/fetchDealers | python3 -m json.tool > evidence/getalldealers
curl -fsS http://localhost:3030/fetchDealer/1 | python3 -m json.tool > evidence/getdealerbyid
curl -fsS http://localhost:3030/fetchDealers/Kansas | python3 -m json.tool > evidence/getdealersbyState
curl -fsS http://localhost:8000/djangoapp/get_cars | python3 -m json.tool > evidence/getallcarmakes
curl -fsS 'http://localhost:5050/analyze/Fantastic%20services' | python3 -m json.tool > evidence/analyzereview
printf 'Collected real command responses in evidence/. Verify original data is imported before submitting.\n'
