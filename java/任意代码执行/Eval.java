package exec.service;

import java.io.*;
import java.net.Socket;

/**
 * 代码执行
 */
public class CallExec {

    /**
     * 代码执行
     *
     * @param code
     * @return 输出信息（如打印信息）
     */
    public String eval(String code) {
        //设置临时存储路径
        String tempPath;
        if (System.getProperty("os.name").toLowerCase().startsWith("win")) {
            tempPath = "D:\\temp0099990011\\";
        } else {
            tempPath = "/tmp/temp0099990011/";
        }

        File dir = new File(tempPath);
        if (dir.exists() && dir.isDirectory()) {
        } else {
            dir.mkdir();
        }

        //生成java文件
        String s = "class Temp{";
        s += "public static void main(String[] args) throws Exception {";
        s += code;
        s += "}}";
        File f = new File(tempPath.concat("Temp.java"));
        PrintWriter pw = null;
        try {
            pw = new PrintWriter(new FileWriter(f));
            pw.println(s);
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                pw.close();
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        }

        //动态编译
        execmd("javac ".concat(tempPath).concat("Temp.java"));

        //执行代码
        String result = execmd("java -cp ".concat(tempPath).concat(" Temp"));

        //删除临时存储路径
        File[] files = dir.listFiles();
        for (File file : files) {
            file.delete();
        }
        dir.delete();

        return result;
    }

}
