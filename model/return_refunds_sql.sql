-- Create the return_refunds table if it doesn't exist
CREATE TABLE IF NOT EXISTS return_refunds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Pending',
    request_date DATETIME NOT NULL,
    processed_date DATETIME,
    refund_amount FLOAT,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

-- Insert additional dummy data
INSERT INTO return_refunds 
(order_id, user_id, product_id, reason, status, request_date, processed_date, refund_amount)
VALUES 
(1, 1, 5, 'Product arrived damaged', 'Approved', '2025-04-15 10:30:00', '2025-04-18 14:45:00', 299.99),
(1, 1, 7, 'Wrong item received', 'Rejected', '2025-04-10 09:15:00', '2025-04-12 11:20:00', NULL),
(1, 1, 8, 'Product not as described', 'Processing', '2025-04-20 16:45:00', NULL, NULL),
(1, 1, 5, 'Missing parts or accessories', 'Completed', '2025-04-05 13:20:00', '2025-04-08 09:30:00', 149.50),
(1, 1, 7, 'Arrived too late', 'Pending', '2025-04-25 18:10:00', NULL, NULL);
