import os
import pytest
import pymysql
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
DATABASE_URL = os.getenv("DATABASE_URL")

@pytest.mark.parametrize("db_config, expected", [
    (DATABASE_URL, True),  # 환경 변수에서 불러온 DB URL
    ("mysql+pymysql://wrong_user:wrong_password@127.0.0.1:3306/testdb", False),
])
def test_database_connection(db_config, expected):
    """
    ✅ MySQL 데이터베이스 연결 테스트
    - 올바른 정보: 정상 연결
    - 잘못된 정보: OperationalError 발생
    """
    if not MYSQL_ROOT_PASSWORD or not MYSQL_DATABASE or not DATABASE_URL:
        pytest.skip("⚠️ 환경 변수(MYSQL_ROOT_PASSWORD, MYSQL_DATABASE, DATABASE_URL)가 설정되지 않음.")

    try:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_ROOT_PASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQL_PORT,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        conn.close()
        assert expected, f"❌ 예상과 다르게 {db_config} 에 연결되었습니다."
    except pymysql.MySQLError:
        assert not expected, f"❌ 예상과 다르게 연결에 실패하였습니다."