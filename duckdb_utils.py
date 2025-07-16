import duckdb


def duckdb_create_csv_to_s3(conn_params: dict, bucket_name: str, object_name: str = "file.csv") -> None:
    """
    Ручка для создания .csv напрямую в S3 через DuckDB.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :param object_name: Название файла в бакете.
    :return: Ничего.
    """
    con = duckdb.connect()
    endpoint = conn_params["endpoint"]
    access_key = conn_params["access_key"]
    secret_key = conn_params["secret_key"]
    secure = conn_params.get("secure", True)
    con.sql(
        f"""
        SET TIMEZONE = 'UTC';
        INSTALL httpfs;
        LOAD httpfs;
        SET s3_url_style = 'path';
        SET s3_endpoint = '{endpoint}';
        SET s3_access_key_id = '{access_key}';
        SET s3_secret_access_key = '{secret_key}';
        SET s3_use_ssl = {secure};
        COPY (SELECT 1 as one) TO 's3://{bucket_name}/{object_name}';
        """,
    )
    con.close()
    print(f"CSV written to s3://{bucket_name}/{object_name}")


def duckdb_read_csv_from_s3(conn_params: dict, bucket_name: str, object_name: str = "file.csv") -> None:
    """
    Ручка для чтения .csv напрямую из S3 через DuckDB.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :param object_name: Название файла в бакете.
    :return: Ничего.
    """
    con = duckdb.connect()
    endpoint = conn_params["endpoint"]
    access_key = conn_params["access_key"]
    secret_key = conn_params["secret_key"]
    secure = conn_params.get("secure", True)
    df = con.sql(
        f"""
        SET TIMEZONE = 'UTC';
        INSTALL httpfs;
        LOAD httpfs;
        SET s3_url_style = 'path';
        SET s3_endpoint = '{endpoint}';
        SET s3_access_key_id = '{access_key}';
        SET s3_secret_access_key = '{secret_key}';
        SET s3_use_ssl = {secure};
        SELECT * FROM read_csv('s3://{bucket_name}/{object_name}');
        """,
    ).df()
    con.close()
    print(df.head())
    print(f"CSV read from s3://{bucket_name}/{object_name}")
