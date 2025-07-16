from s3_utils import S3_CONFIGS, boto3_list_objects, minio_list_objects

minio_list_objects(conn_params=S3_CONFIGS["minio"], bucket_name=S3_CONFIGS["minio"]["bucket"])
boto3_list_objects(conn_params=S3_CONFIGS["minio"], bucket_name=S3_CONFIGS["minio"]["bucket"])

minio_list_objects(conn_params=S3_CONFIGS["selectel"], bucket_name=S3_CONFIGS["selectel"]["bucket"])
boto3_list_objects(conn_params=S3_CONFIGS["selectel"], bucket_name=S3_CONFIGS["selectel"]["bucket"])

minio_list_objects(conn_params=S3_CONFIGS["vk"], bucket_name=S3_CONFIGS["vk"]["bucket"])
boto3_list_objects(conn_params=S3_CONFIGS["vk"], bucket_name=S3_CONFIGS["vk"]["bucket"])

minio_list_objects(conn_params=S3_CONFIGS["aws"], bucket_name=S3_CONFIGS["aws"]["bucket"])
boto3_list_objects(conn_params=S3_CONFIGS["aws"], bucket_name=S3_CONFIGS["aws"]["bucket"])
