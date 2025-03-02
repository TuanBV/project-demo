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
    image VARCHAR(256),
    start_date DATE,
    end_date DATE,
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0
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

CREATE TABLE IF NOT EXISTS `image` (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(256),
    path VARCHAR(256),
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0
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

CREATE TABLE IF NOT EXISTS `image` (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    path VARCHAR(50),
    created_user VARCHAR(256),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_user VARCHAR(256),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    flg_del INTEGER DEFAULT 0
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


INSERT INTO nike.kind
(id, name, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(1, 'string', 'admin', '2025-02-28 08:43:34', NULL, '2025-02-28 08:43:34', 0);
INSERT INTO nike.kind
(id, name, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(2, 'Second Sale !!!', 'admin', '2025-02-28 10:10:23', NULL, '2025-02-28 10:10:23', 0);
INSERT INTO nike.kind
(id, name, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(3, 'Women', 'admin', '2025-02-28 10:10:57', NULL, '2025-02-28 10:10:57', 0);

INSERT INTO nike.category
(id, name, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(1, 'Men', 'admin', '2025-02-28 08:57:19', NULL, '2025-02-28 08:57:19', 0);
INSERT INTO nike.category
(id, name, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(2, 'Big Sale !!!', 'admin', '2025-02-28 09:54:39', NULL, '2025-02-28 09:54:39', 0);
INSERT INTO nike.category
(id, name, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(3, 'Big Sale !!', 'admin', '2025-02-28 10:11:12', NULL, '2025-02-28 10:11:12', 0);

INSERT INTO nike.image
(id, name, `path`, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(1, 'image_1740219078.jpg', 'upload/images/image_1740219078.jpg', 'admin', '2025-02-22 10:11:18', NULL, '2025-02-22 10:11:18', 0);
INSERT INTO nike.image
(id, name, `path`, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(2, 'image_1740219747.png', 'upload/images/image_1740219747.png', 'admin', '2025-02-22 10:22:27', NULL, '2025-02-22 10:22:27', 0);
INSERT INTO nike.image
(id, name, `path`, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(3, 'image_1740219997.jpg', 'upload/images/image_1740219997.jpg', 'admin', '2025-02-22 10:26:37', NULL, '2025-02-22 10:26:37', 0);

INSERT INTO nike.`user`
(user_id, username, email, fullname, password, token, `role`, flg_del, created_user, updated_user, created_date, updated_date, birthday, area, city, state, postcode)
VALUES('GryfqpgyoJEM7JEs42QN', 'admin', 'admin@gmail.com', 'admin', '$2b$12$BWex6PXXyVItz17nWaDh8u0pvM/EYZRAq5wAz6cvaSLRKHRw2isue', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZW1haWwiOiJhZG1pbkBnbWFpbC5jb20iLCJleHAiOjE3MzU2MjA5MjQuNjg3MjI1fQ.eY4RVWx3amDw4HoaPS3heQHLMECAiZnDpWmEEXyvTJE', 1, 0, NULL, NULL, '2024-12-23 15:20:31.000', '2024-12-23 15:20:31.000', NULL,NULL,NULL,NULL,NULL);
INSERT INTO nike.`user`
(user_id, username, email, fullname, password, token, `role`, flg_del, created_user, updated_user, created_date, updated_date, birthday, area, city, state, postcode)
VALUES('gWu8bXF7VMfAoBgLcIdj', 'demo', 'demo@gmail.com', 'demo', '$2b$12$nNCuavy2VNitM4H5LhTYRe7xYClvN9ormTR0gglG86WxNQiSy19qO', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRlbW8iLCJlbWFpbCI6ImRlbW9AZ21haWwuY29tIiwiZXhwIjoxNzM1NjIwODgyLjAwODU5Nn0.i0jk84tONI--n61Wqq8Z8ckNkcg94oEyWfbbrgDOdJE', 0, 0, NULL, NULL, '2024-12-23 15:22:51.000', '2024-12-23 15:22:51.000', NULL,NULL,NULL,NULL,NULL);

INSERT INTO nike.sale
(id, name, discount, image, start_date, end_date, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(1, 'Big Sale Month 1 !!!', 10, 'upload/sale/sale_1739775463.jpg', NULL, NULL, 'admin', '2025-02-17 06:57:43', NULL, '2025-02-17 06:58:44', 0);
INSERT INTO nike.sale
(id, name, discount, image, start_date, end_date, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(2, 'Big Sale Month 2 !!!', 20, 'upload/sale/sale_1739775478.jpg', NULL, NULL, 'admin', '2025-02-17 06:57:58', NULL, '2025-02-17 06:58:44', 0);
INSERT INTO nike.sale
(id, name, discount, image, start_date, end_date, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(3, 'Big Sale Month 3 !!!', 0, 'upload/sale/sale_1739775489.jpg', NULL, NULL, 'admin', '2025-02-17 06:58:09', NULL, '2025-02-17 06:58:44', 0);
INSERT INTO nike.sale
(id, name, discount, image, start_date, end_date, created_user, created_date, updated_user, updated_date, flg_del)
VALUES(4, 'Big Sale Month 4 !!!', 0, 'upload/sale/sale_1739775509.jpg', NULL, NULL, 'admin', '2025-02-17 06:58:29', NULL, '2025-02-17 06:58:44', 0);