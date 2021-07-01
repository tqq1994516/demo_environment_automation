#! /bin/bash 
port=10115
PID=`ps -ef | grep $port | grep -v grep | awk '{print $2}'`
export JAVA_HOME=/home/software/jdk1.8.0_121
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export PATH=$JAVA_HOME/bin:$PATH
if [ -n "$PID" ];then
    echo "`date +%F%H%M%S` testReport service $PID is running, stop it"
    kill -9 $PID
fi
echo "`date +%F%H%M%S` start clear out [*.html] and [*.attach] and [*.json] and [*.log] files at
demo_environment_automation/result/ and demo_environment_automation/html/ and demo_enviroment_automation/logs/ ten days ago"
find /root/ceshibu/demo_environment_automation/result -mtime +10 -name "*-attachment.attach" -exec rm -rf {} \;
find /root/ceshibu/demo_environment_automation/result -mtime +10 -name "*-result.json" -exec rm -rf {} \;
find /root/ceshibu/demo_environment_automation/html -mtime +10 -name "*.html" -exec rm -rf {} \;
find /root/ceshibu/demo_environment_automation/logs -mtime +10 -name "*.log" -exec rm -rf {} \;
echo "clear over"
source /root/anaconda3/bin/activate demo_env_autotest
cd /root/ceshibu/demo_environment_automation
echo "`date +%F%H%M%S` start running test"
python test_main.py
echo "`date +%F%H%M%S` start generate allure report"
/root/ceshibu/demo_environment_automation/framework/allure-2.13.9/bin/allure generate ./result/ -o ./report/ --clean
echo "`date +%F%H%M%S` start to startup report service.port:$port"
nohup /root/ceshibu/demo_environment_automation/framework/allure-2.13.9/bin/allure open -h 0.0.0.0 -p $port ./report

#以下为定时任务设置
#demo_env_autotest_task
#00 23 * * * /root/ceshibu/demo_env_sh.sh
