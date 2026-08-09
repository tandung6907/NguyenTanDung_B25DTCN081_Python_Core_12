-- Script SQL Khởi Tạo CSDL MySQL Workbench Quan Hệ 1-N (Day 12)
-- Dự án: Quản Lý Thư Viện (library_management)
-- Rikkei Education - Python & FastAPI

CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- 1. Bảng Tác giả (Bảng Cha 1)
CREATE TABLE IF NOT EXISTS authors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Bảng Sách (Bảng Con N có Khóa Ngoại)
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    author_id INT NOT NULL,
    borrow_count INT DEFAULT 0,
    available_quantity INT DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_books_authors FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Dữ liệu mẫu khởi tạo (DML Datasets)
INSERT INTO authors (name, email, bio) VALUES
('Nguyễn Văn An', 'an.nguyen@rikkei.edu.vn', 'Chuyên gia Lập trình Python & Web Architecture'),
('Trần Thị Bình', 'binh.tran@rikkei.edu.vn', 'Tác giả sách FastAPI và Microservices'),
('Lê Hoàng Cường', 'cuong.le@rikkei.edu.vn', 'Kỹ sư CSDL MySQL & ORM Optimization');

INSERT INTO books (title, price, author_id, borrow_count, available_quantity) VALUES
('Lập Trình Python Cơ Bản', 120000.0, 1, 45, 3),
('FastAPI Web Architecture', 250000.0, 2, 12, 15),
('MySQL & SQLAlchemy Masterclass', 180000.0, 3, 88, 2),
('Python Clean Code & Testing', 210000.0, 1, 30, 8);
