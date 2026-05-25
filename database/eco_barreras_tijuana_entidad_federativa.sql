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
-- Table structure for table `entidad_federativa`
--

DROP TABLE IF EXISTS `entidad_federativa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entidad_federativa` (
  `id_entidad` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `clave_inegi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_entidad`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entidad_federativa`
--

LOCK TABLES `entidad_federativa` WRITE;
/*!40000 ALTER TABLE `entidad_federativa` DISABLE KEYS */;
INSERT INTO `entidad_federativa` VALUES (1,'Baja California','02'),(2,'Baja California Sur','03'),(3,'Sonora','26'),(4,'Sinaloa','25'),(5,'Chihuahua','08'),(6,'Aguascalientes','01'),(9,'Campeche','04'),(10,'Coahuila','05'),(11,'Colima','06'),(12,'Chiapas','07'),(14,'Ciudad de México','09'),(15,'Durango','10'),(16,'Guanajuato','11'),(17,'Guerrero','12'),(18,'Hidalgo','13'),(19,'Jalisco','14'),(20,'México','15'),(21,'Michoacán','16'),(22,'Morelos','17'),(23,'Nayarit','18'),(24,'Nuevo León','19'),(25,'Oaxaca','20'),(26,'Puebla','21'),(27,'Querétaro','22'),(28,'Quintana Roo','23'),(29,'San Luis Potosí','24'),(32,'Tabasco','27'),(33,'Tamaulipas','28'),(34,'Tlaxcala','29'),(35,'Veracruz','30'),(36,'Yucatán','31'),(37,'Zacatecas','32');
/*!40000 ALTER TABLE `entidad_federativa` ENABLE KEYS */;
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
