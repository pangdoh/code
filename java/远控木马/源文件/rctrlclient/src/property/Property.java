package property;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Properties;

public class Property {
    // 控制端ip
    public static String host = getProperty("host");
    // 控制端端口
    public static Integer port = Integer.parseInt(getProperty("port"));
    // 自动重连时间（毫秒）
    public static long reConnectTime = Integer.parseInt(getProperty("reConnectTime"));

    static {
        // 获取配置信息
        if(host == null || host.equals("")){
            host = "";
        }
        if(port == null || port == 0){
            port = 4321;
        }
    }

    private static String getProperty(String key){
        Properties prop = new Properties();
        InputStream in = Property.class.getResourceAsStream("/conf/rctrl.conf");
        try {
            prop.load(in);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return prop.getProperty(key);
    }
}
