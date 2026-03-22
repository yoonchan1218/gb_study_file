use ddl;

CREATE TABLE tbl_movie (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    director VARCHAR(100) NOT NULL,
    release_year INT NOT NULL,
    running_time INT NOT NULL COMMENT '상영시간(분)',
    rating DECIMAL(3,1) DEFAULT 0.0 COMMENT '평점(0.0~10.0)',
    genre VARCHAR(20) NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

select * from tbl_movie;

CREATE TABLE tbl_product (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(200) NOT NULL,
    price INT NOT NULL,
    stock INT DEFAULT 0,
    category VARCHAR(20) NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

select id, product_name, price, stock, category, created, updated
from tbl_product;

CREATE TABLE tbl_order (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100) NOT NULL,
    customer_email VARCHAR(100) NOT NULL,
    total_amount INT DEFAULT 0,
    order_status VARCHAR(20) NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE tbl_order_item (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity INT NOT NULL,
    price INT NOT NULL COMMENT '주문 당시 가격',
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES tbl_order(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES tbl_product(id)
);

select p.product_name, p.price, p.stock, p.category, o.customer_name, o.total_amount, o.order_status,
oi.id, oi.quantity, oi.price
from tbl_product p join tbl_order_item oi 
on p.id = oi.product_id
join tbl_order o 
on oi.order_id = o.id;