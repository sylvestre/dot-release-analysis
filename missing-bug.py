# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
from analysis import analyzeFiles

if __name__ == "__main__":
    bugs, nbUnset, total = analyzeFiles(['Firefox', 'Firefox for Android'])
    if nbUnset > 0:
        sys.exit(43)
