#!/bin/bash
set -e;
source env/bin/activate;

echo "[ ] Removing old artefacts...";
rm dist/*;

echo "[ ] Building new artefacts...";
python3 setup.py sdist bdist_wheel;

echo "[ ] Uploading artefacts to PyPI...";
python3 -m twine upload dist/*;

echo "[+] All done!";