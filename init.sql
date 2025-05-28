-- 建立資料庫使用者（如果不存在）
DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'user') THEN
      CREATE USER "user" WITH PASSWORD 'pass';
   END IF;
END
$do$;

-- 確保 public schema 的權限
GRANT ALL PRIVILEGES ON SCHEMA public TO "user";

-- 設置默認權限
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
GRANT ALL PRIVILEGES ON TABLES TO "user";

-- 確保已存在表的權限
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "user";

-- 確保使用者可以建立表
GRANT CREATE ON SCHEMA public TO "user";

-- 確保使用者是資料庫擁有者
ALTER DATABASE mydb OWNER TO "user";
