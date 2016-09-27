/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2014/10/28 18:59:29                          */
/*==============================================================*/


drop table if exists cat_exclude;

drop table if exists cat_list;

drop index show_id on channel_exclude;

drop table if exists channel_exclude;

drop table if exists crawler;

drop index show_id on episode;

drop index id on episode;

drop table if exists episode;

drop table if exists keyword;

drop index show_id on ordered;

drop table if exists ordered;

drop index show_id on owner;

drop index id on owner;

drop table if exists owner;

drop table if exists page;

drop table if exists send_result;

drop table if exists send_status;

drop table if exists site;

drop table if exists task;

/*==============================================================*/
/* Table: cat_exclude                                           */
/*==============================================================*/
create table cat_exclude
(
   id                   int not null auto_increment,
   cat_name             varchar(64),
   primary key (id)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

/*==============================================================*/
/* Table: cat_list                                              */
/*==============================================================*/
create table cat_list
(
   id                   int not null auto_increment,
   cat_name             varchar(64),
   url                  varchar(256),
   site_name            varchar(32),
   primary key (id)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

/*==============================================================*/
/* Table: channel_exclude                                       */
/*==============================================================*/
create table channel_exclude
(
   id                   int not null auto_increment,
   show_id              varchar(32),
   user_name            varchar(128),
   url                  varchar(256),
   primary key (id)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

/*==============================================================*/
/* Index: show_id                                               */
/*==============================================================*/
create unique index show_id on channel_exclude
(
   show_id
);

/*==============================================================*/
/* Table: crawler                                               */
/*==============================================================*/
create table crawler
(
   spider_id            int not null,
   spider_name          varchar(32),
   primary key (spider_id)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

/*==============================================================*/
/* Table: episode                                               */
/*==============================================================*/
create table episode
(
   id                   bigint not null auto_increment,
   video_id             int,
   show_id              varchar(32),
   owner_show_id        varchar(32),
   title                varchar(256),
   category             varchar(64),
   tag                  varchar(256),
   played               bigint,
   upload_time          datetime,
   create_time          datetime,
   update_time          datetime,
   spider_id            int,
   url                  varchar(256),
   site_id              int,
   thumb_url            varchar(256),
   description          text,
   stash                bool default 0,
   primary key (id),
   key AK_Key_2 (create_time),
   key AK_Key_3 (upload_time),
   key AK_Key_4 (played),
   key AK_Key_5 (site_id),
   key AK_Key_6 (stash),
   key AK_Key_7 (spider_id)
)
engine = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

/*==============================================================*/
/* Index: id                                                    */
/*==============================================================*/
create unique index id on episode
(
   id
);

/*==============================================================*/
/* Index: show_id                                               */
/*==============================================================*/
create unique index show_id on episode
(
   show_id
);

/*==============================================================*/
/* Table: keyword                                               */
/*==============================================================*/
create table keyword
(
   id                   int not null auto_increment,
   keyword              varchar(64),
   type                 varchar(8),
   user                 varchar(32),
   site_id              int,
   primary key (id)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

/*==============================================================*/
/* Table: ordered                                               */
/*==============================================================*/
create table ordered
(
   show_id              varchar(32) not null,
   user                 varchar(32),
   ctime                datetime,
   disable              bool,
   audit                bool,
   primary key (show_id)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

/*==============================================================*/
/* Index: show_id                                               */
/*==============================================================*/
create unique index show_id on ordered
(
   show_id
);

/*==============================================================*/
/* Table: owner                                                 */
/*==============================================================*/
create table owner
(
   id                   int not null auto_increment,
   owner_id             int,
   show_id              varchar(32),
   user_name            varchar(128),
   intro                text,
   played               bigint,
   fans                 int,
   vcount               int,
   pcount               int,
   create_time          datetime,
   update_time          datetime,
   spider_id            int,
   aka                  varchar(32),
   url                  varchar(256),
   site_id              int,
   primary key (id)
)
engine = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

/*==============================================================*/
/* Index: id                                                    */
/*==============================================================*/
create unique index id on owner
(
   id
);

/*==============================================================*/
/* Index: show_id                                               */
/*==============================================================*/
create unique index show_id on owner
(
   show_id
);

/*==============================================================*/
/* Table: page                                                  */
/*==============================================================*/
create table page
(
   id                   int not null auto_increment,
   url                  varchar(1024),
   site_id              int,
   ctime                datetime,
   user                 varchar(32),
   primary key (id)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

/*==============================================================*/
/* Table: send_result                                           */
/*==============================================================*/
create table send_result
(
   show_id              varchar(32) not null,
   status_id            int default NULL,
   create_time          datetime default CURRENT_TIMESTAMP,
   update_time          datetime default CURRENT_TIMESTAMP,
   primary key (show_id),
   key AK_Key_2 (status_id)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

/*==============================================================*/
/* Table: send_status                                           */
/*==============================================================*/
create table send_status
(
   status_id            int not null,
   status               varchar(16),
   primary key (status_id)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

/*==============================================================*/
/* Table: site                                                  */
/*==============================================================*/
create table site
(
   site_id              int not null,
   site_name            varchar(32),
   site_code            varchar(32),
   primary key (site_id)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

/*==============================================================*/
/* Table: task                                                  */
/*==============================================================*/
create table task
(
   task_id              int not null auto_increment,
   data_count           int,
   begin_time           datetime,
   end_time             datetime,
   primary key (task_id)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;

alter table episode add constraint FK_episode_crawler foreign key (spider_id)
      references crawler (spider_id) on delete set null on update cascade;

alter table episode add constraint FK_episode_site foreign key (site_id)
      references site (site_id) on delete set null on update cascade;

alter table keyword add constraint FK_Reference_6 foreign key (site_id)
      references site (site_id) on delete restrict on update restrict;

alter table ordered add constraint FK_ordered_owner foreign key (show_id)
      references owner (show_id) on delete restrict on update cascade;

alter table owner add constraint FK_owner_crawler foreign key (spider_id)
      references crawler (spider_id) on delete restrict on update restrict;

alter table owner add constraint FK_owner_site foreign key (site_id)
      references site (site_id) on delete restrict on update restrict;

alter table page add constraint FK_Reference_7 foreign key (site_id)
      references site (site_id) on delete restrict on update restrict;

alter table send_result add constraint FK_Reference_8 foreign key (status_id)
      references send_status (status_id) on delete restrict on update restrict;

