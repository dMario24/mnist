from typing import Annotated
from fastapi import FastAPI, File, UploadFile
import os
import pymysql.cursors
import json

import jigeum.seoul 
from mnist.db import dml
from mnist.model import predict_digit

app = FastAPI()



@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, label :str, insert_loop: int = 1):
    # 파일 저장
    img = await file.read()
    file_name = file.filename
    file_ext = file.content_type.split('/')[-1]

    # 디렉토리가 없으면 오류, 코드에서 확인 및 만들기 추가
    upload_dir = os.getenv('UPLOAD_DIR','/home/diginori/code/mnist/img/n77')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    import uuid
    file_full_path = os.path.join(upload_dir, 
            f'{uuid.uuid4()}.{file_ext}')

    with open(file_full_path, "wb") as f:
        f.write(img)

    sql = "INSERT INTO image_processing(file_name, label, file_path, request_time, request_user) VALUES(%s, %s, %s, %s, %s)"
   

    insert_row = 0
    for _ in range(insert_loop):
        insert_row = dml(sql, file_name, label, file_full_path, jigeum.seoul.now(), 'n77')
    
    return {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_full_path": file_full_path,
            "insert_row_cont": insert_row
           }


@app.post("/uploadfile2/")
async def create_upload_file(file: UploadFile, label :str):
    # 파일 저장
    img = await file.read()
    file_name = file.filename
    file_ext = file.content_type.split('/')[-1]

    # 디렉토리가 없으면 오류, 코드에서 확인 및 만들기 추가
    upload_dir = os.getenv('UPLOAD_DIR','/home/diginori/code/mnist/img/n77')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    import uuid
    file_full_path = os.path.join(upload_dir, 
            f'{uuid.uuid4()}.{file_ext}')

    with open(file_full_path, "wb") as f:
        f.write(img)

    sql = "INSERT INTO image_processing(file_name, label, file_path, request_time, request_user) VALUES(%s, %s, %s, %s, %s)"
    import jigeum.seoul 
    from mnist.db import dml

    insert_row = dml(sql, file_name, label, file_full_path, jigeum.seoul.now(), 'n77')

    p = "?"
    p = predict_digit('/home/diginori/code/mnist/img/n77/475d95c1-ecfd-42ea-a085-19f050bae74d.png')
    
    return {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_full_path": file_full_path,
            "insert_row_cont": insert_row,
            "predict": p,
            "label": label
           }

@app.get("/all")
def all():
    from mnist.db import select
    sql = "SELECT * FROM image_processing"
    result = select(query=sql, size=-1)
    return result

@app.get("/one")
def one():
    from mnist.db import select
    sql = """SELECT * FROM image_processing 
    WHERE prediction_time IS NULL ORDER BY num LIMIT 1"""
    result = select(query=sql, size=1)
    return result[0]

@app.get("/many/")
def many(size: int = -1):
    from mnist.db import get_conn
    sql = "SELECT * FROM image_processing WHERE prediction_time IS NULL ORDER BY num"
    conn = get_conn()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchmany(size)

    return result

