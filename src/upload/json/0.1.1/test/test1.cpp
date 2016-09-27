// =====================================================================================
// 
//       Filename:  test.cpp $Id$:
// 
//    Description:  
// 
//        Created:  10/09/2012 11:29:14 AM CST
//       Revision:  $Rev$:
//       Compiler:  g++
// 
//         Author:  liubo (lb), lb.falcons@gmail.com ($Author$:)
//        Company:  funshion
// 
// =====================================================================================

#include <iostream>
#include <string>
#include "json.h"
using namespace std;
using namespace pandaria;

int main(void)
{
    json j,k;

    j.add("test1",111);

    j.add("test2","afdadfadf");

    j.append("test3",111);
    j.append("test3",1112);

    j.append("test4","adfadfadfadfafadf");
    j.append("test4","xxxxxxxxxxxxxxxxxxxxxxadfadfadfadfafadf");

    k = j;
    j.add("test5",k);


    cout << j.to_formated_str() << endl;

    json m;
    string error_info,info=j.to_formated_str();
    bool ret = m.parse(info,error_info);
    if( ret == false )
    {
        cout << error_info << endl;
        exit(1);
    }

    cout << "parse ok" << endl;

    int r;
    cout << "test3:" << (r = m.get("test3",0,error_info)) << endl;
    if( r == -1 )
    {
        cout << error_info << endl;
    }

    cout << "test1:" << m.get("test1",0,error_info) << endl;


    string r2;
    string def("aaa");
    cout << "test2:" << (r2 = m.get("test2",def,error_info)) << endl;
    if( r2 == "" )
    {
        cout << error_info << endl;
    }

    cout << "test4:" << endl;
    json array;
    m.get("test4",array,error_info);
    vector<json> v;
    array.get_array(v);
    cout << v.size() << endl; 
    for(int i = 0; i < v.size() ; ++i )
    {
        cout << v[i].get_string()<< endl;
    }


    return 0;
}
