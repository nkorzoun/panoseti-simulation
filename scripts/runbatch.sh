#!/bin/bash

# ./run.sh [directory name]
# options: -p [primary particle] -e [energy range] -m [spectral slope] -z [zenith range] -s [scattering range]
# e.g.
# ./run.sh test -p gamma -e '1E4 1E4' -m -2.5 -z '0. 0.' -s '400.E2 400.E2'
# ./run.sh test2 -p proton -e '1E4 1E4' -m -2.5 -z '0. 5.' -s '400.E2 400.E2'

./run.sh -p gamma -e '1E5 1E5' -m -2.5 -z '0. 0.' -s '200.E2 200.E2' zenithtest0
wait $!
./run.sh -p gamma -e '1E5 1E5' -m -2.5 -z '30. 30.' -s '200.E2 200.E2' zenithtest30
wait $!
./run.sh -p gamma -e '1E5 1E5' -m -2.5 -z '45. 45.' -s '200.E2 200.E2' zenithtest45
wait $!
./run.sh -p gamma -e '1E5 1E5' -m -2.5 -z '60. 60.' -s '200.E2 200.E2' zenithtest60
wait $!