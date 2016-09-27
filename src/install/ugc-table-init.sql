-- MySQL dump 10.11
--
-- Host: localhost    Database: ugc
-- ------------------------------------------------------
-- Server version	5.0.95
-- CREATE DATABASE `ugc` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ugc_audit_log`
--

DROP TABLE IF EXISTS `ugc_audit_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ugc_audit_log` (
  `id` int(11) NOT NULL auto_increment,
  `tid` varchar(128) NOT NULL,
  `funshion_id` varchar(64) NOT NULL,
  `uid` int(11) NOT NULL,
  `flag` int(11) NOT NULL,
  `time` datetime default NULL,
  `del_flag` int(11) default NULL,
  PRIMARY KEY  (`id`),
  KEY `ix_uid_audit_log` (`tid`,`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ugc_audit_workspace`
--

DROP TABLE IF EXISTS `ugc_audit_workspace`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ugc_audit_workspace` (
  `tid` varchar(128) NOT NULL,
  `uid` int(11) NOT NULL,
  `time` datetime NOT NULL,
  PRIMARY KEY (`tid`,`uid`),
  KEY `ix_uid_audit_workspace` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ugc_dat`
--

DROP TABLE IF EXISTS `ugc_dat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ugc_dat` (
  `dat_id` varchar(64) NOT NULL,
  `dat_size` bigint(20) NOT NULL,
  `mserver_ip` varchar(16) NOT NULL,
  `mserver_port` varchar(32) NOT NULL,
  `distribution_time` datetime NOT NULL,
  `flag` int(11) default NULL,
  `del_flag` int(11) default NULL,
  `sendmacros_time` datetime default NULL,
  PRIMARY KEY  (`dat_id`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ugc_fid_map`
--

DROP TABLE IF EXISTS `ugc_fid_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ugc_fid_map` (
  `id` int(11) NOT NULL auto_increment,
  `funshion_id` varchar(64) NOT NULL,
  `dat_id` varchar(64) NOT NULL,
  `tid` varchar(128) NOT NULL,
  `flag` int(11) DEFAULT NULL,
  `ctime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `index_map_datid` (`dat_id`) USING BTREE,
  KEY `index_map_tid` (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ugc_file`
--

DROP TABLE IF EXISTS `ugc_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ugc_file` (
  `funshion_id` varchar(64) NOT NULL,
  `tid` varchar(128) NOT NULL,
  `rate` varchar(64) NOT NULL,
  `file_size` bigint(20) NOT NULL,
  `filename` varchar(256) NOT NULL,
  `duration` bigint(20) NOT NULL,
  `video_url` varchar(1024) NOT NULL,
  `small_image` longtext NOT NULL,
  `large_image` longtext NOT NULL,
  `logo` varchar(1024) default NULL,
  `ctime` datetime NOT NULL,
  `definition` varchar(32) default NULL,
  PRIMARY KEY  (`funshion_id`,`tid`),
  KEY `index_tid` (`tid`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ugc_video`
--

DROP TABLE IF EXISTS `ugc_video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ugc_video` (
  `tid` varchar(128) character set gbk NOT NULL,
  `site` varchar(128) character set gbk NOT NULL,
  `title` varchar(256) character set gbk default NULL,
  `tags` varchar(512) character set gbk NOT NULL,
  `origin` varchar(32) character set gbk NOT NULL,
  `channel` varchar(512) character set gbk NOT NULL,
  `description` longtext character set gbk,
  `priority` int(11) NOT NULL,
  `task_id` varchar(32) DEFAULT NULL,
  `step` varchar(64) CHARACTER SET gbk NOT NULL,
  `status` int(11) NOT NULL,
  `ip` varchar(64) character set gbk default NULL,
  `port` varchar(32) character set gbk default NULL,
  `vid` varchar(256) character set gbk default NULL,
  `video_id` varchar(128) character set gbk default NULL,
  `seconds` int(11) default NULL,
  `refer` varchar(1024) character set gbk default NULL,
  `ttype` int(11) default NULL,
  `uid` int(11) NOT NULL,
  `audit_uid` int(11) default NULL,
  `ctime` datetime default NULL,
  `mtime` datetime default NULL,
  `pub_time` datetime default NULL,
  `audit_free` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY  (`tid`),
  KEY `ix_site_video` (`site`,`uid`),
  KEY `uid` (`uid`),
  KEY `task_id` (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `v_get_audit_detail_task`
--

DROP TABLE IF EXISTS `v_get_audit_detail_task`;
/*!50001 DROP VIEW IF EXISTS `v_get_audit_detail_task`*/;
/*!50001 CREATE TABLE `v_get_audit_detail_task` (
  `tid` varchar(128),
  `uid` int(11),
  `title` varchar(256),
  `tags` varchar(512),
  `channel` varchar(512),
  `funshion_id` varchar(64),
  `filename` varchar(256),
  `file_size` bigint(20),
  `video_url` varchar(1024),
  `small_image` longtext,
  `large_image` longtext,
  `logo` varchar(1024),
  `rate` varchar(64),
  `duration` bigint(20),
  `step` varchar(64),
  `status` int(11),
  `priority` int(11),
  `time` datetime,
  `username` varchar(30),
  `vid` varchar(256),
  `description` longtext
) ENGINE=InnoDB */;

--
-- Temporary table structure for view `v_get_cloud_tasklist`
--

DROP TABLE IF EXISTS `v_get_cloud_tasklist`;
/*!50001 DROP VIEW IF EXISTS `v_get_cloud_tasklist`*/;
/*!50001 CREATE TABLE `v_get_cloud_tasklist` (
  `tid` varchar(128),
  `site` varchar(128),
  `vid` varchar(256),
  `priority` int(11)
) ENGINE=InnoDB */;

--
-- Temporary table structure for view `v_get_fail_tasklist`
--

DROP TABLE IF EXISTS `v_get_fail_tasklist`;
/*!50001 DROP VIEW IF EXISTS `v_get_fail_tasklist`*/;
/*!50001 CREATE TABLE `v_get_fail_tasklist` (
  `tid` varchar(128),
  `uid` int(11),
  `title` varchar(256),
  `tags` varchar(512),
  `channel` varchar(512),
  `step` varchar(64),
  `status` int(11),
  `funshion_id` varchar(64),
  `priority` int(11),
  `time` datetime,
  `video_url` varchar(1024),
  `small_image` longtext,
  `large_image` longtext,
  `duration` bigint(20),
  `username` varchar(30),
  `vid` varchar(256),
  `rate` varchar(64)
) ENGINE=InnoDB */;

--
-- Temporary table structure for view `v_get_forwards_space_info`
--

DROP TABLE IF EXISTS `v_get_forwards_space_info`;
/*!50001 DROP VIEW IF EXISTS `v_get_forwards_space_info`*/;
/*!50001 CREATE TABLE `v_get_forwards_space_info` (
  `tid` varchar(128),
  `uid` int(11),
  `title` varchar(256),
  `tags` varchar(512),
  `description` longtext,
  `priority` int(11),
  `channel` varchar(512),
  `step` varchar(64),
  `status` int(11),
  `mserver_ip` varchar(16),
  `funshion_id` varchar(64),
  `dat_id` varchar(64),
  `time` datetime
) ENGINE=InnoDB */;

--
-- Temporary table structure for view `v_get_notify_macros_list`
--

DROP TABLE IF EXISTS `v_get_notify_macros_list`;
/*!50001 DROP VIEW IF EXISTS `v_get_notify_macros_list`*/;
/*!50001 CREATE TABLE `v_get_notify_macros_list` (
  `tid` varchar(128),
  `dat_id` varchar(64),
  `dat_size` bigint(20),
  `mserver_ip` varchar(16),
  `mserver_port` varchar(32),
  `title` varchar(256),
  `site` varchar(128),
  `tags` varchar(512),
  `channel` varchar(512),
  `description` longtext,
  `step` varchar(64),
  `status` int(11),
  `funshion_id` varchar(64),
  `rate` varchar(64),
  `file_size` bigint(20),
  `filename` varchar(256),
  `video_url` varchar(1024),
  `small_image` longtext,
  `duration` bigint(20),
  `flag` int(11),
  `time` datetime,
  `logo` varchar(1024)
) ENGINE=InnoDB */;

--
-- Temporary table structure for view `v_get_notify_macros_list_v2`
--

DROP TABLE IF EXISTS `v_get_notify_macros_list_v2`;
/*!50001 DROP VIEW IF EXISTS `v_get_notify_macros_list_v2`*/;
/*!50001 CREATE TABLE `v_get_notify_macros_list_v2` (
  `tid` varchar(128),
  `dat_id` varchar(64),
  `dat_size` bigint(20),
  `mserver_ip` varchar(16),
  `mserver_port` varchar(32),
  `title` varchar(256),
  `site` varchar(128),
  `tags` varchar(512),
  `channel` varchar(512),
  `description` longtext,
  `step` varchar(64),
  `status` int(11),
  `funshion_id` varchar(64),
  `rate` varchar(64),
  `file_size` bigint(20),
  `filename` varchar(256),
  `video_url` varchar(1024),
  `small_image` longtext,
  `duration` bigint(20),
  `flag` int(11),
  `time` datetime,
  `logo` varchar(1024),
  `username` varchar(30)
) ENGINE=InnoDB */;

--
-- Temporary table structure for view `v_get_pass_tasklist`
--

DROP TABLE IF EXISTS `v_get_pass_tasklist`;
/*!50001 DROP VIEW IF EXISTS `v_get_pass_tasklist`*/;
/*!50001 CREATE TABLE `v_get_pass_tasklist` (
  `tid` varchar(128),
  `uid` int(11),
  `title` varchar(256),
  `tags` varchar(512),
  `channel` varchar(512),
  `step` varchar(64),
  `status` int(11),
  `funshion_id` varchar(64),
  `priority` int(11),
  `time` datetime,
  `video_url` varchar(1024),
  `small_image` longtext,
  `large_image` longtext,
  `duration` bigint(20),
  `username` varchar(30),
  `vid` varchar(256),
  `rate` varchar(64)
) ENGINE=InnoDB */;

--
-- Temporary table structure for view `v_get_pending_tasklist`
--

DROP TABLE IF EXISTS `v_get_pending_tasklist`;
/*!50001 DROP VIEW IF EXISTS `v_get_pending_tasklist`*/;
/*!50001 CREATE TABLE `v_get_pending_tasklist` (
  `tid` varchar(128),
  `uid` int(11),
  `title` varchar(256),
  `tags` varchar(512),
  `channel` varchar(512),
  `step` varchar(64),
  `status` int(11),
  `funshion_id` varchar(64),
  `priority` int(11),
  `time` datetime,
  `video_url` varchar(1024),
  `small_image` longtext,
  `large_image` longtext,
  `duration` bigint(20),
  `username` varchar(30),
  `vid` varchar(256),
  `rate` varchar(64)
) ENGINE=InnoDB */;

--
-- Temporary table structure for view `v_get_user_audit_info`
--

DROP TABLE IF EXISTS `v_get_user_audit_info`;
/*!50001 DROP VIEW IF EXISTS `v_get_user_audit_info`*/;
/*!50001 CREATE TABLE `v_get_user_audit_info` (
  `tid` varchar(128),
  `uid` int(11),
  `username` varchar(30),
  `flag` int(11),
  `time` datetime
) ENGINE=InnoDB */;

--
-- Temporary table structure for view `v_get_user_audit_info_v2`
--

DROP TABLE IF EXISTS `v_get_user_audit_info_v2`;
/*!50001 DROP VIEW IF EXISTS `v_get_user_audit_info_v2`*/;
/*!50001 CREATE TABLE `v_get_user_audit_info_v2` (
  `tid` varchar(128),
  `uid` int(11),
  `username` varchar(30),
  `flag` int(11),
  `time` datetime
) ENGINE=InnoDB */;

--
-- Temporary table structure for view `v_get_verify_examresult`
--

DROP TABLE IF EXISTS `v_get_verify_examresult`;
/*!50001 DROP VIEW IF EXISTS `v_get_verify_examresult`*/;
/*!50001 CREATE TABLE `v_get_verify_examresult` (
  `tid` varchar(128),
  `uid` int(11),
  `ip` varchar(64),
  `port` varchar(32),
  `funshion_id` varchar(64),
  `flag` int(11),
  `site` varchar(128),
  `ttype` int(11)
) ENGINE=InnoDB */;

--
-- Temporary table structure for view `v_video_base`
--

DROP TABLE IF EXISTS `v_video_base`;
/*!50001 DROP VIEW IF EXISTS `v_video_base`*/;
/*!50001 CREATE TABLE `v_video_base` (
  `uid` int(11),
  `username` varchar(30),
  `tid` varchar(128),
  `site` varchar(128),
  `title` varchar(256),
  `tags` varchar(512),
  `origin` varchar(32),
  `channel` varchar(512),
  `description` longtext,
  `priority` int(11),
  `step` varchar(64),
  `status` int(11),
  `video_id` varchar(128),
  `seconds` int(11),
  `ttype` int(11)
) ENGINE=InnoDB */;

--
-- Final view structure for view `v_get_audit_detail_task`
--

/*!50001 DROP TABLE `v_get_audit_detail_task`*/;
/*!50001 DROP VIEW IF EXISTS `v_get_audit_detail_task`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`ugc_kaifa`@`%` SQL SECURITY INVOKER */
/*!50001 VIEW `v_get_audit_detail_task` AS select `ugc_video`.`tid` AS `tid`,`ugc_video`.`uid` AS `uid`,`ugc_video`.`title` AS `title`,`ugc_video`.`tags` AS `tags`,`ugc_video`.`channel` AS `channel`,`ugc_file`.`funshion_id` AS `funshion_id`,`ugc_file`.`filename` AS `filename`,`ugc_file`.`file_size` AS `file_size`,`ugc_file`.`video_url` AS `video_url`,`ugc_file`.`small_image` AS `small_image`,`ugc_file`.`large_image` AS `large_image`,`ugc_file`.`logo` AS `logo`,`ugc_file`.`rate` AS `rate`,`ugc_file`.`duration` AS `duration`,`ugc_video`.`step` AS `step`,`ugc_video`.`status` AS `status`,`ugc_video`.`priority` AS `priority`,`ugc_video`.`mtime` AS `time`,`auth_user`.`username` AS `username`,`ugc_video`.`vid` AS `vid`,`ugc_video`.`description` AS `description` from ((`ugc_video` join `ugc_file`) join `auth_user`) where ((`ugc_video`.`site` <> _gbk'qy') and (`ugc_video`.`tid` = `ugc_file`.`tid`) and (`auth_user`.`id` = `ugc_video`.`uid`)) */;

--
-- Final view structure for view `v_get_cloud_tasklist`
--

/*!50001 DROP TABLE `v_get_cloud_tasklist`*/;
/*!50001 DROP VIEW IF EXISTS `v_get_cloud_tasklist`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`ugc_kaifa`@`%` SQL SECURITY INVOKER */
/*!50001 VIEW `v_get_cloud_tasklist` AS select `ugc_video`.`tid` AS `tid`,`ugc_video`.`site` AS `site`,`ugc_video`.`vid` AS `vid`,`ugc_video`.`priority` AS `priority` from (`ugc_video` join `auth_user`) where (`ugc_video`.`uid` = `auth_user`.`id`) */;

--
-- Final view structure for view `v_get_fail_tasklist`
--

/*!50001 DROP TABLE `v_get_fail_tasklist`*/;
/*!50001 DROP VIEW IF EXISTS `v_get_fail_tasklist`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`ugc_kaifa`@`%` SQL SECURITY INVOKER */
/*!50001 VIEW `v_get_fail_tasklist` AS select `ugc_audit_log`.`tid` AS `tid`,`ugc_audit_log`.`uid` AS `uid`,`ugc_video`.`title` AS `title`,`ugc_video`.`tags` AS `tags`,`ugc_video`.`channel` AS `channel`,`ugc_video`.`step` AS `step`,`ugc_video`.`status` AS `status`,`ugc_file`.`funshion_id` AS `funshion_id`,`ugc_video`.`priority` AS `priority`,`ugc_audit_log`.`time` AS `time`,`ugc_file`.`video_url` AS `video_url`,`ugc_file`.`small_image` AS `small_image`,`ugc_file`.`large_image` AS `large_image`,`ugc_file`.`duration` AS `duration`,`auth_user`.`username` AS `username`,`ugc_video`.`vid` AS `vid`,`ugc_file`.`rate` AS `rate` from (((`ugc_audit_log` join `ugc_video`) join `ugc_file`) join `auth_user`) where ((`ugc_audit_log`.`tid` = `ugc_video`.`tid`) and (`ugc_audit_log`.`tid` = `ugc_file`.`tid`) and (`ugc_audit_log`.`flag` = 0) and (`ugc_video`.`site` <> _gbk'qy') and (`ugc_audit_log`.`uid` = `auth_user`.`id`)) */;

--
-- Final view structure for view `v_get_forwards_space_info`
--

/*!50001 DROP TABLE `v_get_forwards_space_info`*/;
/*!50001 DROP VIEW IF EXISTS `v_get_forwards_space_info`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`ugc_kaifa`@`%` SQL SECURITY INVOKER */
/*!50001 VIEW `v_get_forwards_space_info` AS select `ugc_video`.`tid` AS `tid`,`ugc_video`.`uid` AS `uid`,`ugc_video`.`title` AS `title`,`ugc_video`.`tags` AS `tags`,`ugc_video`.`description` AS `description`,`ugc_video`.`priority` AS `priority`,`ugc_video`.`channel` AS `channel`,`ugc_video`.`step` AS `step`,`ugc_video`.`status` AS `status`,`ugc_dat`.`mserver_ip` AS `mserver_ip`,`ugc_fid_map`.`funshion_id` AS `funshion_id`,`ugc_fid_map`.`dat_id` AS `dat_id`,`ugc_video`.`ctime` AS `time` from ((`ugc_video` left join `ugc_fid_map` on((`ugc_video`.`tid` = `ugc_fid_map`.`tid`))) left join `ugc_dat` on((`ugc_dat`.`dat_id` = `ugc_fid_map`.`dat_id`))) */;

--
-- Final view structure for view `v_get_notify_macros_list`
--

/*!50001 DROP TABLE `v_get_notify_macros_list`*/;
/*!50001 DROP VIEW IF EXISTS `v_get_notify_macros_list`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`ugc_kaifa`@`%` SQL SECURITY INVOKER */
/*!50001 VIEW `v_get_notify_macros_list` AS select `ugc_video`.`tid` AS `tid`,`ugc_dat`.`dat_id` AS `dat_id`,`ugc_dat`.`dat_size` AS `dat_size`,`ugc_dat`.`mserver_ip` AS `mserver_ip`,`ugc_dat`.`mserver_port` AS `mserver_port`,`ugc_video`.`title` AS `title`,`ugc_video`.`site` AS `site`,`ugc_video`.`tags` AS `tags`,`ugc_video`.`channel` AS `channel`,`ugc_video`.`description` AS `description`,`ugc_video`.`step` AS `step`,`ugc_video`.`status` AS `status`,`ugc_file`.`funshion_id` AS `funshion_id`,`ugc_file`.`rate` AS `rate`,`ugc_file`.`file_size` AS `file_size`,`ugc_file`.`filename` AS `filename`,`ugc_file`.`video_url` AS `video_url`,`ugc_file`.`small_image` AS `small_image`,`ugc_file`.`duration` AS `duration`,`ugc_dat`.`flag` AS `flag`,`ugc_dat`.`distribution_time` AS `time`,`ugc_file`.`logo` AS `logo` from (((`ugc_video` join `ugc_file`) join `ugc_dat`) join `ugc_fid_map`) where ((`ugc_file`.`tid` = `ugc_video`.`tid`) and (`ugc_fid_map`.`tid` = `ugc_file`.`tid`) and (`ugc_dat`.`dat_id` = `ugc_fid_map`.`dat_id`)) */;

--
-- Final view structure for view `v_get_notify_macros_list_v2`
--

/*!50001 DROP TABLE `v_get_notify_macros_list_v2`*/;
/*!50001 DROP VIEW IF EXISTS `v_get_notify_macros_list_v2`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`ugc_kaifa`@`%` SQL SECURITY INVOKER */
/*!50001 VIEW `v_get_notify_macros_list_v2` AS select `ugc_video`.`tid` AS `tid`,`ugc_dat`.`dat_id` AS `dat_id`,`ugc_dat`.`dat_size` AS `dat_size`,`ugc_dat`.`mserver_ip` AS `mserver_ip`,`ugc_dat`.`mserver_port` AS `mserver_port`,`ugc_video`.`title` AS `title`,`ugc_video`.`site` AS `site`,`ugc_video`.`tags` AS `tags`,`ugc_video`.`channel` AS `channel`,`ugc_video`.`description` AS `description`,`ugc_video`.`step` AS `step`,`ugc_video`.`status` AS `status`,`ugc_file`.`funshion_id` AS `funshion_id`,`ugc_file`.`rate` AS `rate`,`ugc_file`.`file_size` AS `file_size`,`ugc_file`.`filename` AS `filename`,`ugc_file`.`video_url` AS `video_url`,`ugc_file`.`small_image` AS `small_image`,`ugc_file`.`duration` AS `duration`,`ugc_dat`.`flag` AS `flag`,`ugc_dat`.`distribution_time` AS `time`,`ugc_file`.`logo` AS `logo`,`auth_user`.`username` AS `username` from ((((`ugc_video` join `ugc_file`) join `ugc_dat`) join `ugc_fid_map`) join `auth_user`) where ((`ugc_file`.`tid` = `ugc_video`.`tid`) and (`ugc_fid_map`.`tid` = `ugc_file`.`tid`) and (`ugc_dat`.`dat_id` = `ugc_fid_map`.`dat_id`) and (`ugc_video`.`uid` = `auth_user`.`id`)) */;

--
-- Final view structure for view `v_get_pass_tasklist`
--

/*!50001 DROP TABLE `v_get_pass_tasklist`*/;
/*!50001 DROP VIEW IF EXISTS `v_get_pass_tasklist`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`ugc_kaifa`@`%` SQL SECURITY INVOKER */
/*!50001 VIEW `v_get_pass_tasklist` AS select `ugc_audit_log`.`tid` AS `tid`,`ugc_audit_log`.`uid` AS `uid`,`ugc_video`.`title` AS `title`,`ugc_video`.`tags` AS `tags`,`ugc_video`.`channel` AS `channel`,`ugc_video`.`step` AS `step`,`ugc_video`.`status` AS `status`,`ugc_file`.`funshion_id` AS `funshion_id`,`ugc_video`.`priority` AS `priority`,`ugc_audit_log`.`time` AS `time`,`ugc_file`.`video_url` AS `video_url`,`ugc_file`.`small_image` AS `small_image`,`ugc_file`.`large_image` AS `large_image`,`ugc_file`.`duration` AS `duration`,`auth_user`.`username` AS `username`,`ugc_video`.`vid` AS `vid`,`ugc_file`.`rate` AS `rate` from (((`ugc_audit_log` join `ugc_video`) join `ugc_file`) join `auth_user`) where ((`ugc_audit_log`.`tid` = `ugc_video`.`tid`) and (`ugc_audit_log`.`tid` = `ugc_file`.`tid`) and (`ugc_audit_log`.`flag` = 1) and (`ugc_video`.`site` <> _gbk'qy') and (`ugc_audit_log`.`uid` = `auth_user`.`id`)) */;

--
-- Final view structure for view `v_get_pending_tasklist`
--

/*!50001 DROP TABLE `v_get_pending_tasklist`*/;
/*!50001 DROP VIEW IF EXISTS `v_get_pending_tasklist`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`ugc_kaifa`@`%` SQL SECURITY INVOKER */
/*!50001 VIEW `v_get_pending_tasklist` AS select `ugc_audit_workspace`.`tid` AS `tid`,`ugc_audit_workspace`.`uid` AS `uid`,`ugc_video`.`title` AS `title`,`ugc_video`.`tags` AS `tags`,`ugc_video`.`channel` AS `channel`,`ugc_video`.`step` AS `step`,`ugc_video`.`status` AS `status`,`ugc_file`.`funshion_id` AS `funshion_id`,`ugc_video`.`priority` AS `priority`,`ugc_audit_workspace`.`time` AS `time`,`ugc_file`.`video_url` AS `video_url`,`ugc_file`.`small_image` AS `small_image`,`ugc_file`.`large_image` AS `large_image`,`ugc_file`.`duration` AS `duration`,`auth_user`.`username` AS `username`,`ugc_video`.`vid` AS `vid`,`ugc_file`.`rate` AS `rate` from (((`ugc_audit_workspace` join `ugc_video`) join `ugc_file`) join `auth_user`) where ((`ugc_audit_workspace`.`tid` = `ugc_video`.`tid`) and (`ugc_audit_workspace`.`tid` = `ugc_file`.`tid`) and (`ugc_video`.`step` = _gbk'audit') and (`ugc_video`.`status` = 0) and (`ugc_video`.`site` <> _gbk'qy') and (`ugc_audit_workspace`.`uid` = `auth_user`.`id`)) */;

--
-- Final view structure for view `v_get_user_audit_info`
--

/*!50001 DROP TABLE `v_get_user_audit_info`*/;
/*!50001 DROP VIEW IF EXISTS `v_get_user_audit_info`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`ugc_kaifa`@`%` SQL SECURITY INVOKER */
/*!50001 VIEW `v_get_user_audit_info` AS select `ugc_video`.`tid` AS `tid`,`ugc_audit_log`.`uid` AS `uid`,`auth_user`.`username` AS `username`,`ugc_audit_log`.`flag` AS `flag`,`ugc_audit_log`.`time` AS `time` from ((`ugc_video` join `ugc_audit_log`) join `auth_user`) where ((`ugc_video`.`tid` = `ugc_audit_log`.`tid`) and (`auth_user`.`id` = `ugc_audit_log`.`uid`)) */;

--
-- Final view structure for view `v_get_user_audit_info_v2`
--

/*!50001 DROP TABLE `v_get_user_audit_info_v2`*/;
/*!50001 DROP VIEW IF EXISTS `v_get_user_audit_info_v2`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`ugc_kaifa`@`%` SQL SECURITY INVOKER */
/*!50001 VIEW `v_get_user_audit_info_v2` AS select `ugc_audit_log`.`tid` AS `tid`,`ugc_audit_log`.`uid` AS `uid`,`auth_user`.`username` AS `username`,`ugc_audit_log`.`flag` AS `flag`,`ugc_audit_log`.`time` AS `time` from (`ugc_audit_log` join `auth_user`) where (`auth_user`.`id` = `ugc_audit_log`.`uid`) */;

--
-- Final view structure for view `v_get_verify_examresult`
--

/*!50001 DROP TABLE `v_get_verify_examresult`*/;
/*!50001 DROP VIEW IF EXISTS `v_get_verify_examresult`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`ugc_kaifa`@`%` SQL SECURITY INVOKER */
/*!50001 VIEW `v_get_verify_examresult` AS select `ugc_video`.`tid` AS `tid`,`ugc_video`.`uid` AS `uid`,`ugc_video`.`ip` AS `ip`,`ugc_video`.`port` AS `port`,`ugc_file`.`funshion_id` AS `funshion_id`,`ugc_audit_log`.`flag` AS `flag`,`ugc_video`.`site` AS `site`,`ugc_video`.`ttype` AS `ttype` from ((`ugc_video` join `ugc_file`) join `ugc_audit_log`) where ((`ugc_video`.`tid` = `ugc_file`.`tid`) and (`ugc_audit_log`.`funshion_id` = `ugc_file`.`funshion_id`)) */;

--
-- Final view structure for view `v_video_base`
--

/*!50001 DROP TABLE `v_video_base`*/;
/*!50001 DROP VIEW IF EXISTS `v_video_base`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`ugc_kaifa`@`%` SQL SECURITY INVOKER */
/*!50001 VIEW `v_video_base` AS select `ugc_video`.`uid` AS `uid`,`auth_user`.`username` AS `username`,`ugc_video`.`tid` AS `tid`,`ugc_video`.`site` AS `site`,`ugc_video`.`title` AS `title`,`ugc_video`.`tags` AS `tags`,`ugc_video`.`origin` AS `origin`,`ugc_video`.`channel` AS `channel`,`ugc_video`.`description` AS `description`,`ugc_video`.`priority` AS `priority`,`ugc_video`.`step` AS `step`,`ugc_video`.`status` AS `status`,`ugc_video`.`video_id` AS `video_id`,`ugc_video`.`seconds` AS `seconds`,`ugc_video`.`ttype` AS `ttype` from (`ugc_video` join `auth_user`) where (`ugc_video`.`uid` = `auth_user`.`id`) */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-03-25 15:52:52
