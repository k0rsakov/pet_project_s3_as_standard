from utils.duckdb_utils import duckdb_read_csv_from_s3
from utils.s3_utils import S3_CONFIGS

duckdb_read_csv_from_s3(conn_params=S3_CONFIGS["minio"], bucket_name=S3_CONFIGS["minio"]["bucket"])

duckdb_read_csv_from_s3(conn_params=S3_CONFIGS["selectel"], bucket_name=S3_CONFIGS["selectel"]["bucket"])

duckdb_read_csv_from_s3(conn_params=S3_CONFIGS["vk"], bucket_name=S3_CONFIGS["vk"]["bucket"])

duckdb_read_csv_from_s3(conn_params=S3_CONFIGS["aws"], bucket_name=S3_CONFIGS["aws"]["bucket"])

