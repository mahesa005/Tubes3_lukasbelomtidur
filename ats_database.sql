/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.7.2-MariaDB, for osx10.20 (arm64)
--
-- Host: localhost    Database: ats_database
-- ------------------------------------------------------
-- Server version	11.7.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `ApplicantProfile`
--

DROP TABLE IF EXISTS `ApplicantProfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ApplicantProfile` (
  `applicant_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`applicant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ApplicantProfile`
--

LOCK TABLES `ApplicantProfile` WRITE;
/*!40000 ALTER TABLE `ApplicantProfile` DISABLE KEYS */;
INSERT INTO `ApplicantProfile` (`applicant_id`, `first_name`, `last_name`, `date_of_birth`, `address`, `phone_number`) VALUES (1,'Nicholas','Freeman','1991-09-27','1520 Lauren Station Suite 331, Susanburgh, CO 29754','081262097177'),
(2,'Shannon','Lee','2002-11-07','Unit 0525 Box 7291, DPO AE 96147','081224114397'),
(3,'Deanna','Riggs','1991-01-07','3527 Hayes Underpass, Chavezmouth, CA 88936','081272928270'),
(4,'Joshua','Harris','1989-08-24','39701 Robbins Mount, East Lisa, VT 50313','081234487315'),
(5,'Margaret','Caldwell','1975-07-26','2591 Jones Mews Suite 835, Davidton, CT 48954','081260130463'),
(6,'Joseph','Gibbs','1974-10-21','213 Smith Garden Apt. 006, Blackchester, AZ 82260','081279434115'),
(7,'Ricardo','Morales','1970-02-05','16440 Bruce Stream Suite 995, Reedtown, OR 87433','081298401554'),
(8,'Jonathan','Patel','1982-11-18','726 Kimberly Union Suite 400, Timothybury, MP 12746','081227013982'),
(9,'Lisa','Morgan','2001-10-28','754 Thomas Club Suite 825, East Josephborough, GU 99362','081213295145'),
(10,'Brittany','Daniels','1968-01-22','78870 Nicholas Ways Suite 131, Port Nicholas, ME 71611','081284076623'),
(11,'Mike','Sanchez','1984-10-02','Unit 5903 Box 9384, DPO AA 56468','081218285555'),
(12,'Todd','Arnold','1987-02-07','907 Erica Parkways, Markland, TX 46621','081253084271'),
(13,'Caitlin','Conway','1968-10-25','89552 Wilson Common Apt. 935, New Amymouth, MO 51271','081226570950'),
(14,'Brandon','Smith','1971-09-07','23140 Johnson Route, Lake Jessica, NJ 67652','081223448142'),
(15,'Tara','Castaneda','1980-09-04','774 Jacqueline Greens Suite 598, South Victor, GA 82960','081253098745'),
(16,'Amanda','Howard','1996-08-28','36561 Joyce Port, Cherylburgh, VI 88907','081252500106'),
(17,'John','Collins','1969-12-11','8674 Clark Fall, Ashleyhaven, VT 84730','081272779366'),
(18,'Tammy','Jensen','1966-09-28','2565 Stokes Groves Apt. 667, Port Jamestown, MI 68948','081211763383'),
(19,'Hunter','Martin','1988-06-26','08538 Brown Vista Suite 683, Sarahfort, KY 24502','081244277275'),
(20,'Clifford','Barber','1990-03-26','0610 Kristin Garden Apt. 521, Johnsonport, WY 01312','081215566646');
/*!40000 ALTER TABLE `ApplicantProfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ApplicationDetail`
--

DROP TABLE IF EXISTS `ApplicationDetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ApplicationDetail` (
  `detail_id` int(11) NOT NULL AUTO_INCREMENT,
  `applicant_id` int(11) NOT NULL,
  `application_role` varchar(100) DEFAULT NULL,
  `cv_path` text NOT NULL,
  PRIMARY KEY (`detail_id`),
  KEY `applicant_id` (`applicant_id`),
  CONSTRAINT `applicationdetail_ibfk_1` FOREIGN KEY (`applicant_id`) REFERENCES `ApplicantProfile` (`applicant_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ApplicationDetail`
--

LOCK TABLES `ApplicationDetail` WRITE;
/*!40000 ALTER TABLE `ApplicationDetail` DISABLE KEYS */;
INSERT INTO `ApplicationDetail` (`detail_id`, `applicant_id`, `application_role`, `cv_path`) VALUES (1,1,'FITNESS','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/FITNESS/97123005.pdf'),
(2,2,'BPO','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/BPO/13964744.pdf'),
(3,3,'ARTS','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/ARTS/20148147.pdf'),
(4,4,'ACCOUNTANT','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/ACCOUNTANT/17556527.pdf'),
(5,5,'BUSINESS-DEVELOPMENT','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/BUSINESS-DEVELOPMENT/31638814.pdf'),
(6,6,'SALES','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/SALES/37540732.pdf'),
(7,7,'ACCOUNTANT','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/ACCOUNTANT/24703009.pdf'),
(8,8,'INFORMATION-TECHNOLOGY','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/INFORMATION-TECHNOLOGY/39413067.pdf'),
(9,9,'CONSTRUCTION','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/CONSTRUCTION/78298706.pdf'),
(10,10,'FITNESS','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/FITNESS/24767027.pdf'),
(11,11,'DIGITAL-MEDIA','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/DIGITAL-MEDIA/11270462.pdf'),
(12,12,'DIGITAL-MEDIA','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/DIGITAL-MEDIA/16509761.pdf'),
(13,13,'CONSULTANT','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/CONSULTANT/88907739.pdf'),
(14,14,'BANKING','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/BANKING/11637468.pdf'),
(15,15,'SALES','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/SALES/20423658.pdf'),
(16,16,'DESIGNER','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/DESIGNER/13014900.pdf'),
(17,17,'ENGINEERING','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/ENGINEERING/21847415.pdf'),
(18,18,'ADVOCATE','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/ADVOCATE/74126637.pdf'),
(19,19,'PUBLIC-RELATIONS','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/PUBLIC-RELATIONS/24491862.pdf'),
(20,20,'BANKING','/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/BANKING/17213671.pdf');
/*!40000 ALTER TABLE `ApplicationDetail` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-06-07 18:38:44
