-- Script de criação e população mínima do banco saep_db
-- Crie o banco (execute como superuser):
-- CREATE DATABASE saep_db;
-- Em seguida, conecte ao banco e execute as instruções abaixo.

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(80) UNIQUE NOT NULL,
  password VARCHAR(120) NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  code VARCHAR(50) UNIQUE NOT NULL,
  name VARCHAR(200) NOT NULL,
  brand VARCHAR(100),
  category VARCHAR(50),
  specs JSONB,
  quantity INTEGER NOT NULL DEFAULT 0,
  min_quantity INTEGER NOT NULL DEFAULT 1,
  price NUMERIC(12,2),
  warranty_months INTEGER,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS movements (
  id SERIAL PRIMARY KEY,
  product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  type VARCHAR(10) NOT NULL,
  amount INTEGER NOT NULL,
  responsible VARCHAR(120) NOT NULL,
  timestamp TIMESTAMP DEFAULT now()
);

-- Inserir ao menos 3 usuários
INSERT INTO users (username, password) VALUES
('admin','admin123'),
('estoquista','estoque2025'),
('usuario','senha123')
ON CONFLICT (username) DO NOTHING;

-- Inserir ao menos 3 produtos
INSERT INTO products (code, name, brand, category, specs, quantity, min_quantity, price, warranty_months) VALUES
('SPH-001', 'Smartphone Zeta 128GB', 'ZetaTech', 'smartphone',
 '{"storage":"128GB","screen":"6.1in FHD","battery":"4000mAh","connectivity":["4G","WiFi","Bluetooth"], "imei": null }', 15, 5, 1999.90, 12),
('NBK-002', 'Notebook CoreBook 15.6"', 'CoreInc', 'notebook',
 '{"cpu":"Intel i5","ram":"16GB","storage":"512GB SSD","screen":"15.6in FHD","battery":"6 cells"}', 8, 3, 4599.00, 24),
('TV-003', 'Smart TV Ultra 55" 4K', 'ViewMax', 'smart_tv',
 '{"screen":"55in 4K","hdmi":3,"smart_os":"ViewOS","voltage":"110-220V"}', 4, 2, 3199.00, 12);

-- Inserir movimentações de exemplo
INSERT INTO movements (product_id, type, amount, responsible) VALUES
(1,'in',5,'admin'),
(2,'out',1,'estoquista'),
(3,'in',3,'usuario');
