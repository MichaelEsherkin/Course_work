
CREATE LOGIN testuser1   
    WITH PASSWORD = 'testpass1';  
GO  

CREATE DATABASE testbase1;

USE testbase1;

CREATE USER testuser1 FOR LOGIN testuser1;  
GO  

GRANT ALL TO testuser1;

GRANT CONTROL ON SCHEMA :: dbo TO testuser1;

GO

USE testbase1;

ALTER TABLE [Seller] DROP CONSTRAINT [fk_Seller_Order]
GO
ALTER TABLE [Client] DROP CONSTRAINT [fk_Client_Order]
GO
ALTER TABLE [Order] DROP CONSTRAINT [fk_Order_Details_order]
GO
ALTER TABLE [Manufacturer_name] DROP CONSTRAINT [fk_Manufacturer_Product]
GO
ALTER TABLE [Product] DROP CONSTRAINT [fk_Product_Details_order]
GO
ALTER TABLE [Product] DROP CONSTRAINT [fk_Product_Product_material]
GO
ALTER TABLE [Material] DROP CONSTRAINT [fk_Material_Product_material]
GO
ALTER TABLE [Details_order] DROP CONSTRAINT [fk_Details_order_Executable_orders]
GO
ALTER TABLE [Product] DROP CONSTRAINT [fk_Product_Product_price]
GO
ALTER TABLE [Service] DROP CONSTRAINT [fk_Service_Details_order]
GO
ALTER TABLE [Service] DROP CONSTRAINT [fk_Service_Service_price]
GO
ALTER TABLE [Manufacturer_country] DROP CONSTRAINT [fk_Manufacturer_country_Manufacturer_name_1]
GO

DROP TABLE [Order]
GO
DROP TABLE [Seller]
GO
DROP TABLE [Client]
GO
DROP TABLE [Manufacturer_name]
GO
DROP TABLE [Details_order]
GO
DROP TABLE [Product]
GO
DROP TABLE [Product_material]
GO
DROP TABLE [Material]
GO
DROP TABLE [Executable_orders]
GO
DROP TABLE [Product_price]
GO
DROP TABLE [Service]
GO
DROP TABLE [Service_price]
GO
DROP TABLE [Manufacturer_country]
GO

CREATE TABLE [Order] (
[id_order] int NOT NULL IDENTITY(1,1),
[id_client] int NOT NULL,
[id_seller] int NOT NULL,
[date_order] datetime NULL,
PRIMARY KEY ([id_order]) 
)
GO
CREATE TABLE [Seller] (
[id_seller] int NOT NULL IDENTITY(1,1),
[surname_seller] varchar(20) NOT NULL,
[name_seller] varchar(20) NOT NULL,
[patronymic_seller] varchar(20) NULL,
[phone_number_seller] varchar(20) NULL,
[position_seller] varchar(30) NOT NULL,
PRIMARY KEY ([id_seller]) 
)
GO
CREATE TABLE [Client] (
[id_client] int NOT NULL IDENTITY(1,1),
[surname_client] varchar(20) NOT NULL,
[name_client] varchar(20) NOT NULL,
[patronymic_client] varchar(20) NULL,
[phone_number_client] varchar(20) NULL,
PRIMARY KEY ([id_client]) 
)
GO
CREATE TABLE [Manufacturer_name] (
[id_manufacturer] int NOT NULL IDENTITY(1,1),
[name_manufacturer] varchar(40) NOT NULL,
[id_manufacturer_country] int NOT NULL,
PRIMARY KEY ([id_manufacturer]) 
)
GO
CREATE TABLE [Details_order] (
[id_details] int NOT NULL IDENTITY(1,1),
[id_service_price] int NULL,
[id_service] int NULL,
[id_product_price] int NULL,
[id_product] int NULL,
[id_order] int NOT NULL,
[count_details] int NULL,
PRIMARY KEY ([id_details]) 
)
GO
CREATE TABLE [Product] (
[id_product] int NOT NULL IDENTITY(1,1),
[id_manufacturer] int NOT NULL,
[name_product] varchar(20) NOT NULL,
[product_availability] smallint NOT NULL,
PRIMARY KEY ([id_product]) 
)
GO
CREATE TABLE [Product_material] (
[id_product_material] int NOT NULL IDENTITY(1,1),
[id_material] int NOT NULL,
[id_product] int NOT NULL,
PRIMARY KEY ([id_product_material]) 
)
GO
CREATE TABLE [Material] (
[id_material] int NOT NULL IDENTITY(1,1),
[name_material] varchar(20) NOT NULL,
PRIMARY KEY ([id_material]) 
)
GO
CREATE TABLE [Executable_orders] (
[id_queue] int NOT NULL IDENTITY(1,1),
[id_details] int NOT NULL,
[order_execution_date] datetime NULL,
[execute_queue] smallint NULL,
[ready] tinyint NOT NULL,
[date_ready] datetime NULL,
[condition] varchar(255) NULL,
PRIMARY KEY ([id_queue]) 
)
GO
CREATE TABLE [Product_price] (
[id_product_price] int NOT NULL IDENTITY(1,1),
[id_product] int NOT NULL,
[cost_product] money NOT NULL,
[price_list_date] datetime NOT NULL,
PRIMARY KEY ([id_product_price]) 
)
GO
CREATE TABLE [Service] (
[id_service] int NOT NULL IDENTITY(1,1),
[name_service] varchar(20) NOT NULL,
PRIMARY KEY ([id_service]) 
)
GO
CREATE TABLE [Service_price] (
[id_service_price] int NOT NULL IDENTITY(1,1),
[id_service] int NOT NULL,
[cost_service] money NOT NULL,
[price_list_date] datetime NOT NULL,
PRIMARY KEY ([id_service_price]) 
)
GO
CREATE TABLE [Manufacturer_country] (
[id_manufacturer_country] int NOT NULL IDENTITY(1,1),
[country_manufacturer] varchar(30) NOT NULL,
PRIMARY KEY ([id_manufacturer_country]) 
)
GO

