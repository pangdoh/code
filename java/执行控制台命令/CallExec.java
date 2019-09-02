package exec.service;

import java.io.*;
import java.net.Socket;

/**
 * 命令执行
 */
public class CallExec {

    /**
     * 控制台命令执行
     *
     * @param cmd
     * @return 执行结果
     */
    public String execmd(String cmd) {
        String result = "";
        try {
            Process p = Runtime.getRuntime().exec(cmd);
            InputStreamReader ir = new InputStreamReader(p.getInputStream());
            LineNumberReader input = new LineNumberReader(ir);
            String line;
            while ((line = input.readLine()) != null) {
                result += line.concat("\r\n");
            }
            if (result.length() > 0) {
                result = result.substring(0, result.lastIndexOf("\r\n"));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return result;
    }


}
