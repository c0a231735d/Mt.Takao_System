import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import mysql.connector
from pydantic import BaseModel


app = FastAPI()
db_config = { # MySQL 接続設定
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "password",
    "database": "main_db"
}
login_user = {"id": None, "name": "", "email": ""} # ログインユーザー識別用


class Account(BaseModel):
    username: str
    email: str
    password: str


class QRCode(BaseModel):
    qr_code: str


@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        # ファイルパスを取得(ファイルパス変わるので、今後変更が必要)
        file_path = os.path.join(os.path.dirname(__file__), "../app_html/test.html")
        with open(file_path, "r", encoding="utf-8") as file:
            return HTMLResponse(content=file.read(), status_code=200)
    except Exception as e:
        return HTMLResponse(content=f"Error: {e}", status_code=500)


#アカウントの作成
@app.post("/accounts/")
def create_account(account: Account):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO accounts (username, email, password) VALUES (%s, %s, %s)", \
                    (account.username, account.email, account.password))
        connection.commit() # DBに反映
        cursor.execute("SELECT LAST_INSERT_ID()") # 登録したユーザーのIDを取得
        login_user["id"] = cursor.fetchone()[0] # ログインユーザーID更新
        cursor.close()
        connection.close()
        login_user["name"] = account.username # ログインユーザー名更新
        login_user["email"] = account.email # ログインユーザーemail更新
        return {"message": "Account created", "account": account}
    except mysql.connector.Error as err: # 接続に失敗した場合
        print(f"Error: {err}")
        return {"message": "Account creation failed"}


#QRコードの検証
@app.post("/verify_qr/")
def verify_qr(qr_code: QRCode):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT route_name, is_peak FROM stamps WHERE qr_code = %s", (qr_code.qr_code,))
    result = cursor.fetchone()
    
    if result:
        route_name, is_peak = result
        if is_peak:
            # 盗聴スタンプを読み込んだら待機状態へ
            cursor.execute("SELECT * FROM accounts WHERE id = %s", (login_user['id'],))
            cursor.execute("UPDATE accounts SET state = %s WHERE id = %s", ("wait", login_user['id']))
        else:
            # スタンプを読み込んだらアクティブ状態へ
            cursor.execute("UPDATE accounts SET state = %s WHERE id = %s", ("active", login_user['id']))
        connection.commit() # DBに反映
        cursor.close()
        connection.close()
        return {"message": "QRコードは正常です", "route_name": route_name, "is_peak": bool(is_peak)}
    else:
        cursor.close()
        connection.close()
        return {"message": "QRコードが無効です"}


# 特典の取得
# @app.post("/get_gift/")
# def get_gift(account: Account):
#     connection = mysql.connector.connect(**db_config)
#     cursor = connection.cursor()
#     # cursor.execute("SELECT COUNT(*) FROM accounts WHERE username = %s AND is_peak = True", (account.username,))
#     peak_count = cursor.fetchone()[0]
#     cursor.close()
#     connection.close()
#     print(peak_count)

    # if peak_count >= 10:
    #     return {"message": "特典を獲得しました", "gift": "Special Gift"}
    # else:
    #     return {"message": "特典を獲得するには、10個のピークスタンプが必要です", "current_peak_count": peak_count}
    
    if __name__ == "__main__":
        user_init = Account(username="test", email="test@test.te", password="test")
        qr_init = QRCode(qr_code="QR_CODE_A2")
        print(create_account(user_init))
        print(login_user)
        print(verify_qr(qr_init))