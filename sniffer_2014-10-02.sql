# ************************************************************
# Sequel Pro SQL dump
# Version 4135
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 192.168.56.101 (MySQL 5.6.19-1~dotdeb.1)
# Database: sniffer
# Generation Time: 2014-10-02 08:27:39 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table packets
# ------------------------------------------------------------

DROP TABLE IF EXISTS `packets`;

CREATE TABLE `packets` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `dest_mac` varchar(255) DEFAULT NULL,
  `src_mac` varchar(255) DEFAULT NULL,
  `interface_protocol` int(11) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `ip_hdr_lngt` int(11) DEFAULT NULL,
  `ttl` int(11) DEFAULT NULL,
  `ip_protocol` int(11) DEFAULT NULL,
  `src_adress` varchar(255) DEFAULT NULL,
  `dest_adress` varchar(255) DEFAULT NULL,
  `src_port` int(11) DEFAULT NULL,
  `dest_port` int(11) DEFAULT NULL,
  `seq_num` int(64) DEFAULT NULL,
  `acknowledgement` int(64) DEFAULT NULL,
  `tcp_header_lngt` int(11) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
