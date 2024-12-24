CREATE TABLE IF NOT EXISTS `user` (
    user_id VARCHAR(20) PRIMARY KEY,
    username VARCHAR(256) NOT NULL,
    email VARCHAR(256) NOT NULL,
    password VARCHAR(256) NOT NULL,
    fullname VARCHAR(256) NOT NULL,
    token VARCHAR(1000),
    role INTEGER DEFAULT 0,
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO nike.`user`
(user_id, username, email, fullname, password, token, `role`, flg_del, created_user, updated_user, created_date, updated_date)
VALUES('GryfqpgyoJEM7JEs42QN', 'admin', 'admin@gmail.com', 'admin', '$2b$12$BWex6PXXyVItz17nWaDh8u0pvM/EYZRAq5wAz6cvaSLRKHRw2isue', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZW1haWwiOiJhZG1pbkBnbWFpbC5jb20iLCJleHAiOjE3MzU2MjA5MjQuNjg3MjI1fQ.eY4RVWx3amDw4HoaPS3heQHLMECAiZnDpWmEEXyvTJE', 1, 0, NULL, NULL, '2024-12-23 15:20:31.000', '2024-12-23 15:20:31.000');
INSERT INTO nike.`user`
(user_id, username, email, fullname, password, token, `role`, flg_del, created_user, updated_user, created_date, updated_date)
VALUES('gWu8bXF7VMfAoBgLcIdj', 'demo', 'demo@gmail.com', 'demo', '$2b$12$nNCuavy2VNitM4H5LhTYRe7xYClvN9ormTR0gglG86WxNQiSy19qO', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRlbW8iLCJlbWFpbCI6ImRlbW9AZ21haWwuY29tIiwiZXhwIjoxNzM1NjIwODgyLjAwODU5Nn0.i0jk84tONI--n61Wqq8Z8ckNkcg94oEyWfbbrgDOdJE', 0, 0, NULL, NULL, '2024-12-23 15:22:51.000', '2024-12-23 15:22:51.000');

CREATE TABLE IF NOT EXISTS `cart` (
    cart_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(256),
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0,
    fk_user_id VARCHAR(20),
    CONSTRAINT fk_user FOREIGN KEY (fk_user_id) REFERENCES user(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `product` (
    product_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    weight VARCHAR(256),
    height VARCHAR(256),
    qr_code VARCHAR(256) NOT NULL,
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0,
    fk_cart_id VARCHAR(20),
    CONSTRAINT fk_cart FOREIGN KEY (fk_cart_id) REFERENCES cart(cart_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `post` (
    id SERIAL PRIMARY KEY,
    image_url VARCHAR(256),
    image_url_type VARCHAR(256),
    caption VARCHAR(1000),
    timestamp TIMESTAMP,
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `comment` (
    id SERIAL PRIMARY KEY,
    text VARCHAR(1000),
    username VARCHAR(256),
    timestamp TIMESTAMP,
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
