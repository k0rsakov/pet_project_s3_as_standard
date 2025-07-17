from utils.pandas_utils import pandas_read_csv_from_s3
from utils.s3_utils import S3_CONFIGS

pandas_read_csv_from_s3(
    conn_params=S3_CONFIGS["minio"],
    bucket_name=S3_CONFIGS["minio"]["bucket"],
)

pandas_read_csv_from_s3(
    conn_params=S3_CONFIGS["selectel"],
    bucket_name=S3_CONFIGS["selectel"]["bucket"],
)

pandas_read_csv_from_s3(
    conn_params=S3_CONFIGS["vk"],
    bucket_name=S3_CONFIGS["vk"]["bucket"],
)

pandas_read_csv_from_s3(
    conn_params=S3_CONFIGS["aws"],
    bucket_name=S3_CONFIGS["aws"]["bucket"],
)
