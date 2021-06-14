# 首先创建一个数据库名字为cov即可
-- create database cov;

# 通过use cov 变更成cov数据库 然后在其中创建history表(字段信息如下所示)
CREATE TABLE `history` (
  `ds` datetime NOT NULL COMMENT '日期',
  `confirm` int(11) DEFAULT NULL COMMENT '累计确诊',
  `confirm_add` int(11) DEFAULT NULL COMMENT '当日新增确诊',
  `suspect` int(11) DEFAULT NULL COMMENT '剩余疑似',
  `suspect_add` int(11) DEFAULT NULL COMMENT '当日新增疑似',
  `heal` int(11) DEFAULT NULL COMMENT '累计治愈',
  `heal_add` int(11) DEFAULT NULL COMMENT '当日新增治愈',
  `dead` int(11) DEFAULT NULL COMMENT '累计死亡',
  `dead_add` int(11) DEFAULT NULL COMMENT '当日新增死亡',
  PRIMARY KEY (`ds`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


# 创建details表(字段信息如下所示)
CREATE TABLE `details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `update_time` datetime DEFAULT NULL COMMENT '数据最后更新时间',
  `province` varchar(50) DEFAULT NULL COMMENT '省',
  `city` varchar(50) DEFAULT NULL COMMENT '市',
  `confirm` int(11) DEFAULT NULL COMMENT '累计确诊',
  `confirm_add` int(11) DEFAULT NULL COMMENT '新增治愈',
  `heal` int(11) DEFAULT NULL COMMENT '累计治愈',
  `dead` int(11) DEFAULT NULL COMMENT '累计死亡',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


# 创建hotsearch表(字段信息如下所示)
CREATE TABLE `hotsearch` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `content` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

