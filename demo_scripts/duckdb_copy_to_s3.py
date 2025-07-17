from utils.duckdb_utils import duckdb_create_csv_to_s3
from utils.s3_utils import S3_CONFIGS

duckdb_create_csv_to_s3(conn_params=S3_CONFIGS["minio"], bucket_name=S3_CONFIGS["minio"]["bucket"])

duckdb_create_csv_to_s3(conn_params=S3_CONFIGS["selectel"], bucket_name=S3_CONFIGS["selectel"]["bucket"])

duckdb_create_csv_to_s3(conn_params=S3_CONFIGS["vk"], bucket_name=S3_CONFIGS["vk"]["bucket"])

duckdb_create_csv_to_s3(conn_params=S3_CONFIGS["aws"], bucket_name=S3_CONFIGS["aws"]["bucket"])
