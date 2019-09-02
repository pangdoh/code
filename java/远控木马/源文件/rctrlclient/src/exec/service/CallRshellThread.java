package exec.service;

public class CallRshellThread implements Runnable{
    private String host;
    private int port;

    public CallRshellThread(String host,int port) {
        this.host = host;
        this.port = port;
    }

    @Override
    public void run() {
        new CallExec().rShell(host, port);
    }
}
