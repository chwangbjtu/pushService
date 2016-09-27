#include<stdlib.h>
#include<string.h>
#include<errno.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include <iostream>

#include <arpa/inet.h>
#include <unistd.h>
#include <iostream>
#include <fstream>
#include <time.h>
#include <stdlib.h>

#include <pthread.h>
#include <sys/time.h>
#include <map>

//g++ main.cpp -lpthread

using namespace std;

//string buff = "GET /push?cli=aphone&ps=mid:1&mac=abc&ver=1.2.3.4&sid=1234 HTTP/1.0\r\n\r\n";
string buff = "0123456789";


#pragma pack(1)
typedef struct header
{
    unsigned short _version;
    unsigned short _type;
    unsigned int   _magic_code;
    unsigned int   _length;
    
}header_t;
#pragma pack()

unsigned int ip = 0;
unsigned int port = 0;
unsigned int psec = 1;

string sip;
string sport;
int send(unsigned int ip, unsigned short port)
{
        int sockfd;
        struct sockaddr_in dest_addr; //destnation ip info 

        if(-1==(sockfd=socket(AF_INET,SOCK_STREAM,0)))
        {
                cout<<"create error"<<endl;
                return -1;
        }

        dest_addr.sin_family = AF_INET;
        dest_addr.sin_addr.s_addr = ip;
        dest_addr.sin_port = port;

        if(-1 == connect(sockfd,(struct sockaddr*)&dest_addr,sizeof(struct sockaddr)))
        {
                cout<<"connect error"<<endl;
                return -1;
        }

        char buf1[2048]={0};

        //close(sockfd);
        //sleep(5);

        string login;
        string htbt;
        login.assign(sizeof(header_t),'\0');
        header_t * pheader = (header_t *)(login.data());
        pheader->_version = htons(1);
        pheader->_type = htons(1);
        pheader->_magic_code = 0;
        pheader->_length = 0;

        htbt.assign(sizeof(header_t),'\0');
        pheader = (header_t *)(htbt.data());
        pheader->_version = htons(1);
        pheader->_type = htons(2);
        pheader->_magic_code = 0;
        pheader->_length = 0;

        while(true)
        {
            send(sockfd,login.data(),login.size(),0);
            int n = 0;
            while(n < sizeof(header_t))
            {
                int tn = recv(sockfd,buf1,2046,0);
                if (tn > 0)
                {
                    n += tn;
                }
                else if (tn ==0 )
                {
                    cout<<"server disconnected"<<endl;
                    exit(0);
                }
                else if(tn < 0)
                {
                    continue;
                }
            }

            pheader = (header_t *)buf1;
            cout<<"r size :"<<n<<":header_t size:"<<sizeof(header_t)<<endl;
            cout<<"version:"<<ntohs(pheader->_version)<<endl;
            cout<<"type:   "<<ntohs(pheader->_type)<<endl;
            cout<<"code:   "<<ntohl(pheader->_magic_code)<<endl;
            cout<<"length:   "<<ntohl(pheader->_length)<<endl;
            sleep(10);


            send(sockfd,htbt.data(),htbt.size(),0);
            msg.clear();
            recv_msg(sockfd,msg);

            pheader = (header_t *)msg.data();
            cout<<"r size :"<<n<<endl;
            cout<<"version:"<<ntohs(pheader->_version)<<endl;
            cout<<"type:   "<<ntohs(pheader->_type)<<endl;
            cout<<"code:   "<<ntohl(pheader->_magic_code)<<endl;
            cout<<"length:   "<<ntohl(pheader->_length)<<endl;
        }

        return 0;
}

int recv_msg(int fd,string &msg)
{
            int n = 0;
            while(n < sizeof(header_t))
            {
                int tn = recv(sockfd,buf1,2046,0);
                if (tn > 0)
                {
                    n += tn;
                    msg.append(buf1, tn);
                }
                else if (tn ==0 )
                {
                    cout<<"server disconnected"<<endl;
                    exit(0);
                }
                else if(tn < 0)
                {
                    continue;
                }
            }

    return 0;
}

//a.out ip port threadnum
int main(int argc,char**argv)
{
        if ( argc != 4)
        {
                cout<<"a.out ip port threadnum"<<endl;

                return -1;
        }

        sip.assign(argv[1]);
        sport.assign(argv[2]);

        string str1 = sip;
        in_addr ipaddr1;
        memset(&ipaddr1,0,sizeof(ipaddr1));
        if(inet_pton(AF_INET,str1.c_str(),(struct in_addr*)&ipaddr1)>0)
        {   
                ip = ipaddr1.s_addr;
        }

        port = htons(atoi(sport.data()));
		cout<<__LINE__<<":"<<ip<<":"<<port<<endl;
        list<int> fds;

        for(int i=0;i<2;i++)
        {
            int fd = connect(ip,port);
            fds.push_back(fd);
        }

        while(1)
        {
                sleep(10);
        }

        return 0;
}
