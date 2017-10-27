#-*-coding:utf-8
from __init__ import *
from __config__ import *
def execute(params):
    ### 执行命令
    #print params
    fun = function.get(params["cmd"], help)
    ret = fun(params["param"])
    if ret == EXIT:
        return SHELL_STATUS_STOP
    return SHELL_STATUS_RUN
def tokenize(cmd):
    lines = cmd.replace('\n', '').replace('\r', '').replace('\t', ' ').split(' ')
    cmd_tokens = init_params()
    for i in range(len(lines)):
        line = lines[i]
        if i == 0:
            cmd_tokens["cmd"] = line
        else:
            if line[0:1] == "i":
                cmd_tokens["param"][line[0:1]] = line[2:].split(",")
            else:
                cmd_tokens["param"][line[0:1]] = line[2:]   
    return cmd_tokens
def shell_loop():
    status = SHELL_STATUS_RUN
    while status == SHELL_STATUS_RUN:
        ### 显示命令提示符
        sys.stdout.write('> ')
        sys.stdout.flush()
        ### 读取命令输入
        cmd = sys.stdin.readline()
        ### 切分命令输入
        params = tokenize(cmd)
        ### 执行该命令并获取新的状态
        status = execute(params)
def main(): 
  shell_loop()
if __name__ == "__main__":
  main() 