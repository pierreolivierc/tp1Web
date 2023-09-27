-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Sep 27, 2023 at 04:57 PM
-- Server version: 8.0.31
-- PHP Version: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tp1_troqueur`
--

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
CREATE TABLE IF NOT EXISTS `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `description_UNIQUE` (`description`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `description`) VALUES
(3, 'Neuf'),
(1, 'Occasion'),
(2, 'Presque neuf');

-- --------------------------------------------------------

--
-- Table structure for table `objets`
--

DROP TABLE IF EXISTS `objets`;
CREATE TABLE IF NOT EXISTS `objets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titre` varchar(50) NOT NULL,
  `description` varchar(2000) NOT NULL,
  `photo` varchar(50) DEFAULT NULL,
  `categorie` int NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `objets`
--

INSERT INTO `objets` (`id`, `titre`, `description`, `photo`, `categorie`, `date`) VALUES
(1, 'Honda civic 2018', 'Raison de la vente: moteur a sauté', '2023-09-26-14h45m36.jpg', 1, '2023-09-26'),
(2, 'Meuble de tv', 'À donner ', '2023-09-26-15h25m30.jpg', 1, '2023-09-26'),
(3, 'Compte interdit: Peter pan', 'Très bon, je recommande!', '2023-09-26-14h52m46.jpg', 1, '2023-09-26'),
(4, 'Télévision 55po', 'Ne marche plus, vendu pour pièce', '2023-09-26-15h44m34.jpg', 1, '2023-09-26'),
(5, 'GTA V', 'J\'ai volé le jeu chez EBGame. À qui la chance', '2023-09-26-14h54m24.jpg', 3, '2023-09-26'),
(6, 'PS5', 'c\'est moi qui a volé le jeu GTA V. GUESS WHAT. J\'ai volé la ps5 avec, mais elle ne va pas bien', '2023-09-26-21h01m35.jpg', 1, '2023-09-26'),
(7, 'Toyota corolla 2022', 'À vendre, mais sans les roues.', '2023-09-27-09h20m52.jpg', 1, '2023-09-27'),
(8, 'Télévision 20 pouces', 'Raison de la vente, j\'ai acheté un mp3', 'image_par_default.jpg', 1, '2023-09-27'),
(9, 'Xbox', 'J\'ai acheté 8 xbox et je veux les vendre 3 fois le prix.', '2023-09-27-09h30m17.jpg', 1, '2023-09-27');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
