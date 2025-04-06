-- Create the Database if it doesn't exist
CREATE DATABASE IF NOT EXISTS lucerne_boutique;

USE lucerne_boutique;

-- Suppliers Table
CREATE TABLE IF NOT EXISTS Suppliers (
    Supplier_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Phone VARCHAR(15),
    Address VARCHAR(255)
);

-- Customers Table
CREATE TABLE IF NOT EXISTS Customers (
    Customer_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL
);

-- CustomerPhones Table (Normalization)
CREATE TABLE IF NOT EXISTS CustomerPhones (
    Phone_ID INT AUTO_INCREMENT PRIMARY KEY,
    Customer_ID INT NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID) ON DELETE CASCADE
);

-- Products Table
CREATE TABLE IF NOT EXISTS Products (
    Product_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Type VARCHAR(50),
    Price DECIMAL(10, 2) NOT NULL,
    Stock_Level INT NOT NULL,
    Supplier_ID INT,
    Product_Image_Path VARCHAR(255), -- Storing the image file path or URL
    FOREIGN KEY (Supplier_ID) REFERENCES Suppliers(Supplier_ID) ON DELETE CASCADE
);


-- Discounts Table
CREATE TABLE IF NOT EXISTS Discounts (
    Discount_ID INT AUTO_INCREMENT PRIMARY KEY,
    Code VARCHAR(20) NOT NULL,
    Discount_Percentage DECIMAL(5, 2) NOT NULL,
    Start_Date DATE NOT NULL,
    End_Date DATE NOT NULL,
    Status VARCHAR(20) NOT NULL
);

-- Sales Transactions Table
CREATE TABLE IF NOT EXISTS Sales_Transactions (
    Transaction_ID INT AUTO_INCREMENT PRIMARY KEY,
    Customer_ID INT NOT NULL,
    Transaction_Date DATE NOT NULL,
    Total_Amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID) ON DELETE CASCADE
);

-- Product Sales Table
-- Corrected Product Sales Table
CREATE TABLE IF NOT EXISTS Product_Sales (
    Product_Sales_ID INT AUTO_INCREMENT PRIMARY KEY,
    Transaction_ID INT NOT NULL,
    Product_ID INT NOT NULL,
    Customer_ID INT NOT NULL, -- Added Customer_ID column
    Quantity INT NOT NULL,
    Sale_Price DECIMAL(10, 2) NOT NULL,
    Discount_ID INT,
    Discount_Percentage DECIMAL(5, 2), -- Added column to store the discount percentage
    Total DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (Transaction_ID) REFERENCES Sales_Transactions(Transaction_ID) ON DELETE CASCADE,
    FOREIGN KEY (Product_ID) REFERENCES Products(Product_ID) ON DELETE CASCADE,
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID) ON DELETE CASCADE, -- Foreign key for Customer_ID
    FOREIGN KEY (Discount_ID) REFERENCES Discounts(Discount_ID) ON DELETE CASCADE
);


-- Users Table for Login and Sign-Up
CREATE TABLE IF NOT EXISTS Users (
    User_ID INT AUTO_INCREMENT PRIMARY KEY,
    Password VARCHAR(255) NOT NULL, -- Store hashed passwords
    Role ENUM('Manager', 'Employee') NOT NULL,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Initial Data for Suppliers
INSERT INTO Suppliers (Name, Phone, Address) VALUES
('Luxury Supplies Co.', '0591234567', '123 Luxury St, Cityville'),
('Clothing Masters', '0599876543', '456 Fashion Ave, Styleton');

-- Insert Initial Data for Customers
INSERT INTO Customers (Name) VALUES
('Khadija Al-Qasim'),
('Amal Al-Fahad');

-- Insert Initial Data for Customer Phones
INSERT INTO CustomerPhones (Customer_ID, Phone) VALUES
(1, '0591122334'),
(2, '0592233445');

-- Insert Initial Data for Products with Image Paths
INSERT INTO Products (Name, Type, Price, Stock_Level, Supplier_ID, Product_Image_Path) VALUES
('Black Boots', 'Footwear', 150.00, 25, 1, 'C:/Users/Ziad/Downloads/471443202_1147886564008054_1345586819978854992_n.jpg'),
('White Top', 'Clothing', 120.00, 20, 2, 'C:/Users/Ziad/Downloads/471782759_1147886567341387_3067979125738125079_n.jpg'),
('Brown Boots', 'Footwear', 180.00, 10, 1, 'C:/Users/Ziad/Downloads/462549595_567464309625057_3245448140960918667_n.jpg'),
('Luxury Watch', 'Jewelry', 500.00, 15, 1, 'C:/Users/Ziad/Downloads/462577594_668848415710850_2250199333766038299_n.jpg'),
('Evening Gown', 'Clothing', 400.00, 30, 2, 'C:/Users/Ziad/Downloads/462577740_1277005453620710_3247109509920062618_n.jpg');


-- Insert Initial Data for Discounts
INSERT INTO Discounts (Code, Discount_Percentage, Start_Date, End_Date, Status) VALUES
('HOLIDAY20', 20.00, '2024-12-01', '2024-12-31', 'Active'),
('WINTER5', 5.00, '2024-12-01', '2024-12-31', 'Active');

-- Insert Initial Data for Sales Transactions
INSERT INTO Sales_Transactions (Customer_ID, Transaction_Date, Total_Amount) VALUES
(1, '2024-12-06', 850.00),
(2, '2024-12-07', 600.00);

-- Insert Initial Data for Product Sales with Discount
INSERT INTO Product_Sales (Transaction_ID, Product_ID, Customer_ID, Quantity, Sale_Price, Discount_ID, Discount_Percentage, Total) 
VALUES (1, 1, 1, 1, 500.00, NULL, NULL, 500.00);


-- Insert Initial Data for Users (Manager and Employee)
INSERT INTO Users (Password, Role) VALUES
('123', 'Manager'), 
('1234', 'Employee');