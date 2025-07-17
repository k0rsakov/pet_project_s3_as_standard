from utils.s3_utils import S3_CONFIGS, boto3_upload_csv, minio_upload_csv

minio_upload_csv(
    conn_params=S3_CONFIGS["minio"],
    bucket_name=S3_CONFIGS["minio"]["bucket"],
    object_name="titanic_minio_client.csv",
    file_path="../titanic.csv",
)
boto3_upload_csv(
    conn_params=S3_CONFIGS["minio"],
    bucket_name=S3_CONFIGS["minio"]["bucket"],
    object_name="titanic_boto3_client.csv",
    file_path="../titanic.csv",
)

minio_upload_csv(
    conn_params=S3_CONFIGS["selectel"],
    bucket_name=S3_CONFIGS["selectel"]["bucket"],
    object_name="titanic_minio_client.csv",
    file_path="../titanic.csv",
)
boto3_upload_csv(
    conn_params=S3_CONFIGS["selectel"],
    bucket_name=S3_CONFIGS["selectel"]["bucket"],
    object_name="titanic_boto3_client.csv",
    file_path="../titanic.csv",
)

minio_upload_csv(
    conn_params=S3_CONFIGS["vk"],
    bucket_name=S3_CONFIGS["vk"]["bucket"],
    object_name="titanic_minio_client.csv",
    file_path="../titanic.csv",
)
boto3_upload_csv(
    conn_params=S3_CONFIGS["vk"],
    bucket_name=S3_CONFIGS["vk"]["bucket"],
    object_name="titanic_boto3_client.csv",
    file_path="../titanic.csv",
)

minio_upload_csv(
    conn_params=S3_CONFIGS["aws"],
    bucket_name=S3_CONFIGS["aws"]["bucket"],
    object_name="titanic_minio_client.csv",
    file_path="../titanic.csv",
)
boto3_upload_csv(
    conn_params=S3_CONFIGS["aws"],
    bucket_name=S3_CONFIGS["aws"]["bucket"],
    object_name="titanic_boto3_client.csv",
    file_path="../titanic.csv",
)
