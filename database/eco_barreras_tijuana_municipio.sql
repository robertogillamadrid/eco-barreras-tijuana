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
-- Table structure for table `municipio`
--

DROP TABLE IF EXISTS `municipio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `municipio` (
  `id_municipio` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_entidad` int NOT NULL,
  PRIMARY KEY (`id_municipio`),
  KEY `id_entidad` (`id_entidad`),
  CONSTRAINT `municipio_ibfk_1` FOREIGN KEY (`id_entidad`) REFERENCES `entidad_federativa` (`id_entidad`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `municipio`
--

LOCK TABLES `municipio` WRITE;
/*!40000 ALTER TABLE `municipio` DISABLE KEYS */;
INSERT INTO `municipio` VALUES (1,'Tijuana',1),(2,'Mexicali',1),(3,'Ensenada',1),(4,'Tecate',1),(5,'Rosarito',1),(6,'San Quintín',1),(7,'Los datos la fuente los reporta en toneladas anuales, en tanto que en este cuadro se reportan en miles de toneladas anuales, esto, aunado a los redond',14),(8,'Aguascalientes',6),(9,'Baja California',1),(10,'Baja California Sur',1),(11,'Campeche',9),(12,'Coahuila',10),(13,'Colima',11),(14,'Chiapas',12),(15,'Chihuahua',5),(16,'Ciudad de México',14),(17,'Durango',15),(18,'Guanajuato',16),(19,'Guerrero',17),(20,'Hidalgo',18),(21,'Jalisco',19),(22,'México',20),(23,'Michoacán',21),(24,'Morelos',22),(25,'Nayarit',23),(26,'Nuevo León',24),(27,'Oaxaca',25),(28,'Puebla',26),(29,'Querétaro',27),(30,'Quintana Roo',28),(31,'San Luis Potosí',29),(32,'Sinaloa',4),(33,'Sonora',3),(34,'Tabasco',32),(35,'Tamaulipas',33),(36,'Tlaxcala',34),(37,'Veracruz',35),(38,'Yucatán',36),(39,'Zacatecas',37),(40,'Los datos proceden del Censo Nacional de Gobiernos Municipales y Delegacionales (Módulo de Residuos Sólidos Urbanos), actualmente conocido como Censo ',12),(41,'Los datos proceden del Censo Nacional de Gobiernos Municipales y Delegacionales (Módulo de Residuos Sólidos Urbanos), actualmente conocido como Censo ',12),(42,'Instituto Nacional de Estadística y Geografía, Censo Nacional de Gobiernos Municipales y Demarcaciones Territoriales de la Ciudad de México, consultad',14),(43,'Los datos la fuente los reporta en toneladas anuales, en tanto que en este cuadro se reportan en miles de toneladas anuales, esto, aunado a los redond',14),(44,'Aguascalientes',6),(45,'Baja California',1),(46,'Baja California Sur',1),(47,'Campeche',9),(48,'Coahuila',10),(49,'Colima',11),(50,'Chiapas',12),(51,'Chihuahua',5),(52,'Ciudad de México',14),(53,'Durango',15),(54,'Guanajuato',16),(55,'Guerrero',17),(56,'Hidalgo',18),(57,'Jalisco',19),(58,'México',20),(59,'Michoacán',21),(60,'Morelos',22),(61,'Nayarit',23),(62,'Nuevo León',24),(63,'Oaxaca',25),(64,'Puebla',26),(65,'Querétaro',27),(66,'Quintana Roo',28),(67,'San Luis Potosí',29),(68,'Sinaloa',4),(69,'Sonora',3),(70,'Tabasco',32),(71,'Tamaulipas',33),(72,'Tlaxcala',34),(73,'Veracruz',35),(74,'Yucatán',36),(75,'Zacatecas',37),(76,'Los datos proceden del Censo Nacional de Gobiernos Municipales y Delegacionales (Módulo de Residuos Sólidos Urbanos), actualmente conocido como Censo ',12),(77,'Los datos proceden del Censo Nacional de Gobiernos Municipales y Delegacionales (Módulo de Residuos Sólidos Urbanos), actualmente conocido como Censo ',12),(78,'Instituto Nacional de Estadística y Geografía, Censo Nacional de Gobiernos Municipales y Demarcaciones Territoriales de la Ciudad de México, consultad',14);
/*!40000 ALTER TABLE `municipio` ENABLE KEYS */;
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
