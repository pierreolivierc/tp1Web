-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mar. 26 sep. 2023 à 18:54
-- Version du serveur : 8.0.31
-- Version de PHP : 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `tp1_troqueur`
--

-- --------------------------------------------------------

--
-- Structure de la table `categories`
--

DROP TABLE IF EXISTS `categories`;
CREATE TABLE IF NOT EXISTS `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `description_UNIQUE` (`description`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `categories`
--

INSERT INTO `categories` (`id`, `description`) VALUES
(3, 'Neuf'),
(1, 'Occasion'),
(2, 'Presque neuf');

-- --------------------------------------------------------

--
-- Structure de la table `objets`
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `objets`
--

INSERT INTO `objets` (`id`, `titre`, `description`, `photo`, `categorie`, `date`) VALUES
(1, 'Honda civic 2018', 'Raison de la vente: moteur a sauté', '2023-09-26-14h45m36.jpg', 1, '2023-09-26'),
(2, 'Meuble de tv', 'À donner ', '2023-09-26-14h50m09.jpg', 1, '2023-09-26'),
(3, 'Compte interdit: Peter pan', 'Très bon, je recommande!', '2023-09-26-14h52m46.jpg', 1, '2023-09-26'),
(4, 'Télévision 55po', 'Ne marche plus, vendu pour pièce', '2023-09-26-14h53m36.jpg', 1, '2023-09-26'),
(5, 'GTA V', 'J\'ai volé le jeu chez EBGame. À qui la chance', '2023-09-26-14h54m24.jpg', 3, '2023-09-26');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
