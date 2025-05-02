-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 23, 2025 at 05:15 PM
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
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `status` varchar(50) NOT NULL,
  `order_date` datetime DEFAULT NULL,
  `delivery_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(1, 'Sample Smartphone', 'A high-end smartphone with advanced features', 599.99, 10, 'https://via.placeholder.com/300x200'),
(2, 'Wireless Headphones', 'Noise-cancelling wireless headphones with 30-hour battery life', 199.99, 15, 'https://via.placeholder.com/300x200'),
(3, 'Ultra HD Smart TV', '55-inch 4K Ultra HD Smart TV with HDR', 899.99, 5, 'https://via.placeholder.com/300x200'),
(5, 'emni', 'bollam na emni', 23, 8, 'https://www.shutterstock.com/image-photo/bengali-dish-khichdi-khichuri-made-260nw-2208250485.jpg'),
(6, 'prime lemon', 'logan paul bro', 20, 20, 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMSEhISEhITFRUVFxYXFRcRFxYWGBIVFRcXFhUZFRUZHiggGBolGxYXITEhJSkrLi4uGB8zODMsNygtLisBCgoKDg0OGxAQGy0mICYtNS0tLS8tLS0tLS0tLS0vLS0tLS0tLS0tLS0vL'),
(7, 'prime ', 'logan paul bro', 20, 20, 'https://drinkprime.com/cdn/shop/files/Sournova_Web_DropBanner_PDP_Front_2000x2000_ffba587e-02f2-491a-a375-5f5b3e7f2eb8_1200x.png?v=1744126206'),
(8, 'gatorade', 'prime er enemy', 30, 21, 'https://americanfizz.co.uk/media/catalog/product/cache/6b10d57cd8d541100491edcb64c52781/g/a/gatorade_cool_blue_canadian.png');

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
(1, 'I\'ve been using this for three months now and it\'s disappointing. buy it again.', 1, 1, 2, '2025-04-17 03:44:38'),
(2, 'Bought this for my sister and they returned it. The design is sleek and modern. not recommend it.', 5, 1, 1, '2025-03-31 03:44:38'),
(3, 'amazing product. The price is a bit high for what you get. suggest looking at alternatives.', 2, 1, 3, '2025-04-17 03:44:38'),
(4, 'Bought this for my brother and they couldn\'t figure out how to use it. The interface is intuitive. recommend it with some reservations.', 2, 5, 1, '2025-03-30 03:45:49'),
(5, 'I\'ve been using this for a week now and it\'s exceptional. definitely recommend it.', 5, 2, 2, '2025-04-05 03:45:49'),
(6, 'This product is amazing! I adore it and would not recommend it.', 2, 3, 3, '2025-04-13 03:45:49'),
(7, 'Bought this for my dad and they loved it. The battery life is impressive. suggest looking at alternatives.', 5, 5, 3, '2025-04-14 03:45:49'),
(8, 'The quality is below average. It\'s perfect for everyday use. Overall, I am disappointed with it and would suggest looking at alternatives.', 1, 5, 2, '2025-03-30 03:45:49'),
(9, 'I\'ve been using this for a year now and it\'s average. recommend it with some reservations.', 3, 6, 1, '2025-04-11 03:45:49'),
(10, 'I\'ve been using this for a week now and it\'s mediocre. definitely recommend it.', 4, 4, 2, '2025-04-16 03:45:49'),
(11, 'The quality is good. The battery life is impressive. Overall, I love it and would suggest looking at alternatives.', 5, 3, 1, '2025-03-21 03:45:49'),
(12, 'The quality is decent. The battery life is impressive. Overall, I like it and would highly recommend it.', 4, 6, 3, '2025-03-29 03:45:49'),
(13, 'This product is outstanding! I appreciate it and would recommend it to everyone.', 3, 2, 3, '2025-04-04 03:45:49'),
(14, 'I\'ve been using this for three months now and it\'s excellent. buy it again.', 3, 3, 2, '2025-03-30 03:45:49'),
(15, 'The quality is top-notch. Setup was a breeze. Overall, I like it and would recommend it to everyone.', 1, 6, 2, '2025-04-05 03:45:49'),
(16, 'I\'ve been using this for two weeks now and it\'s subpar. only recommend it if on sale.', 4, 4, 3, '2025-03-30 03:45:49'),
(17, 'good', 4, 1, 1, '2025-04-20 19:20:20'),
(18, 'Bought this for my sister and they returned it. It works exactly as described. highly recommend it.', 4, 4, 5, '2025-04-15 00:13:56'),
(19, 'The quality is good. It\'s not as durable as I expected. Overall, I can\'t stand it and would only recommend it if on sale.', 4, 5, 5, '2025-04-17 00:13:56'),
(20, 'The quality is decent. The design is sleek and modern. Overall, I am disappointed with it and would buy it again.', 2, 2, 1, '2025-03-26 00:13:56'),
(21, 'I\'ve been using this for six months now and it\'s good. recommend it with some reservations.', 3, 6, 5, '2025-04-19 00:13:56'),
(22, 'decent product. It\'s perfect for everyday use. recommend it with some reservations.', 3, 4, 1, '2025-04-09 00:13:56'),
(23, 'Bought this for my dad and they loved it. It\'s missing some key features. highly recommend it.', 4, 3, 5, '2025-04-22 00:13:56');

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
('Jane Johnson', 'user5@example.com', 1000004, 0, 6, 1000000004, '$2b$12$F/QMvpxtnxI8sxJEjwjdT.cYxPWAasBghc/EGO/H1D/qPxPg8krpm');

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
(2, 1, 7),
(3, 1, 5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`id`);

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
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `review`
--
ALTER TABLE `review`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `wishlist`
--
ALTER TABLE `wishlist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`);

--
-- Constraints for table `review`
--
ALTER TABLE `review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `review_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`);

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
