#include <string>
#include <fstream>
#include <cstdlib>
#include <iostream>
#include <windows.h>
using namespace std;
int main()
{
    SetConsoleOutputCP(65001);
    cout << "正在检测运行环境，请稍候..." << endl;
    cout << "------------------------------" << endl;
    int check_python = system("py --version >nul 2>&1");
    if (check_python != 0)
    {
        check_python = system("python --version >nul 2>&1");
    }
    if (check_python != 0)
    {
        cout << "错误：检测到系统未安装 Python 3.6 或以上版本！" << endl;
        cout << "是否尝试自动为您安装 Python？(输入 Y/N):";
        char c1;
        cin >> c1;
        cin.ignore();
        if (c1 == 'Y' || c1 == 'y')
        {
            cout << "正在尝试自动安装 Python，请稍候..." << endl;
            int install_result = system("winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements");
            if (install_result != 0)
            {
                cout << "自动安装失败，正在为您打开 Python 官网下载页面..." << endl;
                system("start https://www.python.org/downloads/");
            }
            else
            {
                cout << "安装成功！由于环境变量刷新延迟，请关闭此窗口并重新运行本程序。" << endl;
            }
            cout << "\n按任意键退出..." << endl;
            system("pause >nul");
            return 0;
        }
        else
        {
            cout << "已取消。程序退出。" << endl;
            cout << "\n按任意键退出..." << endl;
            system("pause >nul");
            return 0;
        }
    }
    string py_cmd = (system("py --version >nul 2>&1") == 0) ? "py" : "python";
    string check_cmd = py_cmd + " -c \"import requests\" >nul 2>&1";
    int check_requests = system(check_cmd.c_str());
    if (check_requests != 0)
    {
        cout << "错误：检测到缺少 requests 库" << endl;
        cout << "是否安装 requests 库？(输入 Y/N):";
        char c2;
        cin >> c2;
        cin.ignore();
        if (c2 == 'Y'||c2 == 'y')
        {
            string install_cmd = py_cmd + " -m pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple";
            system(install_cmd.c_str());
            cout << "成功：安装结束！" << endl;
            cout << "------------------------------" << endl;
        }
        else
        {
            cout << "已取消。程序退出。" << endl;
            cout << "\n按任意键退出..." << endl;
            system("pause >nul");
            return 0;
        }
    }
    else
    {
        cout << "[提示] 依赖检测通过，准备启动程序..." << endl;
        cout << "------------------------------" << endl;
    }
    ifstream f("main.py");
    if (!f.good())
    {
        cout << "错误：未找到 main.py，请确保该程序与 main.py 放在同一目录下！" << endl;
        cout << "\n按任意键退出..." << endl;
        system("pause >nul");
        return 1;
    }
    f.close();
    string run_cmd = py_cmd + " main.py";
    system(run_cmd.c_str());
    cout << "\n------------------------------" << endl;
    cout << "程序运行结束。按任意键关闭窗口..." << endl;
    system("pause >nul");
    return 0;
}