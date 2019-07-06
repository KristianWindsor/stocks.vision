
--
-- User: backend
--

CREATE USER backend IDENTIFIED WITH mysql_native_password BY 'pass';
GRANT ALL PRIVILEGES ON stocksvision.* TO 'backend'@'%' WITH GRANT OPTION;

--
-- User: crawlapi
--

CREATE USER crawlapi IDENTIFIED WITH mysql_native_password BY 'pass';
GRANT ALL PRIVILEGES ON stocksvision.* TO 'crawlapi'@'%' WITH GRANT OPTION;

--
-- User: crawlscheduler
--

CREATE USER crawlscheduler IDENTIFIED WITH mysql_native_password BY 'pass';
GRANT ALL PRIVILEGES ON stocksvision.* TO 'crawlscheduler'@'%' WITH GRANT OPTION;

--
-- User: phpmyadmin
--

CREATE USER phpmyadmin IDENTIFIED WITH mysql_native_password BY 'pass';
GRANT ALL PRIVILEGES ON stocksvision.* TO 'phpmyadmin'@'%' WITH GRANT OPTION;