ALTER TABLE [Seller] ADD CONSTRAINT [fk_Seller_Order] FOREIGN KEY ([id_seller]) REFERENCES [Order] ([id_seller])
GO
ALTER TABLE [Client] ADD CONSTRAINT [fk_Client_Order] FOREIGN KEY ([id_client]) REFERENCES [Order] ([id_client])
GO
ALTER TABLE [Order] ADD CONSTRAINT [fk_Order_Details_order] FOREIGN KEY ([id_order]) REFERENCES [Details_order] ([id_order])
GO
ALTER TABLE [Manufacturer_name] ADD CONSTRAINT [fk_Manufacturer_Product] FOREIGN KEY ([id_manufacturer]) REFERENCES [Product] ([id_manufacturer])
GO
ALTER TABLE [Product] ADD CONSTRAINT [fk_Product_Details_order] FOREIGN KEY ([id_product]) REFERENCES [Details_order] ([id_product])
GO
ALTER TABLE [Product] ADD CONSTRAINT [fk_Product_Product_material] FOREIGN KEY ([id_product]) REFERENCES [Product_material] ([id_product])
GO
ALTER TABLE [Material] ADD CONSTRAINT [fk_Material_Product_material] FOREIGN KEY ([id_material]) REFERENCES [Product_material] ([id_material])
GO
ALTER TABLE [Details_order] ADD CONSTRAINT [fk_Details_order_Executable_orders] FOREIGN KEY ([id_details]) REFERENCES [Executable_orders] ([id_details])
GO
ALTER TABLE [Product] ADD CONSTRAINT [fk_Product_Product_price] FOREIGN KEY ([id_product]) REFERENCES [Product_price] ([id_product])
GO
ALTER TABLE [Service] ADD CONSTRAINT [fk_Service_Details_order] FOREIGN KEY ([id_service]) REFERENCES [Details_order] ([id_service])
GO
ALTER TABLE [Service] ADD CONSTRAINT [fk_Service_Service_price] FOREIGN KEY ([id_service]) REFERENCES [Service_price] ([id_service])
GO
ALTER TABLE [Manufacturer_country] ADD CONSTRAINT [fk_Manufacturer_country_Manufacturer_name_1] FOREIGN KEY ([id_manufacturer_country]) REFERENCES [Manufacturer_name] ([id_manufacturer_country])
GO

