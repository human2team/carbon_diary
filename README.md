# Carbon Diary

탄소 다이어리를 실행하기 위한 설정 및 실행 방법을 안내합니다.

---

## 1. 환경 설정

### (1) .env 파일 생성

프로젝트 루트에 `.env.env` 파일이 있습니다.
이를 `.env`로 이름을 변경한 뒤, 내부 환경 변수를 알맞게 채워주세요.

예시:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=carbon_diary
```

---

## 2. 데이터베이스 생성

프로젝트에 포함된 `carbon_records.sql` 파일을 이용해 데이터베이스와 테이블을 생성합니다.

```bash
mysql -u your_username -p < carbon_records.sql
```

---

## 3. 패키지 설치

`requirements.txt`에 정의된 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

---

## 4. 애플리케이션 실행

설정이 완료되면 `app.py`를 실행합니다.

```bash
python app.py
```

---

## 5. 접속

기본적으로 Flask 애플리케이션은 `http://127.0.0.1:5000` 에서 실행됩니다.
웹 브라우저에서 접속하여 서비스를 확인할 수 있습니다.
