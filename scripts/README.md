# Usage:
sbatch master.qs <directory_name> -p <primary_particle> -e <energy_range> -m <spectral_slope> -z <zenith_range> -a <azimuth_range> -s <scattering_range>

# Example commands:
sbatch master.qs test -p gamma -e '1E4 1E4' -m -2.5 -z '0. 0.' -s '400.E2 400.E2'
sbatch master.qs -p proton -e '1E4 1E4' -m -2.5 -z '0. 5.' -s '400.E2 400.E2'

sbatch master.qs -p gamma -e '1E4 1E6' -m -2.7 -z '20. 20.' -a '180. 180.' -s '600.E2 600.E2' MRK421-sim-gamma
sbatch master.qs -p proton -e '1E4 1E6' -m -2.7 -z '10. 30.' -a '170. 190.' -s '600.E2 600.E2' MRK421-sim-proton
sbatch master.qs -p iron -e '1E4 1E6' -m -2.8 -z '10. 30.' -a '170. 190.' -s '600.E2 600.E2' iron

sbatch master.qs -p gamma -e '1E4 1E7' -m -2.5 -z '0. 20.' -a '0. 360.' -s '1200.E2 1200.E2' palomar-sim-gamma

