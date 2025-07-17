import pandas as pd
from cred import s3_minio_access_key, s3_minio_secret_key, s3_minio_bucket_name, s3_minio_endpoint

def pandas_read_csv_from_s3(
    bucket_name: str, file_name: str, access_key: str, secret_key: str, endpoint: str, secure: bool = False
):
    protocol = "https" if secure else "http"
    df = pd.read_csv(
        filepath_or_buffer=f's3://{bucket_name}/{file_name}',
        storage_options={
            "key": access_key,
            "secret": secret_key,
            "client_kwargs": {"endpoint_url": f"{protocol}://{endpoint}"},
        },
    )
    print(df.head())


# noinspection PyTypeChecker
def pandas_to_s3_csv(
    df: pd.DataFrame,
    conn_params: dict,
    bucket_name: str,
    file_name: str,
    compression: str = "gzip",
) -> None:
    """
    Ручка для записи DataFrame в S3 в формате CSV через pandas.

    :param df: DataFrame pandas.
    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :param file_name: Имя файла в бакете.
    :param compression: Тип сжатия (по умолчанию 'gzip').
    :return: Ничего.
    """
    endpoint_protocol = "https" if conn_params.get("secure", True) else "http"
    endpoint_url = f"{endpoint_protocol}://{conn_params['endpoint']}"

    storage_options = {
        "key": conn_params["access_key"],
        "secret": conn_params["secret_key"],
        "client_kwargs": {"endpoint_url": endpoint_url},
    }
    if conn_params.get("region"):
        storage_options["client_kwargs"]["region_name"] = conn_params["region"]

    s3_path = f"s3://{bucket_name}/{file_name}"

    df.to_csv(
        path_or_buf=s3_path,
        index=False,
        escapechar="\\",
        compression=compression,
        storage_options=storage_options,
    )
    print(f"📝 With pandas; DataFrame saved as CSV to {s3_path} in {conn_params['target']}")
