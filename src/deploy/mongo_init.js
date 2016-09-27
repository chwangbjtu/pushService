db.msg_history.dropIndex("msgid_1");
db.msg_history.createIndex({"msgid":1}, {"unique":true});

db.msg_token_pull.dropIndex("app_name_1");
db.msg_token_pull.createIndex({"app_name":1});

db.msg_progress.dropIndex("msgid_1");
db.msg_progress.createIndex({"msgid":1}, {"unique":true});

db.msg_progress_detail.dropIndex("msgid_1");
db.msg_progress_detail.dropIndex("msgid_1_reportid_1");
db.msg_progress_detail.createIndex({"msgid":1});
db.msg_progress_detail.createIndex({"msgid":1, "reportid":1});
