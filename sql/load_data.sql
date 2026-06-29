LOAD DATA LOCAL INFILE "data/raw/SupplyChainDT.csv"
INTO TABLE order_delivery_analysis
CHARACTER SET latin1
FIELDS TERMINATED BY ','   
ENCLOSED BY '"'  
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(
    `Type`,
    `Days for shipping (real)`,
    `Days for shipment (scheduled)`,
    `Benefit per order`,
    `Sales per customer`,
    `Delivery Status`,
    `Late_delivery_risk`,
    `Category Id`,
    `Category Name`,
    `Customer City`,
    `Customer Country`,
    `Customer Email`,
    `Customer Fname`,
    `Customer Id`,
    `Customer Lname`,
    `Customer Password`,
    `Customer Segment`,
    `Customer State`,
    `Customer Street`,
    `Customer Zipcode`,
    `Department Id`,
    `Department Name`,
    `Latitude`,
    `Longitude`,
    `Market`,
    `Order City`,
    `Order Country`,
    `Order Customer Id`,
    @order_date, 
    `Order Id`,
    `Order Item Cardprod Id`,
    `Order Item Discount`,
    `Order Item Discount Rate`,
    `Order Item Id`,
    `Order Item Product Price`,
    `Order Item Profit Ratio`,
    `Order Item Quantity`,
    `Sales`,
    `Order Item Total`,
    `Order Profit Per Order`,
    `Order Region`,
    `Order State`,
    `Order Status`,
    `Order Zipcode`,
    `Product Card Id`,
    `Product Category Id`,
    `Product Description`,
    `Product Image`,
    `Product Name`,
    `Product Price`,
    `Product Status`,
    @shipping_date,
    `Shipping Mode`
)
SET 
    `order date (DateOrders)` = STR_TO_DATE(@order_date, '%c/%e/%Y %H:%i'), 
    `shipping date (DateOrders)` = STR_TO_DATE(@shipping_date, '%c/%e/%Y %H:%i');

