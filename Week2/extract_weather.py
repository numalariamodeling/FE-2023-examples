import tempfile
from pathlib import Path

from emodpy_malaria.weather import generate_weather

# ---| Request weather files |---

# Request weather time series, for nodes listed in a .csv file
wr = generate_weather(platform="Calculon",
                      site_file="../inputs/example_site.csv",
                      start_date=2019001,
                      end_date=2019365,
                      node_column="nodes",
                      local_dir="../inputs/example_weather/",
                      id_reference="Gridded world grump2.5arcmin",
                      force=True)

print("\n".join(wr.files))