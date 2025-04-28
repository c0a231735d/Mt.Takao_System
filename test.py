import pymysql

# 接続情報を設定
host = 'localhost'       # データベースのホスト名またはIPアドレス
port = 3306              # MySQLのデフォルトポート番号
user = 'root'   # MySQLユーザー名
password = 'password'  # MySQLユーザーパスワード
database = 'main_db'  # 接続先のデータベース名

try:
    # データベースに接続
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        charset='utf8mb4'  # 必要に応じてエンコーディングを指定
    )
    print("データベース接続に成功しました！")

    # 接続確認のための簡単なクエリを実行
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION();")
        result = cursor.fetchone()
        print(f"MySQLのバージョン: {result[0]}")

except pymysql.MySQLError as e:
    print(f"エラーが発生しました: {e}")
finally:
    # 接続を閉じる
    if 'connection' in locals() and connection.open:
        connection.close()
        print("データベース接続を閉じました。")
