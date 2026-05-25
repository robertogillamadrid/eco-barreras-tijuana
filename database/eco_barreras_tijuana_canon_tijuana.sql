-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: eco_barreras_tijuana
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `canon_tijuana`
--

DROP TABLE IF EXISTS `canon_tijuana`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `canon_tijuana` (
  `id_canon` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `latitud` decimal(10,7) DEFAULT NULL,
  `longitud` decimal(10,7) DEFAULT NULL,
  `nivel_prioridad` enum('Alta','Media','Baja') COLLATE utf8mb4_unicode_ci DEFAULT 'Media',
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id_canon`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `canon_tijuana`
--

LOCK TABLES `canon_tijuana` WRITE;
/*!40000 ALTER TABLE `canon_tijuana` DISABLE KEYS */;
INSERT INTO `canon_tijuana` VALUES (1,'Cañón Los Laureles',32.4659000,-117.0317000,'Alta','Flujo directo hacia Río Tijuana y frontera'),(2,'Cañón El Florido',32.4892000,-116.9134000,'Alta','Alta densidad poblacional en zonas aledañas'),(3,'Cañón La Morita',32.5123000,-116.9876000,'Alta','Asentamientos irregulares con alto flujo de residuos'),(4,'Cañón El Refugio',32.4431000,-116.9654000,'Media','Flujo intermitente en temporada de lluvias'),(5,'Cañón Matamoros',32.5234000,-117.0123000,'Media','Zona industrial con residuos mixtos');
/*!40000 ALTER TABLE `canon_tijuana` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-25 11:05:35
