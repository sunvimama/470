-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 12, 2025 at 03:06 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `etech`
--

-- --------------------------------------------------------

--
-- Table structure for table `coupon`
--

CREATE TABLE `coupon` (
  `id` int(11) NOT NULL,
  `code` varchar(50) NOT NULL,
  `discount_amount` float NOT NULL,
  `is_percentage` tinyint(1) DEFAULT NULL,
  `valid_from` datetime DEFAULT NULL,
  `valid_to` datetime DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `coupon`
--

INSERT INTO `coupon` (`id`, `code`, `discount_amount`, `is_percentage`, `valid_from`, `valid_to`, `is_active`) VALUES
(1, 'WELCOME10', 10, 1, NULL, NULL, 1),
(2, 'SAVE20', 20, 1, NULL, NULL, 1),
(3, 'FLAT50', 50, 0, NULL, NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `emi_plans`
--

CREATE TABLE `emi_plans` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `emi_duration` int(11) NOT NULL,
  `emi_amount` decimal(10,2) NOT NULL,
  `payment_method` varchar(50) NOT NULL,
  `status` varchar(50) DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `message` varchar(255) NOT NULL,
  `is_read` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `notification_type` varchar(50) DEFAULT NULL,
  `related_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `user_id`, `message`, `is_read`, `created_at`, `notification_type`, `related_id`) VALUES
(1, 1, 'You added palworld to your wishlist', 1, '2025-05-03 16:04:51', 'wishlist', 10),
(2, 1, 'palworld is back in stock!', 1, '2025-05-03 16:05:13', 'restock', 10),
(3, 1, 'New product added: rex', 1, '2025-05-03 16:18:06', 'new_product', 11),
(4, 2, 'New product added: rex', 0, '2025-05-03 16:18:06', 'new_product', 11),
(5, 3, 'New product added: rex', 0, '2025-05-03 16:18:06', 'new_product', 11),
(6, 4, 'New product added: rex', 0, '2025-05-03 16:18:06', 'new_product', 11),
(7, 5, 'New product added: rex', 0, '2025-05-03 16:18:06', 'new_product', 11),
(8, 6, 'New product added: rex', 0, '2025-05-03 16:18:06', 'new_product', 11),
(9, 1, 'You added AK-47 to your wishlist', 1, '2025-05-03 18:43:50', 'wishlist', 9),
(10, 1, 'AK-47 is back in stock!', 1, '2025-05-03 18:46:34', 'restock', 9),
(11, 1, 'You added prime  to your wishlist', 1, '2025-05-03 19:07:49', 'wishlist', 7),
(12, 1, 'You added emni to your wishlist', 1, '2025-05-12 13:01:14', 'wishlist', 5);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `status` varchar(50) NOT NULL,
  `order_date` datetime DEFAULT NULL,
  `delivery_date` datetime DEFAULT NULL,
  `coupon_code` varchar(50) DEFAULT NULL,
  `discount_amount` float DEFAULT NULL,
  `order_number` varchar(20) DEFAULT NULL,
  `address` varchar(200) NOT NULL DEFAULT '',
  `payment_method` varchar(50) NOT NULL DEFAULT 'cash_on_delivery',
  `total_price` float NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `product_id`, `quantity`, `status`, `order_date`, `delivery_date`, `coupon_code`, `discount_amount`, `order_number`, `address`, `payment_method`, `total_price`) VALUES
(1, 1, NULL, NULL, 'Processing', '2025-05-02 14:25:38', NULL, 'WELCOME10', 62.1, 'TBZ199990YEZ', 'fguywf', 'cash_on_delivery', 558.9),
(2, 1, NULL, NULL, 'Processing', '2025-05-03 21:20:01', NULL, NULL, NULL, 'TBZ265055RHW', 'aftabnagar', 'emi', 650050),
(3, 1, NULL, NULL, 'Processing', '2025-05-03 21:39:33', NULL, NULL, NULL, 'TBZ440649SKF', 'ghu', 'emi', 650046),
(4, 1, NULL, NULL, 'Processing', '2025-05-03 21:57:44', NULL, NULL, NULL, 'TBZ635437FUG', 'kkk', 'emi', 650184),
(5, 1, NULL, NULL, 'Processing', '2025-05-03 22:01:36', NULL, NULL, NULL, 'TBZ500917WDF', 'qeqeqwewe', 'emi', 650023),
(6, 1, NULL, NULL, 'Processing', '2025-05-03 22:02:19', NULL, NULL, NULL, 'TBZ929078RGY', 'qeqeqwewe', 'emi', 650023),
(7, 1, NULL, NULL, 'Processing', '2025-05-03 22:04:24', NULL, NULL, NULL, 'TBZ121067EDI', 'ww', 'emi', 100000),
(8, 1, NULL, NULL, 'Processing', '2025-05-03 22:09:29', NULL, NULL, NULL, 'TBZ573674WBC', 's', 'credit_card', 20),
(9, 1, NULL, NULL, 'Processing', '2025-05-03 22:09:59', NULL, NULL, NULL, 'TBZ801499MXA', 'sx', 'credit_card', 650000),
(10, 1, NULL, NULL, 'Processing', '2025-05-03 22:10:27', NULL, NULL, NULL, 'TBZ234290LXY', 'trt', 'emi', 650000),
(11, 1, NULL, NULL, 'Processing', '2025-05-04 00:42:14', NULL, NULL, NULL, 'TBZ427807CZE', 'adwawdaw', 'credit_card', 650000),
(12, 1, NULL, NULL, 'Processing', '2025-05-04 00:43:15', NULL, NULL, NULL, 'TBZ770144OPR', 'qeqeqwewe', 'credit_card', 650000),
(13, 1, NULL, NULL, 'Processing', '2025-05-04 00:43:26', NULL, NULL, NULL, 'TBZ519129OPH', ';', 'credit_card', 650000),
(14, 1, NULL, NULL, 'Processing', '2025-05-04 00:46:06', NULL, NULL, NULL, 'TBZ787675PPE', 'c', 'credit_card', 650000);

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `product_id`, `product_name`, `quantity`, `price`) VALUES
(1, 1, 5, 'emni', 27, 23),
(2, 2, 7, 'prime ', 1, 20),
(3, 2, 8, 'gatorade', 1, 30),
(4, 2, 9, 'AK-47', 1, 650000),
(5, 3, 5, 'emni', 2, 23),
(6, 3, 9, 'AK-47', 1, 650000),
(7, 4, 5, 'emni', 8, 23),
(8, 4, 9, 'AK-47', 1, 650000),
(9, 5, 5, 'emni', 1, 23),
(10, 5, 9, 'AK-47', 1, 650000),
(11, 6, 5, 'emni', 1, 23),
(12, 6, 9, 'AK-47', 1, 650000),
(13, 7, 10, 'palworld', 1, 100000),
(14, 8, 7, 'prime ', 1, 20),
(15, 9, 9, 'AK-47', 1, 650000),
(16, 10, 9, 'AK-47', 1, 650000),
(17, 11, 9, 'AK-47', 1, 650000),
(18, 12, 9, 'AK-47', 1, 650000),
(19, 13, 9, 'AK-47', 1, 650000),
(20, 14, 9, 'AK-47', 1, 650000);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `price` float NOT NULL,
  `stock` int(11) NOT NULL,
  `image_url` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`id`, `name`, `description`, `price`, `stock`, `image_url`) VALUES
(5, 'emni', 'bollam na emni', 23, 6, 'https://www.shutterstock.com/image-photo/bengali-dish-khichdi-khichuri-made-260nw-2208250485.jpg'),
(7, 'prime ', 'logan paul bro', 20, 19, 'https://drinkprime.com/cdn/shop/files/Sournova_Web_DropBanner_PDP_Front_2000x2000_ffba587e-02f2-491a-a375-5f5b3e7f2eb8_1200x.png?v=1744126206'),
(8, 'gatorade', 'prime er enemy', 30, 21, 'https://americanfizz.co.uk/media/catalog/product/cache/6b10d57cd8d541100491edcb64c52781/g/a/gatorade_cool_blue_canadian.png'),
(9, 'AK-47', '', 650000, 2, ''),
(10, 'palworld', '3233', 100000, 15, 'https://www.shutterstock.com/image-photo/bengali-dish-khichdi-khichuri-made-260nw-2208250485.jpg'),
(11, 'rex', 'so coolk', 12, 12, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTofDm5VuRbkmrsFkkfa8zJiHa-C5n7rGsWkQ&s');

-- --------------------------------------------------------

--
-- Table structure for table `return_refunds`
--

CREATE TABLE `return_refunds` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `reason` text NOT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'Pending',
  `request_date` datetime NOT NULL,
  `processed_date` datetime DEFAULT NULL,
  `refund_amount` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `return_refunds`
--

INSERT INTO `return_refunds` (`id`, `order_id`, `user_id`, `product_id`, `reason`, `status`, `request_date`, `processed_date`, `refund_amount`) VALUES
(1, 1, 2, 5, 'Quality not as expected', 'Pending', '2025-04-25 23:00:35', NULL, NULL),
(2, 1, 2, 5, 'Found a better price elsewhere', 'Completed', '2025-04-05 23:00:35', '2025-04-07 23:00:35', 162.53),
(3, 1, 4, 8, 'Changed my mind', 'Pending', '2025-04-07 23:00:35', NULL, NULL),
(4, 1, 5, 5, 'Product is defective', 'Completed', '2025-04-02 23:00:35', '2025-04-09 23:00:35', 232.34),
(5, 1, 4, 5, 'Ordered by mistake', 'Pending', '2025-04-09 23:00:35', NULL, NULL),
(6, 1, 1, 7, 'Wrong item received', 'Completed', '2025-04-28 23:00:35', '2025-05-04 23:00:35', 347.02),
(7, 1, 1, 7, 'Changed my mind', 'Approved', '2025-04-23 23:00:35', '2025-04-25 23:00:35', 353.28),
(8, 1, 5, 8, 'Missing parts or accessories', 'Rejected', '2025-04-21 23:00:35', '2025-04-25 23:00:35', NULL),
(9, 1, 1, 5, 'Missing parts or accessories', 'Completed', '2025-04-18 23:00:35', '2025-04-23 23:00:35', 224.66),
(10, 1, 3, 7, 'Quality not as expected', 'Processing', '2025-04-16 23:00:35', '2025-04-21 23:00:35', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `review`
--

CREATE TABLE `review` (
  `id` int(11) NOT NULL,
  `content` text NOT NULL,
  `rating` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `review`
--

INSERT INTO `review` (`id`, `content`, `rating`, `user_id`, `product_id`, `timestamp`) VALUES
(18, 'Bought this for my sister and they returned it. It works exactly as described. highly recommend it.', 4, 4, 5, '2025-04-15 00:13:56'),
(19, 'The quality is good. It\'s not as durable as I expected. Overall, I can\'t stand it and would only recommend it if on sale.', 4, 5, 5, '2025-04-17 00:13:56'),
(21, 'I\'ve been using this for six months now and it\'s good. recommend it with some reservations.', 3, 6, 5, '2025-04-19 00:13:56'),
(23, 'Bought this for my dad and they loved it. It\'s missing some key features. highly recommend it.', 4, 3, 5, '2025-04-22 00:13:56'),
(24, 'baje goindho\r\n', 2, 1, 5, '2025-05-12 19:01:41');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `Name` varchar(50) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Nid` int(11) NOT NULL,
  `is_admin` tinyint(1) NOT NULL DEFAULT 0,
  `id` int(11) NOT NULL,
  `phone` int(11) NOT NULL,
  `password` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`Name`, `Email`, `Nid`, `is_admin`, `id`, `phone`, `password`) VALUES
('sunvimama', 'afifsunvi@gmail.com', 222332323, 1, 1, 1762591405, '$2b$12$14QtlMyLpH7nGwbqr6U1Lu10.0Xw7lyWV6MTxZ6TvhgiJTAw62Pge'),
('Emma Johnson', 'user1@example.com', 1000000, 0, 2, 1000000000, '$2b$12$xad8MRcUBTM3N/x7KikqK.2bkw996C3vPpEUaMwALLq4Fzw4iKin.'),
('Emily Davis', 'user2@example.com', 1000001, 0, 3, 1000000001, '$2b$12$zx8IghWA2c97WTD2i1VciuyQXX6OQaxi3sCA88/yuNNzyN2WHVaa2'),
('Michael Brown', 'user3@example.com', 1000002, 0, 4, 1000000002, '$2b$12$WkDqTwC7Ulw.8eBKVayj.OkVDIznLREiYSfRYTSwny.DP/xTew2hG'),
('Sarah Davis', 'user4@example.com', 1000003, 0, 5, 1000000003, '$2b$12$Q9bzjvUX6Fb1hU26RVAYZuuAaCzRHa/ENoPlbPlIF90ZI6KUvtBWK'),
('Jane Johnson', 'user5@example.com', 1000004, 0, 6, 1000000004, '$2b$12$F/QMvpxtnxI8sxJEjwjdT.cYxPWAasBghc/EGO/H1D/qPxPg8krpm'),
('hiii', 'wer@gmail.com', 22334455, 0, 7, 2147483647, '$2b$12$JBVWG80xuH8Z.ngO/7g7Vee2amUYq45TfPKtz5bxzjK3BseSgd/ym');

-- --------------------------------------------------------

--
-- Table structure for table `user_product_views`
--

CREATE TABLE `user_product_views` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `view_count` int(11) DEFAULT NULL,
  `last_viewed` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `wishlist`
--

CREATE TABLE `wishlist` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `wishlist`
--

INSERT INTO `wishlist` (`id`, `user_id`, `product_id`) VALUES
(7, 1, 5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `coupon`
--
ALTER TABLE `coupon`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `emi_plans`
--
ALTER TABLE `emi_plans`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `order_id` (`order_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `order_number` (`order_number`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `return_refunds`
--
ALTER TABLE `return_refunds`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `review`
--
ALTER TABLE `review`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `phone` (`phone`),
  ADD UNIQUE KEY `Nid` (`Nid`);

--
-- Indexes for table `user_product_views`
--
ALTER TABLE `user_product_views`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `wishlist`
--
ALTER TABLE `wishlist`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `coupon`
--
ALTER TABLE `coupon`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `emi_plans`
--
ALTER TABLE `emi_plans`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `return_refunds`
--
ALTER TABLE `return_refunds`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `review`
--
ALTER TABLE `review`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `user_product_views`
--
ALTER TABLE `user_product_views`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `wishlist`
--
ALTER TABLE `wishlist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `emi_plans`
--
ALTER TABLE `emi_plans`
  ADD CONSTRAINT `emi_plans_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `emi_plans_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`);

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`);

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`);

--
-- Constraints for table `return_refunds`
--
ALTER TABLE `return_refunds`
  ADD CONSTRAINT `return_refunds_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  ADD CONSTRAINT `return_refunds_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `return_refunds_ibfk_3` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`);

--
-- Constraints for table `review`
--
ALTER TABLE `review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `review_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`);

--
-- Constraints for table `user_product_views`
--
ALTER TABLE `user_product_views`
  ADD CONSTRAINT `user_product_views_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `user_product_views_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`);

--
-- Constraints for table `wishlist`
--
ALTER TABLE `wishlist`
  ADD CONSTRAINT `wishlist_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `wishlist_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
