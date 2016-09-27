-- MySQL dump 10.13  Distrib 5.6.15, for Linux (x86_64)
--
-- Host: 123.130.127.204    Database: ugc
-- ------------------------------------------------------
-- Server version	5.6.15

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
-- Dumping routines for database 'ugc'
--

/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_add_audit_log` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_add_audit_log`(IN i_uid int, IN i_tid varchar(128)  CHARACTER SET utf8, IN i_funshionid varchar(64)  CHARACTER SET utf8,IN i_result int)
    SQL SECURITY INVOKER
BEGIN

    set @exsted_value = (select 1 from ugc_audit_log where tid = i_tid limit 1 );
    if @exsted_value is null THEN
        insert into ugc_audit_log(tid, funshion_id, uid ,flag, time, del_flag) select i_tid, funshion_id, i_uid, i_result, now(),0   from ugc_file where tid = i_tid and funshion_id = i_funshionid limit 1;
    ELSE
        update ugc_audit_log set uid=i_uid, funshion_id= i_funshionid,flag=i_result where tid = i_tid;
    end if;
 END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_add_audit_workspace` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_add_audit_workspace`(IN `i_tid` varchar(128),IN `i_uid` int)
    SQL SECURITY INVOKER
BEGIN

    START TRANSACTION;
    set @exsted_value = (select 1 from ugc_audit_workspace where tid = i_tid limit 1 );

    if @exsted_value is null THEN
        insert into ugc_audit_workspace(tid, uid) values(i_tid, i_uid);
    end if;
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_add_dat` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_add_dat`(IN `datid` int,IN `datsize` int,IN `mserverip` varchar(20),IN `mserverport` int,OUT `flag` int)
    SQL SECURITY INVOKER
