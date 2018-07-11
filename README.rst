From the Firefox release notes, retrieve the list of bugs fixed in a dot releases
and generate a csv file with the list of revisions

.. code-block::

  virtualenv --no-site-packages venv
  source venv/bin/activate
  pip install -r requirements.txt
  python analysis.py > export.csv


To set up a check in the cron:

.. code-block::

  20 20 * * * cd ~/dev/mozilla/dot-release-analysis && . venv/bin/activate && python missing-bug.py &> /tmp/foo.log; if test $? -ne 0; then cat /tmp/foo.log|mail -s "Missing bug in the release notes" s@mozilla.com; fi

