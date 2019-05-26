SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `stocksvision`
--

-- --------------------------------------------------------

--
-- Table structure for table `stocks`
--

CREATE TABLE IF NOT EXISTS `stocks` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `domain_name` varchar(50) NOT NULL,
  `website_title` varchar(50) NOT NULL DEFAULT '',
  `article_title` varchar(50) NOT NULL DEFAULT '',
  `author` varchar(50) NOT NULL DEFAULT '',
  `date_published` varchar(50) NOT NULL DEFAULT '',
  `flagged` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=306 ;

--
-- Table structure for table `indicators`
--

CREATE TABLE IF NOT EXISTS `indicators` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url_id` int(11) NULL DEFAULT NULL,
  `date_cited` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `platform_id` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=488 ;

--
-- User for phpMyAdmin login
--

CREATE USER phpmyadmin IDENTIFIED WITH mysql_native_password BY 'pass';
GRANT ALL PRIVILEGES ON stocksvision.* TO 'phpmyadmin'@'%' WITH GRANT OPTION;

--
-- User for script login
--

CREATE USER imthescript IDENTIFIED WITH mysql_native_password BY 'pass';
GRANT ALL PRIVILEGES ON stocksvision.* TO 'imthescript'@'%' WITH GRANT OPTION;

