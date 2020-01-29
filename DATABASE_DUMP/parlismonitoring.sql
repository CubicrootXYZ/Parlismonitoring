-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: 
-- Erstellungszeit: 29. Jan 2020 um 14:50
-- Server-Version: 8.0.17
-- PHP-Version: 7.2.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `parlismonitoring`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `parlis_monitoring_authors`
--

CREATE TABLE `parlis_monitoring_authors` (
  `id` int(11) NOT NULL,
  `time` timestamp NULL DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `parlis_monitoring_authors_files`
--

CREATE TABLE `parlis_monitoring_authors_files` (
  `id` int(11) NOT NULL,
  `time` timestamp NULL DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `file_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `parlis_monitoring_files`
--

CREATE TABLE `parlis_monitoring_files` (
  `id` int(11) NOT NULL,
  `time` timestamp NULL DEFAULT NULL,
  `title` varchar(1000) DEFAULT NULL,
  `number` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `link` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `parlis_monitoring_files_keywords`
--

CREATE TABLE `parlis_monitoring_files_keywords` (
  `id` int(11) NOT NULL,
  `time` timestamp NULL DEFAULT NULL,
  `word_id` int(11) DEFAULT NULL,
  `file_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `parlis_monitoring_files_keywords_content`
--

CREATE TABLE `parlis_monitoring_files_keywords_content` (
  `id` int(11) NOT NULL,
  `time` timestamp NULL DEFAULT NULL,
  `word_id` int(11) DEFAULT NULL,
  `file_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `parlis_monitoring_keywords`
--

CREATE TABLE `parlis_monitoring_keywords` (
  `id` int(11) NOT NULL,
  `time` timestamp NULL DEFAULT NULL,
  `word` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `parlis_monitoring_authors`
--
ALTER TABLE `parlis_monitoring_authors`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `parlis_monitoring_authors_files`
--
ALTER TABLE `parlis_monitoring_authors_files`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `parlis_monitoring_files`
--
ALTER TABLE `parlis_monitoring_files`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `parlis_monitoring_files_keywords`
--
ALTER TABLE `parlis_monitoring_files_keywords`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `parlis_monitoring_files_keywords_content`
--
ALTER TABLE `parlis_monitoring_files_keywords_content`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `parlis_monitoring_keywords`
--
ALTER TABLE `parlis_monitoring_keywords`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `parlis_monitoring_authors`
--
ALTER TABLE `parlis_monitoring_authors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `parlis_monitoring_authors_files`
--
ALTER TABLE `parlis_monitoring_authors_files`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `parlis_monitoring_files`
--
ALTER TABLE `parlis_monitoring_files`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `parlis_monitoring_files_keywords`
--
ALTER TABLE `parlis_monitoring_files_keywords`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `parlis_monitoring_files_keywords_content`
--
ALTER TABLE `parlis_monitoring_files_keywords_content`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `parlis_monitoring_keywords`
--
ALTER TABLE `parlis_monitoring_keywords`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
