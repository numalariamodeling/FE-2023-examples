import tempfile
from pathlib import Path

from emodpy_malaria.weather import generate_weather

# ---| Request weather files |---

# Request weather time series, for nodes listed in a .csv file
wr = generate_weather(platform="SLURM_LOCAL",
                      site_file="../inputs/Mutasa.csv",
                      start_date=2019001,
                      end_date=2019365,
                      node_column="nodes",
                      local_dir="../inputs/Mutasa/",
                      is_staging=True)

print("\n".join(wr.files))