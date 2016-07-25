#!/usr/bin/python

import re

subject = "#saya lagi makan @jalanmagelang & &gt;"
result = re.sub(r"(#\S+)|(@\S+)|(&\S+)", "", subject)
print result