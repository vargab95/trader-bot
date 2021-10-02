#!/bin/bash

python3 -m cProfile -o /tmp/tvb.profile $@
pyprof2calltree -i /tmp/tvb.profile -k
