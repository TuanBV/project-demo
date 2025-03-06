CREATE TABLE IF NOT EXISTS `user` (
    user_id VARCHAR(20) PRIMARY KEY,
    username VARCHAR(256) NOT NULL,
    email VARCHAR(256) NOT NULL,
    password VARCHAR(256) NOT NULL,
    fullname VARCHAR(256) NOT NULL,
    token VARCHAR(1000),
    birthday DATE,
    area VARCHAR(256),
    city VARCHAR(256),
    state VARCHAR(256),
    postcode VARCHAR(10),
    role INTEGER DEFAULT 0,
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `image` (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(256),
    path VARCHAR(256),
    folder VARCHAR(20),
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `cart` (
    cart_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(256),
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0,
    user_id VARCHAR(20),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES user(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `category` (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `kind` (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `product_kind` (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    category_id BIGINT,
    kind_id BIGINT,
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES category(id),
    CONSTRAINT fk_kind FOREIGN KEY (kind_id) REFERENCES kind(id),
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `sale` (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(256),
    discount INTEGER DEFAULT 0,
    start_date DATE,
    end_date DATE,
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0,
    image_id BIGINT,
    CONSTRAINT fk_sale_image FOREIGN KEY (image_id) REFERENCES `image`(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `product` (
    product_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(256) NOT NULL,
    info VARCHAR(512) NOT NULL,
    quantity INTEGER DEFAULT 0,
    price DOUBLE DEFAULT 0,
    weight DOUBLE DEFAULT 0,
    height DOUBLE DEFAULT 0,
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0,
    sale_id BIGINT,
    product_kind_id BIGINT,
    CONSTRAINT fk_product_kind FOREIGN KEY (product_kind_id) REFERENCES product_kind(id),
    CONSTRAINT fk_sale FOREIGN KEY (sale_id) REFERENCES sale(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `product_image` (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0,
    product_id BIGINT,
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES product(product_id),
    image_id BIGINT,
    CONSTRAINT fk_image FOREIGN KEY (image_id) REFERENCES image(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `cart_product` (
    cart_id VARCHAR(20) NOT NULL,
    product_id BIGINT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (cart_id, product_id),
    CONSTRAINT fk_cart FOREIGN KEY (cart_id) REFERENCES cart(cart_id),
    CONSTRAINT fk_cart_product FOREIGN KEY (product_id) REFERENCES product(product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `post` (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    image_url VARCHAR(256),
    image_url_kind VARCHAR(256),
    caption VARCHAR(1000),
    timestamp TIMESTAMP,
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `comment` (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    text VARCHAR(1000),
    username VARCHAR(256),
    timestamp TIMESTAMP,
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `offer` (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(256) NOT NULL UNIQUE,
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE INDEX ix_offer_email ON offer (email);


CREATE TABLE IF NOT EXISTS `setting` (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255),
    number_phone VARCHAR(255),
    address VARCHAR(255),
    info TEXT,
    fb_link VARCHAR(255),
    ig_link VARCHAR(255),
    tt_link VARCHAR(255),
    tw_link VARCHAR(255),
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

# Insert user
INSERT INTO nike.`user`
(user_id, username, email, fullname, password, token, `role`, flg_del, created_user, updated_user, created_date, updated_date, birthday, area, city, state, postcode)
VALUES('GryfqpgyoJEM7JEs42QN', 'admin', 'admin@gmail.com', 'admin', '$2b$12$BWex6PXXyVItz17nWaDh8u0pvM/EYZRAq5wAz6cvaSLRKHRw2isue', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZW1haWwiOiJhZG1pbkBnbWFpbC5jb20iLCJleHAiOjE3MzU2MjA5MjQuNjg3MjI1fQ.eY4RVWx3amDw4HoaPS3heQHLMECAiZnDpWmEEXyvTJE', 1, 0, NULL, NULL, '2024-12-23 15:20:31.000', '2024-12-23 15:20:31.000', NULL,NULL,NULL,NULL,NULL);
INSERT INTO nike.`user`
(user_id, username, email, fullname, password, token, `role`, flg_del, created_user, updated_user, created_date, updated_date, birthday, area, city, state, postcode)
VALUES('gWu8bXF7VMfAoBgLcIdj', 'demo', 'demo@gmail.com', 'demo', '$2b$12$nNCuavy2VNitM4H5LhTYRe7xYClvN9ormTR0gglG86WxNQiSy19qO', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRlbW8iLCJlbWFpbCI6ImRlbW9AZ21haWwuY29tIiwiZXhwIjoxNzM1NjIwODgyLjAwODU5Nn0.i0jk84tONI--n61Wqq8Z8ckNkcg94oEyWfbbrgDOdJE', 0, 0, NULL, NULL, '2024-12-23 15:22:51.000', '2024-12-23 15:22:51.000', NULL,NULL,NULL,NULL,NULL);

# Insert category
INSERT INTO nike.category
(id, name, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(1, 'Men', 'admin', '2025-03-04 09:24:08', NULL, '2025-03-04 09:24:08', 0);
INSERT INTO nike.category
(id, name, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(2, 'Women', 'admin', '2025-03-04 09:24:16', NULL, '2025-03-04 09:24:16', 0);
INSERT INTO nike.category
(id, name, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(3, 'Kids', 'admin', '2025-03-04 09:24:24', NULL, '2025-03-04 09:24:24', 0);
INSERT INTO nike.category
(id, name, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(4, 'New & Featured', 'admin', '2025-03-04 09:24:35', NULL, '2025-03-04 09:24:35', 0);
# Insert kind
INSERT INTO nike.kind
(id, name, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(1, 'Shoes', 'admin', '2025-03-04 09:25:06', NULL, '2025-03-04 09:25:06', 0);
INSERT INTO nike.kind
(id, name, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(2, 'Clothing', 'admin', '2025-03-04 09:25:16', NULL, '2025-03-04 09:25:16', 0);
INSERT INTO nike.kind
(id, name, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(3, 'Shop By Sport', 'admin', '2025-03-04 09:25:34', NULL, '2025-03-04 09:25:34', 0);
INSERT INTO nike.kind
(id, name, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(4, 'Featured', 'admin', '2025-03-04 09:25:43', NULL, '2025-03-04 09:25:43', 0);


# Insert image
INSERT INTO nike.image
(id, name, `path`, folder, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(1, 'sale_1741156375.jpg', 'upload/sale/sale_1741156375.jpg', 'sale', NULL, '2025-03-05 06:32:55', NULL, '2025-03-05 06:32:55', 0);

# Insert sale
INSERT INTO nike.sale
(id, name, discount, start_date, end_date, created_user, created_date, updated_user, updated_date, flg_del, image_id)
VALUES(1, 'Siêu sale tháng 3 %%%', 20, '2025-03-05', '2025-03-31', 'admin', '2025-03-05 06:32:55', NULL, '2025-03-05 06:32:55', 0, 1);
