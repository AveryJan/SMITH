#!/usr/bin/env bash
set -euo pipefail
mkdir -p evidence
capture() {
  local name="$1"; shift
  echo "Running: curl -fsS $*" | tee "evidence/$name"
  curl -fsS "$@" | python3 -m json.tool | tee -a "evidence/$name"
}
capture getdealerreviews http://localhost:3030/fetchReviews/dealer/1
capture getalldealers http://localhost:3030/fetchDealers
capture getdealerbyid http://localhost:3030/fetchDealer/1
capture getdealersbyState http://localhost:3030/fetchDealers/Kansas
capture getallcarmakes http://localhost:8000/djangoapp/get_cars
capture analyzereview http://localhost:5050/analyze/Fantastic%20services