BEGIN
  
    START TRANSACTION;
    set @exsted_value = (select 1 from ugc_dat where dat_id = datid limit 1 );
    if @exsted_value=1 THEN
        update ugc_dat set dat_size=datsize, mserver_ip=mserverip, mserver_port=mserverport where dat_id=datid;
        set flag = 2;
    else 
        insert into ugc_dat(dat_id, dat_size, mserver_ip, mserver_port, flag) values(datid, datsize, mserverip, mserverport,0);
        set flag = 1;
    end if;
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_add_package_report` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_add_package_report`(IN i_infohash VARCHAR(64)  CHARACTER SET utf8, IN i_size BIGINT,IN i_mserver_ip VARCHAR(64)  CHARACTER SET utf8, IN i_mserver_port VARCHAR(32)  CHARACTER SET utf8,  IN i_package_list_values VARCHAR(10240) CHARACTER SET utf8, IN i_tid_list_values VARCHAR(10240) CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    SET @exsted_value = 1;

    SET @exsted_value = (SELECT 1 FROM ugc_dat WHERE dat_id = i_infohash LIMIT 1);
    IF @exsted_value IS NULL THEN
        INSERT INTO ugc_dat(dat_id, dat_size, mserver_ip, mserver_port,distribution_time, flag, del_flag)
            VALUES(i_infohash, i_size, i_mserver_ip, i_mserver_port, NOW(), 0, 0);
            
        SET @strsql = CONCAT("insert into ugc_fid_map(dat_id, tid) values ", i_package_list_values);
        PREPARE stmtsql FROM @strsql;
        EXECUTE   stmtsql;

        SET @strsql = CONCAT("update ugc_video set step = 'mpacker', status = 1 where tid in", i_tid_list_values);
        PREPARE stmtsql FROM @strsql;
        EXECUTE   stmtsql;
    END IF;

    SELECT @exsted_value;
    COMMIT;
 END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_add_taskid_tid` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_add_taskid_tid`(IN i_tid VARCHAR(128)  CHARACTER SET utf8, IN i_task_id VARCHAR(32)  CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    
    START TRANSACTION; 
    UPDATE ugc_video SET step = 'transcode', STATUS=0, task_id = i_task_id WHERE tid = i_tid;
    COMMIT;
 END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_add_transcode_report` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_add_transcode_report`(IN i_tid VARCHAR(128) CHARACTER SET utf8, IN i_add_file_values VARCHAR(20480) CHARACTER SET utf8, IN  i_ip VARCHAR(64) CHARACTER SET utf8, IN i_port VARCHAR(32) CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN

    START TRANSACTION;

    SET @exsted_value = (SELECT 1 FROM ugc_file WHERE tid = i_tid LIMIT 1);
    IF @exsted_value IS  NULL THEN
        SET @strsql = CONCAT('insert into ugc_file(funshion_id, tid, rate, file_size, filename, duration, video_url, small_image, large_image, ctime, definition) values',i_add_file_values,'');
        PREPARE stmtsql FROM @strsql;
        EXECUTE   stmtsql;
        SET @audit = (SELECT 1 FROM ugc_video WHERE tid = i_tid and (site = 'kkn' or (site = 'cntv' and channel like '新闻%') or audit_free = 1) LIMIT 1);

        IF @audit IS  NULL THEN
            UPDATE ugc_video SET ip = i_ip, PORT = i_port, step='audit', STATUS=0, mtime=NOW() WHERE tid = i_tid;
        ELSE
            UPDATE ugc_video SET ip = i_ip, PORT = i_port, step='audit', STATUS=1, mtime=NOW() WHERE tid = i_tid;
        END IF;    
        
        SET @flag = 1;
    END IF;

    SELECT @flag;

    COMMIT;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_add_video_task` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_add_video_task`(IN i_tid VARCHAR(64), IN i_uid  INT,IN i_vid VARCHAR(256)  CHARACTER SET utf8, IN i_site VARCHAR(32), IN i_title VARCHAR(1024) CHARACTER SET utf8,
   IN i_describe VARCHAR(1024) CHARACTER SET utf8, IN i_tags VARCHAR(512) CHARACTER SET utf8, IN i_channel VARCHAR(512)  CHARACTER SET utf8, IN i_origin VARCHAR(64)  CHARACTER SET utf8, IN i_priority INT, IN i_pubtime VARCHAR(64)  CHARACTER SET utf8, IN i_audit BOOLEAN)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    INSERT INTO ugc_video(tid, site, title, tags, origin, channel, description, priority, step, STATUS, vid,  uid, ctime, mtime, pub_time, audit_free)  
        VALUES(i_tid, i_site, i_title, i_tags, i_origin, i_channel, i_describe, i_priority, 'submit' , 1, i_vid, i_uid, NOW(), NOW(), i_pubtime, i_audit);

    SELECT i_uid, i_tid;
    COMMIT;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_apply_task` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_apply_task`(IN`userid` int, IN `task_count` int, IN `i_condition` varchar(1024) CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    DECLARE t_condition varchar(1024);
    DECLARE strsql   varchar(1024);

    START TRANSACTION;
    set @count = concat('select count(*) from ugc_video ', i_condition,  ' and ugc_video.site !="kkn" and  ugc_video.tid not in (select ugc_audit_workspace.tid from ugc_audit_workspace) limit ', task_count);
 
    set @strsql = concat('insert into ugc_audit_workspace(tid, uid, time) select  ugc_video.tid,', userid, ', now() from ugc_video ',i_condition,
              ' and ugc_video.site !="kkn" and ugc_video.tid not in (select ugc_audit_workspace.tid from ugc_audit_workspace) order by priority desc   limit ', task_count);

    prepare stmtsqlcount from @count;
    prepare stmtsql from @strsql;
   
    execute   stmtsqlcount; 
    execute   stmtsql; 

    deallocate prepare stmtsqlcount;
    deallocate prepare stmtsql;
    COMMIT;
 
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_apply_task_test` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_apply_task_test`(IN`userid` int, IN `task_count` int)
    SQL SECURITY INVOKER
BEGIN

    DECLARE t_condition varchar(1024);
    DECLARE strsql   varchar(1024);

    START TRANSACTION;
    set @count = concat('select count(*) from ugc_video  and ugc_video.site !="kkn" and  ugc_video.tid not in (select ugc_audit_workspace.tid from ugc_audit_workspace) limit ', task_count);
 
    set @strsql = concat('insert into ugc_audit_workspace(tid, uid, time) select  ugc_video.tid,', userid, ', now() from ugc_video 
               where  ugc_video.site !="kkn" and ugc_video.step = "audit" and ugc_video.status=0 and  ugc_video.tid not in (select ugc_audit_workspace.tid from ugc_audit_workspace) order by priority desc   limit ', task_count);

    prepare stmtsql from @strsql;
    execute   stmtsql; 
    deallocate prepare stmtsql;
    COMMIT;
 
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_apply_task_v2` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_apply_task_v2`(IN`userid` int, IN `task_count` int, IN `i_condition` varchar(1024) CHARACTER SET utf8, IN `i_username` varchar(32))
    SQL SECURITY INVOKER
BEGIN
  
    DECLARE t_condition varchar(1024);
    DECLARE strsql   varchar(1024);
    
    if i_username = 'None' THEN
        call proc_apply_task(userid, task_count, i_condition);
    else
        START TRANSACTION;
        set @from_userid = (select id from auth_user where username=i_username);
        set @count = concat('select count(*) from ugc_video ', i_condition,  ' and uid=',@from_userid,' and  ugc_video.site !="kkn" and ugc_video.tid not in (select ugc_audit_workspace.tid from ugc_audit_workspace)  limit ', task_count);
 
        set @strsql = concat('insert into ugc_audit_workspace(tid, uid, time) select  ugc_video.tid,', userid, ', now() from ugc_video ',i_condition,
              ' and  uid=',@from_userid,' and ugc_video.site !="kkn" and  ugc_video.tid not in (select ugc_audit_workspace.tid from ugc_audit_workspace)  limit ', task_count);

        prepare stmtsqlcount from @count;
        prepare stmtsql from @strsql;
   
        execute   stmtsqlcount; 
        execute   stmtsql;

        deallocate prepare stmtsqlcount;

        deallocate prepare stmtsql;
        COMMIT;
    end if;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_audit_video_task` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_audit_video_task`(IN i_uid int, IN i_tid varchar(128),  IN i_funshionid varchar(64), IN i_result int, IN i_title varchar(256), IN i_channel varchar(512), IN i_logo varchar(1024))
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    set @op_flag = 1;

    set @exsted_value = (select 1 from ugc_audit_log where tid = i_tid and funshion_id = i_funshionid  limit 1);
    if @exsted_value=1 THEN
        set @op_flag = 0;
    end if;

    set @if_exsted = (select 1 from ugc_audit_workspace where tid = i_tid and uid=i_uid limit 1);
    if @if_exsted is  null THEN
        set @op_flag = 0;
    end if;

    if @op_flag=1 THEN

        if i_title !="" and i_channel !="" and i_logo != "" THEN
            update ugc_video set title = i_title, channel = i_channel  where tid=i_tid;
            update ugc_file set logo=i_logo where tid=i_tid;
        elseif  i_title ="" and i_channel !="" and i_logo != "" THEN
            update ugc_video set channel = i_channel  where tid=i_tid;
            update ugc_file set logo=i_logo where tid=i_tid;
        elseif  i_title ="" and i_channel ="" and i_logo != "" THEN
            update ugc_file set logo=i_logo where tid=i_tid;
        elseif  i_title !="" and i_channel ="" and i_logo != "" THEN
            update ugc_video set title = i_title  where tid=i_tid;
            update ugc_file set logo=i_logo where tid=i_tid;
        end if;

        call proc_delete_workspace(i_uid, i_tid);

        call proc_add_audit_log(i_uid, i_tid, i_funshionid, i_result);
   
        if  i_result=1 THEN
            update ugc_video set step="audit",status=1 where  tid=i_tid;
        else
            update ugc_video set step="audit",status=2 where  tid=i_tid;
        end if;
     
    end if;

    select  @op_flag, i_tid;
    COMMIT;
 END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_audit_video_task_v2` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_audit_video_task_v2`(IN i_uid int, IN i_tid varchar(128) CHARACTER SET utf8,  IN i_funshionid varchar(64) CHARACTER SET utf8, IN i_result int, IN i_base_modify varchar(10240) CHARACTER SET utf8, IN i_audit_modify varchar(10240) CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    set names utf8;

    set @op_flag = 1;
   
    call proc_delete_workspace(i_uid, i_tid);

    if  i_result=1 THEN
        update ugc_video set step="audit",status=1, mtime=now() where  tid=i_tid;
    else
        update ugc_video set step="audit",status=2, mtime=now() where  tid=i_tid;
    end if;

    if i_base_modify != "" THEN
        set @sql_sentence = CONCAT("update ugc_video set " , i_base_modify , " where tid=" , "'",i_tid,"';");
        prepare stmt from @sql_sentence;
        EXECUTE stmt;
    end if;

    if i_audit_modify != "" THEN
        set @sql_sentence = CONCAT("update ugc_file set " , i_audit_modify , " where tid=" , "'",i_tid,"';");
        prepare stmt from @sql_sentence;
        EXECUTE stmt;
    end if;

    call proc_add_audit_log(i_uid, i_tid, i_funshionid, i_result);
    select  @op_flag, i_tid;
    COMMIT;
 END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_cancel_audit_task` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_cancel_audit_task`(IN i_uid int, IN i_tid varchar(128)   CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
   
    START TRANSACTION;
    set @exsted_value = (select 1 from ugc_audit_workspace where tid = i_tid limit 1 );
    if @exsted_value is not null THEN
        call proc_delete_workspace(i_uid, i_tid);
        update ugc_video set step="audit",status=0 where  tid=i_tid;
        set @op_flag = 1;
        select  @op_flag, i_tid;
    ELSE
        set @op_flag = 0;
        select  @op_flag, i_tid;
    end if;

    COMMIT;
 END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_cancel_audit_task_v2` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_cancel_audit_task_v2`(IN i_uid int, IN i_tid_list_values varchar(1024))
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    set @strsql = concat("delete  from ugc_audit_workspace  where tid in ",i_tid_list_values, "");
    prepare stmtsql from @strsql;
    execute   stmtsql;
    set @op_flag = 1;
    select  @op_flag, i_tid_list_values; 
    COMMIT;
 END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_cloud_add_task_map` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_cloud_add_task_map`(IN i_tid varchar(128)  CHARACTER SET utf8, IN i_task_id varchar(32)  CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    
    START TRANSACTION; 
    set @exsted_value = 1;
    set @exsted_value = (select 1 from ugc_cloud_task_map where task_id = i_task_id  limit 1);
    if @exsted_value is  null THEN
        insert into ugc_cloud_task_map(task_id, tid, flag) values(i_task_id , i_tid, 0);
    end if;
    select @exsted_value;
    COMMIT;
 END ;;
DELIMITER ;

/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_cloud_get_delete_audit_failed` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_cloud_get_delete_audit_failed`(IN  i_tid_values  varchar(2048) CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    set @strsql = concat("select DISTINCT tid from ugc_fid_map where  tid in ",i_tid_values ,"");
    prepare stmtsql from @strsql;
    execute stmtsql;
    deallocate prepare stmtsql;
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_cloud_get_delete_taskid` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_cloud_get_delete_taskid`(IN  i_tid_values  varchar(2048) CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    set @strsql = concat("select task_id from ugc_cloud_task_map  where tid in  ",i_tid_values ,"");
    prepare stmtsql from @strsql;
    execute stmtsql;
    deallocate prepare stmtsql;
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_cloud_get_delete_taskinfo` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_cloud_get_delete_taskinfo`(IN i_dat_id varchar(64) CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    set @strsql = concat("select DISTINCT ugc_cloud_task_map.task_id  from ugc_fid_map, ugc_cloud_task_map  where  ugc_fid_map.tid =ugc_cloud_task_map.tid  and  ugc_fid_map.dat_id ='", i_dat_id , "'");

    prepare stmtsql from @strsql;
    execute stmtsql;
    deallocate prepare stmtsql;
    
    set @strsql = concat("update  ugc_dat  set del_flag=1  where   dat_id ='", i_dat_id , "'");

    prepare stmtsql from @strsql;
    execute stmtsql;
    deallocate prepare stmtsql;
    COMMIT;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_cloud_get_delete_taskinfo_v2` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_cloud_get_delete_taskinfo_v2`(IN i_dat_id varchar(64) CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN

    START TRANSACTION;
    set @strsql = concat("select DISTINCT ugc_cloud_task_map.task_id,ugc_audit_log.time, ugc_audit_log.flag   from  ugc_audit_log, ugc_cloud_task_map  where  ugc_audit_log.tid =ugc_cloud_task_map.tid order by ugc_audit_log.time asc limit 20");
    prepare stmtsql from @strsql;
    execute stmtsql;
    deallocate prepare stmtsql;

    set @strsql = concat("update  ugc_dat  set del_flag=1  where   dat_id ='", i_dat_id , "'");
    prepare stmtsql from @strsql;
    execute stmtsql;
    deallocate prepare stmtsql;
    COMMIT;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_cloud_get_statics_time` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_cloud_get_statics_time`(IN `i_tid` varchar(128)  CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN

    START TRANSACTION;

    set @strsql = concat("select tid, ctime   from ugc_video where  tid ='",i_tid,"'");
    
    prepare stmtsql from @strsql;
    execute   stmtsql;
    deallocate prepare stmtsql;
    
    set @strsql = concat("select DISTINCT ugc_audit_log.tid, ugc_audit_log.time, ugc_file.ctime   from ugc_audit_log, ugc_file where  ugc_audit_log.tid = ugc_file.tid  and ugc_audit_log.tid ='",i_tid,"'");
    
    prepare stmtsql from @strsql;
    execute   stmtsql;
    deallocate prepare stmtsql;
    
    set @strsql = concat("select DISTINCT ugc_dat.distribution_time, ugc_dat.sendmacros_time   from ugc_fid_map, ugc_dat where ugc_fid_map.dat_id = ugc_dat.dat_id  and ugc_fid_map.tid ='",i_tid,"'");
    prepare stmtsql from @strsql;
    execute   stmtsql;
    deallocate prepare stmtsql;

    COMMIT;
 
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_cloud_get_tasklist` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_cloud_get_tasklist`(IN `task_count` int)
    SQL SECURITY INVOKER
BEGIN

    START TRANSACTION;
    
    create temporary table if not exists tb_update_tid(tid varchar(128) PRIMARY KEY, site varchar(32), vid varchar(256), priority int) DEFAULT CHARSET=utf8;
    set @strsql = concat('insert into tb_update_tid(tid, site, vid, priority) select tid, site, vid, priority from ugc_video where  step = "spider" or step="push"  or step = "forwards" or step="upload"  order by priority desc limit ', task_count);
    prepare stmtsql from @strsql;
    execute   stmtsql;
    deallocate prepare stmtsql;
    select * from tb_update_tid;
    update ugc_video set step = 'taskmanager', status=1  where tid in (select tid from tb_update_tid);
    drop table  if exists tb_update_tid;

    COMMIT;
 
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_cloud_get_task_delete` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_cloud_get_task_delete`(IN `task_count` int, IN `diff_day` int)
    SQL SECURITY INVOKER
BEGIN
    
    START TRANSACTION;
    create temporary table if not exists tb_delete_tid(tid varchar(128), time varchar(128)) DEFAULT CHARSET=utf8;
   
    
    set @strsql = concat('insert into tb_delete_tid(tid, time) select tid, time from ugc_audit_log where del_flag <> 1 and (flag=0 or time like "2013%") order by time asc limit ', task_count);
    prepare stmtsql from @strsql;
    execute   stmtsql;
    deallocate prepare stmtsql;
    
    update ugc_audit_log set del_flag=1  where tid in (select tid from tb_delete_tid);
    

    set @strsql = concat('select task_id  from ugc_cloud_task_map where tid in (select tid from tb_delete_tid)');
    prepare stmtsql from @strsql;
    execute   stmtsql;
    deallocate prepare stmtsql;
    drop table  if exists tb_delete_tid;

    COMMIT;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_cloud_get_task_delete_copy` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_cloud_get_task_delete_copy`(IN `task_count` int, IN `diff_day` int)
    SQL SECURITY INVOKER
BEGIN

    START TRANSACTION;  
    create temporary table if not exists tb_delete_tid(tid varchar(128) PRIMARY KEY, time varchar(128)) DEFAULT CHARSET=utf8;
    
    set @strsql = concat('insert into tb_delete_tid(tid, time) select tid, time from ugc_audit_log where del_flag <> 1 and flag=0  order by time asc limit ', task_count);
    prepare stmtsql from @strsql;
    execute   stmtsql;
    deallocate prepare stmtsql;
    
    update ugc_audit_log set del_flag=1  where tid in (select tid from tb_delete_tid);

    set @strsql = concat('select task_id  from ugc_cloud_task_map where tid in (select tid from tb_delete_tid)');
    prepare stmtsql from @strsql;
    execute   stmtsql;
    deallocate prepare stmtsql;
    drop table  if exists tb_delete_tid;

    COMMIT;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_cloud_repair_error_info` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_cloud_repair_error_info`(IN i_tid varchar(128) CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    delete from ugc_fid_map where tid = i_tid;
    delete from ugc_audit_log where tid = i_tid;
    update ugc_video set step='spider', status = 1 where tid = i_tid;
    delete from ugc_file where tid = i_tid;
    COMMIT;

 END ;;
DELIMITER ;

/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_cloud_update_trans_fail` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_cloud_update_trans_fail`(IN i_task_id varchar(32)  CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    set @exsted_value = 1;
    set @tid = (select tid from ugc_cloud_task_map where task_id = i_task_id limit 1);
    update ugc_video set  step='transcode', status=2 where tid=@tid;
    select @exsted_value;
    COMMIT;
 END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_cloud_verify_task` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_cloud_verify_task`(IN i_uid int, IN i_taskid int,  IN i_result int)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;

    set @op_flag = 1;
    set @i_tid = (select tid from ugc_cloud_task_map where task_id = i_taskid limit 1);

    set @exsted_value = (select 1 from ugc_audit_log where tid = @i_tid   limit 1);
    if @exsted_value=1 THEN
        set @op_flag = 0;
    end if;

    if @op_flag=1 THEN
        if  i_result=1 THEN
            update ugc_video set step="audit",status=1, mtime=now() where  tid=@i_tid;
        else
            update ugc_video set step="audit",status=2, mtime=now() where  tid=@i_tid;
        end if;
        insert into ugc_audit_log(tid, funshion_id, uid, flag, time) select @i_tid, funshion_id, i_uid, 1, now() from ugc_file where tid = @i_tid;
    end if;

    select  @op_flag;
    COMMIT;
 END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_delete_workspace` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_delete_workspace`(IN i_uid int, IN i_tid varchar(128)  CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
     delete from ugc_audit_workspace where tid = i_tid;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_get_all_tasklist` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_get_all_tasklist`(IN `i_uid` int)
    SQL SECURITY INVOKER
BEGIN

    declare done int;
    declare done2 int;
    declare i_tid varchar(128);
    declare t_title varchar(256);
    declare t_tags varchar(512);
    declare t_channel varchar(512);
    declare t_step  varchar(64);
    declare t_status  int;
    declare t_funshion_id varchar(64); 
    declare t_video_url varchar(1024);
    declare t_small_image varchar(1024);
    declare t_large_image varchar(1024);

    DECLARE rs_cursor CURSOR  FOR 
        select ugc_audit_log.tid from ugc_audit_log  where uid=i_uid;
     
    DECLARE rs_cursor2 CURSOR  FOR 
        select title, tags, channel, step, status, funshion_id, video_url, small_image, large_image from v_get_audit_detail_task  where tid=i_tid;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done=1;

    drop table if exists tmp_tidtb;
    CREATE TEMPORARY TABLE tmp_tidtb(tid varchar(128)  primary key, uid int);

    drop table if exists tmp_detail_info;
    CREATE TEMPORARY TABLE tmp_detail_info(tid varchar(128)  primary key, uid int, title varchar(256), tags varchar(512), channel varchar(512), step  varchar(64), status  int, funshion_id varchar(64), video_url varchar(1024), small_image varchar(1024), large_image varchar(1024));

    insert into  tmp_tidtb(tid, uid) select tid, i_uid from  ugc_audit_workspace where uid=i_uid;

    START TRANSACTION;
    set @count = 0;

    open rs_cursor;
    cursor_loop:loop
        FETCH rs_cursor into i_tid;
        if done=1 THEN
            LEAVE cursor_loop;
        end if;

        set @exsted_value = (select 1 from tmp_tidtb where tid = i_tid limit 1);
        if @exsted_value is  null THEN
            insert into  tmp_tidtb(tid, uid) values(i_tid, i_uid);
        end if;
    END loop cursor_loop;

    open rs_cursor2;
    cursor2_loop:loop
        FETCH rs_cursor2 into i_tid;
        if done2=1 THEN
            LEAVE cursor2_loop;
        end if;
   
        set @exsted_value = (select 1 from tmp_tidtb where tid = i_tid limit 1 );
        if @exsted_value is  null THEN
            insert into  tmp_tidtb(tid, uid) values(i_tid, i_uid);
        end if;
    END loop cursor2_loop;

    CLOSE rs_cursor2;
    set done2 = 0;

    CLOSE rs_cursor; 
    set done = 0;
    COMMIT;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_get_details_info` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_get_details_info`(IN `i_tid` varchar(128)  CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    set @strsql = concat("select ugc_video.tid,ugc_video.uid,ugc_video.title,ugc_video.tags,ugc_video.channel,ugc_file.funshion_id, ugc_file.filename, ugc_file.file_size, ugc_file.video_url,
            ugc_file.small_image,ugc_file.large_image,ugc_file.logo,ugc_file.rate, ugc_file.duration, ugc_video.step, ugc_video.status, ugc_video.priority,ugc_video.mtime as time,auth_user.username,
            ugc_video.vid,ugc_video.description, ugc_video.site
            from ugc_video, ugc_file, auth_user where  ugc_video.tid=ugc_file.tid and  auth_user.id = ugc_video.uid  and  ugc_video.tid='",i_tid,"' limit 1");

    prepare stmtsql from @strsql; 
    execute stmtsql;
    deallocate prepare stmtsql; 
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_get_next_task` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_get_next_task`(IN `i_uid` int)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    set @strsql = concat("select DISTINCT ugc_video.tid,ugc_video.uid,ugc_video.title,ugc_video.tags,ugc_video.channel,ugc_file.funshion_id, ugc_file.filename, ugc_file.file_size, ugc_file.video_url,
            ugc_file.small_image,ugc_file.large_image,ugc_file.logo,ugc_file.rate, ugc_file.duration, ugc_video.step, ugc_video.status, ugc_video.priority,ugc_video.mtime as time,auth_user.username,ugc_video.vid,ugc_video.description, ugc_video.site
            from ugc_video, ugc_file,ugc_audit_workspace, auth_user where ugc_video.step='audit' and ugc_video.status=0 and ugc_audit_workspace.tid=ugc_video.tid and ugc_video.tid=ugc_file.tid and  auth_user.id = ugc_video.uid and ugc_audit_workspace.uid=",i_uid," ORDER BY ugc_video.priority desc, ugc_video.ctime limit 1");
      
    prepare stmtsql from @strsql; 
    execute stmtsql;
    deallocate prepare stmtsql; 
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_get_video_url` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_get_video_url`(IN `i_tid` varchar(128))
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    set @sqlstr = concat("select ugc_fid_map.funshion_id,ugc_fid_map.dat_id,ugc_dat.mserver_ip from ugc_fid_map,ugc_dat where ugc_fid_map.tid='",i_tid,"' and ugc_fid_map.dat_id=ugc_dat.dat_id GROUP BY ugc_fid_map.tid;");
    prepare stmtsql from @sqlstr; 
    execute stmtsql; 
    deallocate prepare stmtsql;
    COMMIT;
END ;;
DELIMITER ;

/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_page_get_all_task` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_page_get_all_task`(IN `i_pagecurrent` int,  IN `i_pagesize` int,IN `i_uid` int,  IN `i_searchstr`  varchar(1024)  CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    if i_uid <> -1 THEN
        set @uid_str = concat(" where uid=",i_uid);
    ELSE
        set @uid_str = " ";
    end if;

    set @strsql = concat("select count(DISTINCT(tid)) from ugc_video  where  tid in (select tid from  ugc_audit_workspace ", @uid_str, ") or tid in (select tid from ugc_audit_log ",@uid_str,") ",i_searchstr,"");
    prepare stmtsql from @strsql; 
    execute stmtsql; 
    deallocate prepare stmtsql;
    set @start_pos = i_pagesize*(i_pagecurrent-1); 

    set @strsql = concat("select ugc_video.tid,ugc_video.uid,ugc_video.title,ugc_video.tags,ugc_video.channel,ugc_video.step,ugc_video.status,ugc_file.funshion_id, ugc_video.mtime,
        ugc_file.duration,auth_user.username,ugc_video.vid,ugc_video.priority
        from ugc_video, ugc_file, auth_user where ugc_video.ip is not null and ugc_video.port is not null ", i_searchstr ," and (ugc_video.tid in (select tid from  ugc_audit_workspace ", @uid_str, ") or ugc_video.tid in (select tid from ugc_audit_log ",@uid_str,")) and 
        ugc_video.tid=ugc_file.tid and  auth_user.id = ugc_video.uid ORDER BY ugc_video.priority desc , ugc_video.ctime desc limit ",@start_pos,",",i_pagesize);

    prepare stmtsql from @strsql;
    execute stmtsql;
    deallocate prepare stmtsql; 
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_page_get_failed_task` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_page_get_failed_task`(IN `i_pagecurrent` int,  IN `i_pagesize` int,IN `i_uid` int, IN `i_searchstr`  varchar(1024)  CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    if i_uid <> -1 THEN
        set @uid_str = concat(" and ugc_audit_log.uid=",i_uid);
    ELSE
        set @uid_str = "";
    end if;

    set @strsql = concat("select count(DISTINCT(ugc_video.tid)) from ugc_video,ugc_audit_log   where  ugc_audit_log.flag = 0 and ugc_video.tid=ugc_audit_log.tid ", @uid_str," ", i_searchstr);
    prepare stmtsql from @strsql; 
    execute stmtsql;
    deallocate prepare stmtsql; 

    set @start_pos = i_pagesize*(i_pagecurrent-1); 
    set @strsql = concat("select ugc_video.tid, ugc_video.uid, ugc_video.title, ugc_video.tags, ugc_video.channel, ugc_video.step, ugc_video.status, ugc_file.funshion_id, ugc_audit_log.time,
        ugc_file.duration, auth_user.username, ugc_video.vid, ugc_video.priority from ugc_video, ugc_file, ugc_audit_log, auth_user where ugc_audit_log.flag = 0 ",@uid_str, " ", i_searchstr ," and  ugc_video.tid=ugc_file.tid and ugc_audit_log.tid=ugc_video.tid and auth_user.id = ugc_audit_log.uid ORDER BY ugc_video.ctime desc limit ",@start_pos,",",i_pagesize);
    prepare stmtsql from @strsql; 
    execute stmtsql; 
    deallocate prepare stmtsql; 
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_page_get_passed_task` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_page_get_passed_task`(IN `i_pagecurrent` int,  IN `i_pagesize` int,IN `i_uid` int,  IN `i_searchstr`  varchar(1024)  CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    if i_uid <> -1 THEN
        set @uid_str = concat(" and ugc_audit_log.uid=",i_uid);
    ELSE
        set @uid_str = "";
    end if;

    set @strsql = concat("select count(DISTINCT(ugc_video.tid)) from ugc_video,ugc_audit_log   where  ugc_audit_log.flag = 1 and ugc_video.tid=ugc_audit_log.tid ", @uid_str," ", i_searchstr);
    prepare stmtsql from @strsql;
    execute stmtsql;
    deallocate prepare stmtsql;

    set @start_pos = i_pagesize*(i_pagecurrent-1); 
    set @strsql = concat("select ugc_video.tid, ugc_video.uid, ugc_video.title, ugc_video.tags, ugc_video.channel, ugc_video.step, ugc_video.status, ugc_file.funshion_id, ugc_audit_log.time,
        ugc_file.duration, auth_user.username, ugc_video.vid, ugc_video.priority from ugc_video, ugc_file, ugc_audit_log, auth_user where  ugc_audit_log.flag = 1  ",@uid_str, " ", i_searchstr ," and  ugc_video.tid=ugc_file.tid and ugc_audit_log.tid=ugc_video.tid and auth_user.id = ugc_audit_log.uid ORDER BY  ugc_video.ctime desc limit ",@start_pos,",",i_pagesize);
    prepare stmtsql from @strsql; 
    execute stmtsql; 
    deallocate prepare stmtsql; 
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_page_get_pending_task` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_page_get_pending_task`(IN `i_pagecurrent` int,  IN `i_pagesize` int,IN `i_uid` int)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    if i_uid <> -1 THEN
        set   @uid_str = concat(" ugc_audit_workspace.uid=",i_uid);
    ELSE
        set @uid_str = "";
    end if;
     
    set @strsql = concat("select count(DISTINCT(tid)) from ugc_audit_workspace   where ", @uid_str);
    prepare stmtsql from @strsql;
    execute stmtsql;
    deallocate prepare stmtsql;
      
    set @start_pos = i_pagesize*(i_pagecurrent-1); 
    set @strsql = concat("select ugc_video.tid,ugc_video.uid,ugc_video.title,ugc_video.tags,ugc_video.channel,ugc_video.step,ugc_video.status,ugc_file.funshion_id, ugc_video.ctime,
        ugc_file.duration,auth_user.username,ugc_video.vid,ugc_video.priority
        from ugc_video, ugc_file, ugc_audit_workspace, auth_user where ugc_video.step='audit' and ugc_video.status=0 ",@uid_str, " and  ugc_video.tid=ugc_file.tid and ugc_audit_workspace.tid=ugc_video.tid and auth_user.id = ugc_audit_workspace.uid ORDER BY  ugc_video.priority desc, ugc_video.ctime desc  limit ",@start_pos,",",i_pagesize);
    prepare stmtsql from @strsql; 
    execute stmtsql;
    deallocate prepare stmtsql; 
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_page_get_pending_tasks` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_page_get_pending_tasks`(IN `i_pagecurrent` int,  IN `i_pagesize` int,  IN `i_uid` int,  IN `i_searchstr`  varchar(1024)  CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    if i_uid <> -1 THEN
        set   @uid_str = concat(" and ugc_audit_workspace.uid=",i_uid);
    ELSE
        set @uid_str = "";
    end if;

    set @strsql = concat("select count(DISTINCT(ugc_video.tid)) from ugc_video,ugc_audit_workspace   where  ugc_video.step='audit' and ugc_video.status=0  and ugc_video.tid=ugc_audit_workspace.tid ", @uid_str," ", i_searchstr);
    prepare stmtsql from @strsql; 
    execute stmtsql; 
    deallocate prepare stmtsql;
      
    set @start_pos = i_pagesize*(i_pagecurrent-1); 
    set @strsql = concat("select DISTINCT ugc_video.tid,ugc_video.uid,ugc_video.title,ugc_video.tags,ugc_video.channel,ugc_video.step,ugc_video.status,ugc_file.funshion_id, ugc_audit_workspace.time,
        ugc_file.duration,auth_user.username,ugc_video.vid,ugc_video.priority
        from ugc_video, ugc_file, ugc_audit_workspace, auth_user where ugc_video.step='audit' and ugc_video.status=0 ",@uid_str, " ", i_searchstr ," and  ugc_video.tid=ugc_file.tid and ugc_audit_workspace.tid=ugc_video.tid and auth_user.id = ugc_audit_workspace.uid ORDER BY ugc_video.priority desc , ugc_video.ctime desc limit ",@start_pos,",",i_pagesize);
    prepare stmtsql from @strsql; 
    execute stmtsql;
    deallocate prepare stmtsql; 
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_page_task` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_page_task`(IN `i_pagecurrent` int,  IN `i_pagesize` int, IN `i_ifelse` varchar(1024),IN `i_cond` varchar(1024) CHARACTER SET utf8,IN `i_order` varchar(512))
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    set @pagesize = i_pagesize;
  
    if i_pagecurrent < 1 then 
        set i_pagecurrent = 1; 
    end if;

    set @strsql = concat('select ',i_ifelse,' from ',i_cond,' ',i_order,' limit ',i_pagecurrent*@pagesize-@pagesize,',',@pagesize); 
    prepare stmtsql from @strsql; 

    execute stmtsql; 

    deallocate prepare stmtsql;

    set @strsqlcount=concat('select count(1) as count from ',i_cond); 

    prepare stmtsqlcount from @strsqlcount; 
    execute stmtsqlcount; 
    deallocate prepare stmtsqlcount; 
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_page_task_v2` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_page_task_v2`(IN `i_pagecurrent` int,  IN `i_pagesize` int,IN `i_uid` int)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    set @strsql = concat("select count(*) from ugc_video where origin='forwards' and uid=",i_uid);
    prepare stmtsql from @strsql; 
    execute stmtsql; 
    deallocate prepare stmtsql;
  
    set @start_pos = i_pagesize*(i_pagecurrent-1); 
    set @strsql = concat("select tid,title,tags,description,priority,channel,step,status,ctime from ugc_video where uid=",i_uid ," AND origin='forwards' ORDER BY ctime DESC limit ",@start_pos,",",i_pagesize);
    prepare stmtsql from @strsql; 
    execute stmtsql; 
    deallocate prepare stmtsql; 
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_repair_test` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_repair_test`(t_vid varchar(128)  CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    
    create temporary table if not exists tb_tid(tid varchar(128))ENGINE=InnoDB DEFAULT CHARSET=gbk;
    insert into tb_tid(tid) select tid from ugc_audit_workspace where uid = 46 limit 1000;
    update  ugc_audit_workspace set uid = 18  where  tid in (select tid from tb_tid);
    drop table  if exists tb_tid;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_set_distribute_start` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_set_distribute_start`(IN i_infohash VARCHAR(64)  CHARACTER SET utf8, IN i_tid_list_values VARCHAR(10240) CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    SET @exsted_value = 1;
    
    UPDATE ugc_dat SET flag = 1, sendmacros_time = NOW() WHERE dat_id = i_infohash;
    
    SET @strsql = CONCAT("update ugc_video set step = 'distribute', status = 1 where tid in ", i_tid_list_values);
    PREPARE stmtsql FROM @strsql;
    EXECUTE   stmtsql;
    
    SELECT @exsted_value;
    COMMIT;
 END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_set_package_fail` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_set_package_fail`(IN i_tid_list_values VARCHAR(10240) CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    SET @exsted_value = 1;
    
    SET @strsql = CONCAT("update ugc_video set step = 'mpacker', status = 2 where tid in", i_tid_list_values);
    PREPARE stmtsql FROM @strsql;
    EXECUTE   stmtsql;
    
    SELECT @exsted_value;
    COMMIT;
 END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_set_package_start` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_set_package_start`(IN i_tid VARCHAR(128)  CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    UPDATE ugc_video SET step='mpacker', STATUS=0 WHERE tid=i_tid;
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_set_transcode_fail` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_set_transcode_fail`(IN i_tid VARCHAR(128)  CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    UPDATE ugc_video SET  step='transcode', STATUS=2 WHERE tid=i_tid;
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_statics_audit_info` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_statics_audit_info`(IN i_begin_time varchar(128)  CHARACTER SET utf8, IN i_end_time varchar(128)  CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    declare done int;
    declare t_uid int;
    declare t_success_num int;
    declare t_fail_num int;
    declare t_total_num int;
    declare t_username varchar(128);
    declare t_all_total_num int;
    DECLARE rs_cursor CURSOR  FOR 
        select uid from ugc_audit_log  where  time BETWEEN  i_begin_time and  i_end_time group by uid;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done=1;
    
    open rs_cursor;
   
    create temporary table if not exists tb_statics(uid int primary key, username varchar(128),  success_num int, fail_num int, total_num int);
    set t_all_total_num = 0;

    START TRANSACTION;
    cursor_loop:loop

        FETCH rs_cursor into t_uid;
        if done=1 THEN
            LEAVE cursor_loop;
        end if;
       
        set t_success_num = (select count(*) from ugc_audit_log  where flag=1 and uid=t_uid and  time BETWEEN  i_begin_time and  i_end_time);
        set t_fail_num = (select count(*) from ugc_audit_log  where flag=0 and uid=t_uid and  time BETWEEN  i_begin_time and  i_end_time);
        set t_total_num = t_success_num + t_fail_num;
        set t_username = (select username from auth_user where id = t_uid);
        insert into tb_statics(uid, username, success_num, fail_num, total_num) values(t_uid, t_username,t_success_num, t_fail_num, t_total_num);
        set t_all_total_num = t_all_total_num + t_total_num;

    END loop cursor_loop;

    select * from tb_statics;
    select  t_all_total_num;
    drop table  if exists tb_statics;
    CLOSE rs_cursor; 

    COMMIT;
 
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_statics_audit_info_v2` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_statics_audit_info_v2`(IN `i_pagecurrent` int,  IN `i_pagesize` int,  IN `i_begin_time` varchar(128)  CHARACTER SET utf8, IN `i_end_time` varchar(128)  CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    declare done int;
    declare t_uid int;
    declare t_success_num int;
    declare t_fail_num int;
    declare t_total_num int;
    declare t_username varchar(128);
    declare t_users_counter int;
    declare t_sucess_total_num int;
    declare t_fail_total_num int;
    declare t_all_total_num int;
    DECLARE rs_cursor CURSOR  FOR 
        select DISTINCT(uid) from ugc_audit_log  where  time BETWEEN  i_begin_time and  i_end_time group by uid;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done=1;
    
    open rs_cursor;
    create temporary table if not exists tb_statics(uid int primary key, username varchar(128),  success_num int, fail_num int, total_num int);

    set t_users_counter = 0;
    set t_sucess_total_num = 0;
    set t_fail_total_num = 0;
    set t_all_total_num = 0;
   
    START TRANSACTION;

    cursor_loop:loop

        FETCH rs_cursor into t_uid;
        if done=1 THEN
           LEAVE cursor_loop;
        end if;
       
        set t_success_num = (select count(*) from ugc_audit_log  where flag=1 and uid=t_uid and  time BETWEEN  i_begin_time and  i_end_time);
        set t_fail_num = (select count(*) from ugc_audit_log  where flag=0 and uid=t_uid and  time BETWEEN  i_begin_time and  i_end_time);

        set t_total_num = t_success_num + t_fail_num;

        set t_username = (select username from auth_user where id = t_uid);

        insert into tb_statics(uid, username, success_num, fail_num, total_num) values(t_uid, t_username,t_success_num, t_fail_num, t_total_num);
     
        set t_users_counter = t_users_counter + 1;
        set t_sucess_total_num = t_sucess_total_num + t_success_num;
        set t_fail_total_num = t_fail_total_num + t_fail_num;
        set t_all_total_num = t_all_total_num + t_total_num;

    END loop cursor_loop;

    select t_users_counter;

    set @start_pos = i_pagesize*(i_pagecurrent-1); 
    set @strsql = concat("select * from tb_statics  limit ",@start_pos,",",i_pagesize);
    prepare stmtsql from @strsql;
    execute stmtsql;
    deallocate prepare stmtsql; 
    select  t_sucess_total_num, t_fail_total_num, t_all_total_num;
    drop table  if exists tb_statics;
    CLOSE rs_cursor; 
    COMMIT;
 
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_statics_dat_sort` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_statics_dat_sort`(IN `i_begin_time` varchar(512), IN `i_end_time` varchar(512), IN `i_pagecurrent` int,  IN `i_pagesize` int)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    set @strsql = concat("select count(*)  from ugc_dat where distribution_time BETWEEN '",i_begin_time  ,"' AND  '",i_end_time, "'");
    prepare stmtsql from @strsql; 
    execute stmtsql; 
    deallocate prepare stmtsql;

    set @strsql = concat("select count(ugc_fid_map.funshion_id)  from ugc_dat, ugc_fid_map where ugc_dat.dat_id = ugc_fid_map.dat_id and ugc_dat.distribution_time BETWEEN '",i_begin_time  ,"' AND  '",i_end_time, "'");
    prepare stmtsql from @strsql;
    execute stmtsql;
    deallocate prepare stmtsql;

    set @start_pos = i_pagesize*(i_pagecurrent-1);
  
    set @strsql = concat("select dat_id,  distribution_time,  flag, mserver_ip, mserver_port  from ugc_dat where distribution_time BETWEEN '",i_begin_time  ,"' AND  '",i_end_time ,"' order by mserver_ip");

    prepare stmtsql from @strsql; 
    execute stmtsql; 
    deallocate prepare stmtsql; 
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_statics_details_info` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_statics_details_info`(IN `i_key` varchar(128), IN `i_type` varchar(32),IN `i_pagecurrent` int,  IN `i_pagesize` int)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    IF i_type = 'dat' THEN

        set @strsql = concat("select count(*) from ugc_fid_map, ugc_file, ugc_video, ugc_dat where ugc_fid_map.funshion_id = ugc_file.funshion_id and ugc_video.tid = ugc_fid_map.tid  and ugc_dat.dat_id=ugc_fid_map.dat_id and ugc_fid_map.dat_id = '",i_key, "'");
        prepare stmtsql from @strsql; 
        execute stmtsql;
        deallocate prepare stmtsql;
      
        set @start_pos = i_pagesize*(i_pagecurrent-1); 
        set @strsql = concat("select ugc_fid_map.dat_id, ugc_fid_map.funshion_id, ugc_video.title, ugc_video.site, ugc_video.tags, ugc_file.file_size, ugc_file.rate, ugc_file.duration, ugc_dat.mserver_ip, ugc_dat.mserver_port from ugc_fid_map, ugc_file, ugc_video, ugc_dat where ugc_fid_map.funshion_id = ugc_file.funshion_id and ugc_video.tid = ugc_fid_map.tid  and ugc_dat.dat_id=ugc_fid_map.dat_id and ugc_fid_map.dat_id = '",i_key ,"' limit ",@start_pos,",",i_pagesize);
        prepare stmtsql from @strsql; 
        execute stmtsql; 
        deallocate prepare stmtsql; 

    ELSE 
        set @strsql = concat("select count(*) from ugc_fid_map, ugc_file, ugc_video, ugc_dat where ugc_fid_map.funshion_id = ugc_file.funshion_id and ugc_video.tid = ugc_fid_map.tid  and ugc_dat.dat_id=ugc_fid_map.dat_id and ugc_fid_map.funshion_id = '",i_key, "'");
        prepare stmtsql from @strsql; 
        execute stmtsql;
        deallocate prepare stmtsql;
  
        set @start_pos = i_pagesize*(i_pagecurrent-1); 
        set @strsql = concat("select ugc_fid_map.dat_id, ugc_fid_map.funshion_id, ugc_video.title, ugc_video.site, ugc_video.tags, ugc_file.file_size, ugc_file.rate, ugc_file.duration, ugc_dat.mserver_ip, ugc_dat.mserver_port from ugc_fid_map, ugc_file, ugc_video, ugc_dat where ugc_fid_map.funshion_id = ugc_file.funshion_id and ugc_video.tid = ugc_fid_map.tid  and ugc_dat.dat_id=ugc_fid_map.dat_id and ugc_fid_map.funshion_id = '",i_key ,"' limit ",@start_pos,",",i_pagesize);
        prepare stmtsql from @strsql; 
        execute stmtsql; 
        deallocate prepare stmtsql; 

    END IF;
    COMMIT;
END ;;
DELIMITER ;

/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_update_audit` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_update_audit`(IN i_tid varchar(128), IN i_title varchar(256), IN i_channel varchar(512), IN i_logo varchar(1024))
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    set @exsted_value = (select 1 from ugc_video where tid = i_tid limit 1 );
    update ugc_video set title = i_title, channel = i_channel  where tid=i_tid;
    update ugc_file set logo=i_logo where tid=i_tid;
    select @exsted_value;
    COMMIT;
 END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_upload_video_task` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_upload_video_task`(IN `i_pagecurrent` int,  IN `i_pagesize` int,IN `i_uid` int)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    set @strsql = concat("select count(*) from ugc_video where origin='upload' and uid=",i_uid);
    prepare stmtsql from @strsql; 
    execute stmtsql; 
    deallocate prepare stmtsql;
  
  
    set @start_pos = i_pagesize*(i_pagecurrent-1); 
    set @strsql = concat("select tid,title,tags,description,priority,channel,step,status,ctime from ugc_video where uid=",i_uid ," AND origin='upload' ORDER BY ctime DESC limit ",@start_pos,",",i_pagesize);
    prepare stmtsql from @strsql; 
    execute stmtsql; 
    deallocate prepare stmtsql; 
    COMMIT;
END ;;
DELIMITER ;

/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_verify_video_base` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ugc_kaifa`@`%` PROCEDURE `proc_verify_video_base`(IN i_tid varchar(128)  CHARACTER SET utf8, IN i_state varchar(64)  CHARACTER SET utf8,IN i_ip varchar(64) CHARACTER SET utf8, IN i_port varchar(32)  CHARACTER SET utf8)
    SQL SECURITY INVOKER
BEGIN
    START TRANSACTION;
    set @exsted_value = (select 1 from ugc_video where tid = i_tid limit 1 );
    if @exsted_value = 1 and i_state = 'success' THEN
        update ugc_video set ip = i_ip, port = i_port, step = 'transcode' , status = 1, mtime=now()  where tid=i_tid;
    end if;
    select @exsted_value;
    COMMIT;
 END ;;
DELIMITER ;




-- Dump completed on 2014-03-26 15:21:21
