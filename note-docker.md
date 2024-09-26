<!-- Run command -->
<!-- Tạo thư mục -->
mkdir <ten_folder>

<!-- Tạo tệp docker-compose.yml -->

echo > docker-compose.yml

<!-- Setting for docker-compose.yml -->
version: '3.8'
services:
    mysql:
        image: mysql:latest
        <!-- Tên container -->
        container_name: mysql-container
        <!-- Tự động khởi động lại nếu container ngừng -->
        restart: always
        <!-- Môi trường -->
        environment:
            MYSQL_ROOT_PASSWORD: my_secret_pw
            MYSQL_DATABASE: mydb
            MYSQL_USER: myuser
            MYSQL_PASSWORD: mypassword
        ports:
            - '3306:3306'
        <!-- Lưu trữ dữ liệu -->
        volumes:
            - mysql_data:/var/lib/mysql

<!-- Run Docker compose (C1)-->
docker-compose up -d

<!-- C2:
// build container
docker build -t my-mysql .

// run container
docker run --name mysql-container -d -p 3306:3306 my-mysql
-->



