From the Firefox release notes, retrieve the list of bugs fixed in a dot releases
and generate a csv file with the list of revisions

.. code-block::

  virtualenv --no-site-packages venv
  source venv/bin/activate
  pip install -r requirements.txt
  wget -O notes.json "https://nucleus.mozilla.org/rna/notes/?format=json"
  wget -O releases.json "https://nucleus.mozilla.org/rna/releases/?format=json"
  python analysis.py > export.csv
