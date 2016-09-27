#include <openssl/md5.h>  
#include <sstream>
#include <iostream>  
#include <cstdio>  
#include <iomanip>  
#include <stdlib.h> 

#include <magic.h>

#include "client/gridfs.h"
//#include "client/oid.h"
#include "mongo_processor.h"

mongo_processor::mongo_processor(void){}
mongo_processor::~mongo_processor(void){}

int mongo_processor::init()
{
    std::string errmsg;
    mongo::DBClientConnection* mongo_ins;
    //mongo::DBClientBase* mongo_ins;
    {
        //build recommender's mongo
        mongo_ins=new mongo::DBClientConnection(true);
        if(!mongo_ins->connect("192.168.16.113:30000",errmsg))
        {
            cout<<"mongo connect error"<<endl;
            return -1;
        }
    }

    //GridFS (DBClientBase &client, const std::string &dbName, const std::string &prefix="fs")
    //GridFS
    //mongo::GridFS * fs_ins = new mongo::GridFS(mongo_ins,"test");
    //mongo::GridFile gf1;
    mongo::GridFS * fs_ins1;
    try
    {
    std::string name = "test";
    mongo::GridFS * fs_ins = new mongo::GridFS(*mongo_ins,name);
    fs_ins1 = new mongo::GridFS(*mongo_ins,name);
    //GridFile    findFile (Query query) const
    //mongo::GridFile gf = fs_ins->findFile("{'vid': '888'}");
    //mongo::GridFile gf = fs_ins->findFile("55c47d7f8d654269765a3cea");
    //fs_ins->findFile("{'vid': '888','width':'120','height':'240'}");
    mongo::BSONObjBuilder b;
    //b << "vid" << "888" << "width" << '120';
    //b << "vid" << "888"<<"width"<<"120"<<"height"<<"240";
    //b << "vid" << "888"<<"length"<<11;
    b << "oid" << "123"<<"width"<<120<<"height"<<240;
    //b << "vid" << "123"<<"width"<<"1200";
    //b<<"files_id"<<"55c854a08d65422435db1d63";
    mongo::BSONObj p = b.obj();
    mongo::GridFile gf = fs_ins->findFile(p);
    
    if (gf.exists() )
    {
        cout<<"find file"<<endl;
        cout<<"chuncsize:"<<gf.getChunkSize()<<endl;
        cout<<"filename:"<<gf.getFilename()<<endl;
        cout<<"contenttype:"<<gf.getContentType()<<endl;
        cout<<"md5:"<<gf.getMD5()<<endl;
        cout<<"contentlength:"<<gf.getContentLength()<<endl;
        cout<<"chunk num:"<<gf.getNumChunks()<<endl;

        mongo::BSONElement ele = gf.getFileField("height");
        //mongo::BSONElement ele = gf.getFileField("files_id");
        cout<<"ele size:"<<ele.size()<<endl;
        cout<<"filed name:"<<ele.fieldName()<<endl;
        cout<<"1"<<endl;
        cout<<"is null:"<<ele.isNull()<<endl;
        cout<<"ok:"<<ele.ok()<<endl;
        //mongo::BSONObj objfreq1=ele.Obj();
        //string aa = ele["height"].String();
        //cout<<"value:"<<ele.valuestr()<<endl;

        for(int i=0;i<gf.getNumChunks();i++)
        {
            mongo::GridFSChunk chunk = gf.getChunk(i);
            cout<<"chunck len:"<<chunk.len()<<endl;
            int clen = chunk.len();
            //cout<<"chunk data:"<<chunk.data(clen)<<endl;
            string str(chunk.data(clen),clen);
            cout<<"chunk data:"<<str.size()<<endl;
        }

        /*
        ifstream fin1("/tmp/dsc04403.jpg",ios::binary);
        string info1;
        while(!fin1.eof())
        {
            char c[1024];
            fin1.read(c,1024);
            info1.append(c,fin1.gcount());
        }
        */
        
        /*    
        cout<<"----------------"<<endl;
        mongo::BSONElement ele1 = gf.getFileField("data");
        cout<<"ele size:"<<ele1.size()<<endl;
        cout<<"filed name:"<<ele1.fieldName()<<endl;
        cout<<"1.1"<<endl;
        cout<<"is null:"<<ele1.isNull()<<endl;
        cout<<"ok:"<<ele1.ok()<<endl;
        cout<<"value:"<<ele1.valuestr()<<endl;
        cout<<"----------------"<<endl;
        */
        
        /*
        cout<<"0.5"<<endl;
        mongo::BSONObj objfreq=ele.Obj();
        cout<<"2"<<endl;
        set<string> fields1;
        objfreq.getFieldNames(fields1);
        cout<<"3"<<endl;
        cout<<"num:"<<fields1.size()<<endl;
        */

        /*
        mongo::BSONObj obj = gf.getMetadata();
        set<string> fields;
        obj.getFieldNames(fields);
        //cout<<"obj:"<<obj.toString()<<endl;
        cout<<"obj empty:"<<obj.isEmpty()<<endl;

        set<string>::const_iterator b=fields.begin(),e=fields.end();
        for(;b!=e;++b)
        {
            mongo::BSONElement value=obj.getField(*b);
            cout<<b->c_str()<<endl;
        }
        */
        //BSONElemetn
    }
    else
    {
        cout<<"not find file"<<endl;
    }
    }
    catch(exception &err)
    {   
        cout<<"err1"<<err.what()<<endl;
    }
    catch(...)
    {
        cout<<"err2"<<endl;
    }

    unsigned char md5[17]={0}; 
    MD5_CTX c;
    MD5_Init(&c);

    //ifstream fin("/tmp/t2.jpg",ios::binary);
    ifstream fin("/tmp/dsc04403.jpg",ios::binary);
    string info;
    while(!fin.eof())
    {
        char c[1024];
        fin.read(c,1024);
        //fout.write(c,fin.gcount());
        info.append(c,fin.gcount());
    }

    cout<<"flile len:"<<info.size()<<endl;
    fin.close();

    unsigned char *pData = (unsigned char *)(info.data());
    MD5_Update(&c, pData, info.size());
    MD5_Final(md5,&c);
    for(int i = 0; i < 16; i++)  
        cout << hex << setw(2) << setfill('0') << (int)md5[i]; 
    cout<<endl;
    
    
    stringstream ss; 
    for(int i = 0; i < 16; i++)
        ss<< hex << setw(2) << setfill('0') << (int)md5[i];
    string info11 = ss.str();
    cout<<info11<<endl;

    magic_t myt = magic_open(MAGIC_CONTINUE|MAGIC_ERROR/*|MAGIC_DEBUG*/|MAGIC_MIME);
    magic_load(myt,NULL);
    //printf("magic output: '%s'\n", magic_file(myt, argv[1]));
    //magic_buffer(magic_t cookie, const void *buffer, size_t length);
    //string info22 = magic_buffer(myt,(const void *)(info11.data()),info11.size());
    string info22 = magic_buffer(myt,(const void *)(info11.c_str()),info11.size());
    //magic_close(myt);

    cout<<info22<<endl;

    cout<<"----"<<endl;
    string info222 = magic_buffer(myt,(const void *)(info.c_str()),info.size());
    cout<<info222<<endl;
    cout<<"----"<<endl;

    //magic_file(myt, argv[1]));
   //info22 =  magic_file(myt, "/tmp/dsc04403.jpg");
   info22 =  magic_file(myt, "/tmp/t2.jpg");
    cout<<info22<<endl;

    char * p = NULL;
    p = new char[23134208+10];
    strncpy(p,info11.data(),info11.size());
    string info223 = magic_buffer(myt,(const void *)(p),info11.size());
    cout<<info223<<endl;
    
    magic_close(myt);

    //if (gf1.exists() )
    {
        string filename = "test1";
        string contentType = info22;
        //contentType = info222;
        cout<<"content type:"<<contentType<<endl;
        //mongo::BSONObj after = mongo::BSONObjBuilder().append( "vid" , "12345adf" ).obj();
        //string sin = after.toString();
        //BSONObj idObj = BSON("_id" << 55cabc2c37ede38962cd4c28);
        //mongo::BSONObj after = mongo::BSONObjBuilder().append( "_id" , OID("55cabc2c37ede38962cd4c28") ).obj();
        string tinfo = "123";
        //fs_ins1->storeFile(info.data(),info.size(),filename,contentType);
        //fs_ins1->storeFile(sin.data(),sin.size(),filename,contentType);
        //mongo::BSONObj tobj = fs_ins1->storeFile(tinfo.data(),tinfo.size(),filename,contentType);
        mongo::BSONObj tobj = fs_ins1->storeFile(info.data(),info.size(),filename,contentType);
        string smd5 = tobj.getStringField("md5");
        mongo::BSONElement be = tobj.getField("_id");
        cout<<"smd5--:"<<smd5<<endl;
        cout<<"_id:"<<be.toString(false)<<endl;
        cout<<"_id1:"<<be.OID().toString()<<endl;
        string soid = be.OID().toString();
        mongo::BSONObjBuilder b;
        mongo::BSONObj obj;
        //b.appendAs( obj["_id"] , "55cabc2c37ede38962cd4c28" );
        mongo::BSONObj idObj = BSON("_id" << "55cc72aea343ffbc324dccee");
        //b.append( obj["_id"] , "55cabc2c37ede38962cd4c28" );
        mongo::BSONObjBuilder file;
        file << "_id" << "55cc72aea343ffbc324dccee";
        mongo::BSONObj ret = file.obj();
        
        //mongo::BSONObj nobj = mongo::BSONObjBuilder().append( "width" , "240" ).obj();
        //mongo::BSONObj nobj1 = mongo::BSONObjBuilder().append( "$set" , nobj.toString() ).obj();
        //mongo_ins->update("test.fs.files",QUERY("_id"<<"55cabc2c37ede38962cd4c28"),nobj,true,false);
        //mongo::OID oid("55cc72aea343ffbc324dccee");
        //mongo_ins->update("test.fs.files",QUERY("_id"<<oid),nobj,true,false);
        //mongo_ins->update("test.fs.files", QUERY("_id"<<mongo::OID("55cab97fdcfc9643fd34c961")), BSON("width"<<"220"), false, false);
        //BSON( "$push" << BSON("packet" << BSON( "datetime" << "updated")));
        //mongo_ins->update("test.fs.files", QUERY("_id"<<mongo::OID(soid)), BSON("$set"<<BSON("height"<<240<<"width"<<120<<"oid"<<info11)), false, false);
        mongo_ins->update("test.fs.files", QUERY("_id"<<mongo::OID(soid)), BSON("$set"<<BSON("height"<<240<<"width"<<120<<"oid"<<info11)), false, false);
        //mongo_ins->update("test.fs.files", QUERY("_id"<<mongo::OID("55cab97fdcfc9643fd34c961")), mongo::BSONObjBuider().append( "name" , "eliot" ).obj());
        //mongo_ins->insert("test.fs.files",BSON("_id"<<mongo::OID("55cab97fdcfc9643fd34c962")<<"width"<<"220"<<"height"<<"110"));
        //mongo_ins->insert("test.fs.files",QUERY("_id"<<oid),nobj,true,false);
        //mongo_ins->update("test.fs.files",ret,nobj,true,false);
        //online_ins->update(db_table,query,nobj,true,false);
        //fs_ins1->update("test",after,nobj,true,false);
        //string sres = tobj.toString();
        //cout<<"tres:"<<sres<<endl;

    }    

    return 0;
}
