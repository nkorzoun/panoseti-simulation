#!/bin/bash

# ./run.sh [directory name]
# options: -p [primary particle] -e [energy range] -m [spectral slope] -z [zenith range] -a [azimuth range] -s [scattering range]
# e.g.
# ./run.sh test -p gamma -e '1E4 1E4' -m -2.5 -z '0. 0.' -s '400.E2 400.E2'
# ./run.sh test2 -p proton -e '1E4 1E4' -m -2.5 -z '0. 5.' -s '400.E2 400.E2'

./run.sh -p gamma -e '1E4 1E6' -m -2.7 -z '20. 20.' -a '180. 180.' -s '600.E2 600.E2' MRK421-sim-gamma
./run.sh -p proton -e '1E4 1E6' -m -2.7 -z '10. 30.' -a '170. 190.' -s '600.E2 600.E2' MRK421-sim-proton
./run.sh -p iron -e '1E4 1E6' -m -2.8 -z '10. 30.' -a '170. 190.' -s '600.E2 600.E2' iron
