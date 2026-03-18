python3 src/main.py "/static-site-generator/"
cd docs && touch .nojekyll && python3 -m http.server 8888
