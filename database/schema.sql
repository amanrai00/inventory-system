CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'employee',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  sku VARCHAR(50) UNIQUE NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  stock_quantity INT DEFAULT 0,
  minimum_stock_level INT DEFAULT 10,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sales (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  quantity_sold INT NOT NULL,
  sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO users (name, email, password_hash, role)
SELECT
  'Admin',
  'admin@company.com',
  'pbkdf2:sha256:600000$5byikAyR1mJkUmR2$444e52548248dcbd6f7852c4582ef2f54bdf2a46f8119de8d76ada5a4b322614',
  'admin'
FROM DUAL
WHERE NOT EXISTS (
  SELECT 1
  FROM users
  WHERE email = 'admin@company.com'
);

-- AI demand predictions (added April 2026)
CREATE TABLE IF NOT EXISTS `predictions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `recommended_restock_qty` int DEFAULT NULL,
  `reasoning` text,
  `predicted_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `predictions_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
