
#ifndef __PATH_MANAGER_
#define __PATH_MANAGER_

#include <vector>
#include <string>

using namespace std;

class path_manager
{
	public:
		path_manager();
		~path_manager();

		int init(string& res);
		int get_file_path(long long len, std::string& path);

	private:
		float _unuse_rate;
		vector<string> _vpath;
};

#endif
