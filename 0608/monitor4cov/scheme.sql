
# dg user表
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`(
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `nickname` VARCHAR(128) NOT NULL UNIQUE,
	  `tel` VARCHAR(128),
    `email` VARCHAR(128),
	  `created_at` DATETIME,
    `password` VARCHAR (128),
    KEY (`nickname`)
)DEFAULT CHARSET = UTF8;


DROP TABLE IF EXISTS `ncase`;
CREATE TABLE `ncase`(
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `province` VARCHAR(128),
    `year` VARCHAR(128),
    `date` VARCHAR(128),
	`confirm` int DEFAULT 0,
    `dead` int DEFAULT 0,
    `heal` int DEFAULT 0,
    `newconfirm` int DEFAULT 0,
    `newheal` int DEFAULT 0,
    `newdead` int DEFAULT 0,
    `desp` VARCHAR(128)
)DEFAULT CHARSET = UTF8;