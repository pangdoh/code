package exec.service;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class Eval {
    public String exeJava(String code,String fileName){
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
        if(code.startsWith("package")){
            code = code.substring(code.indexOf("\n") + 1);
        }
        String s = code;
        File f = new File(tempPath.concat(fileName));
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

        CallExec ca = new CallExec();
        //动态编译
        ca.execmd("javac ".concat(tempPath).concat(fileName));

        //执行代码
        String result = ca.execmd("java -cp ".concat(tempPath).concat(" ").concat(fileName.substring(0,fileName.lastIndexOf("."))));

        //删除临时存储路径
        File[] files = dir.listFiles();
        for (File file : files) {
            file.delete();
        }
        dir.delete();

        return result;
    }

    public String exeClass(String code,String fileName){
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
        String s = code;
        File f = new File(tempPath.concat(fileName));
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

        CallExec ca = new CallExec();

        //执行代码
        String result = ca.execmd("java -cp ".concat(tempPath).concat(" ").concat(fileName.substring(0,fileName.lastIndexOf("."))));

        //删除临时存储路径
        File[] files = dir.listFiles();
        for (File file : files) {
            file.delete();
        }
        dir.delete();

        return result;
    }
}
