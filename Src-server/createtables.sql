CREATE TABLE `StatutoryLevel` (
  `country_code` varchar(10) NOT NULL,
  `level_id` varchar(10) NOT NULL AUTO_INCREMENT,
  `level` int(11) NOT NULL,
  `title` varchar(25) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;

CREATE TABLE `StatutoryMaster` (
  `country_code` varchar(10) NOT NULL,
  `id` varchar(10) NOT NULL,
  `value` varchar(50) NOT NULL,
  `parent_id` varchar(10) NOT NULL,
  `status` varchar(1)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
