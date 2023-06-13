import sys
from utils import *
import warnings
import matplotlib.pyplot as plt


short_name = 'MODIS_T-JPL-L2P-v2019.0'
s3_url = 's3://podaac-ops-cumulus-protected/MODIS_T-JPL-L2P-v2019.0/20210820033500-JPL-L2P_GHRSST-SSTskin-MODIS_T-N-v02.0-fv01.0.nc'

home_dir = os.path.expanduser("~")
plot_file_name = os.path.join(home_dir, "harmony_plot_1.png")

if os.path.isfile(plot_file_name):
  os.remove(plot_file_name)

try:
  harmony_client = Client()
  request = Request(
    collection=Collection(id=short_name),
    spatial=BBox(-97.77667, 21.20806, -83.05197, 30.16605),
    temporal={
      'start': dt.datetime(2021, 8, 20),
      'stop': dt.datetime(2021, 8, 21),
    },
  )
  job_id = harmony_client.submit(request)
  harmony_client.wait_for_processing(job_id, show_progress=False)
  data = harmony_client.result_json(job_id)
  results = harmony_client.result_urls(job_id, link_type=LinkType.s3)
  urls = list(results)
  filename = '20210820033500-JPL-L2P_GHRSST-SSTskin-MODIS_T-N-v02.0-fv01.0_subsetted.nc4'

  url = [url for url in urls if filename in url][0]
  creds = harmony_client.aws_credentials()
  s3_fs = s3fs.S3FileSystem(
    key=creds['aws_access_key_id'],
    secret=creds['aws_secret_access_key'],
    token=creds['aws_session_token'],
    client_kwargs={'region_name': 'us-west-2'},
  )

  f = s3_fs.open(url, mode='rb')
  ds = xr.open_dataset(f)
  ds.sea_surface_temperature.plot()
  plt.savefig(plot_file_name)
except Exception as e:
  print(e)
