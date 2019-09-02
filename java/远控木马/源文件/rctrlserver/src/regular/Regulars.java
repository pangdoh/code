package regular;

/**
 * 对指令进行校验
 */
public class Regulars {
    //反弹shell进行校验
    public static boolean regRshell(String s){
        if(s == null || s.trim().equals("")){
            return false;
        }
        if(s.trim().indexOf(" ") < 0 && s.trim().indexOf(":") < 0){
            return false;
        }
        String[] ss = s.trim().split(" ");
        if(ss.length != 2){
            ss = s.trim().split(":");
            if(ss.length != 2){
                return false;
            }else {
                if(!(ss[0].matches("\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}") && ss[1].matches("^\\d{1,5}$"))){
                    return false;
                }
            }
        }else{
            if(!(ss[0].matches("\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}") && ss[1].matches("^\\d{1,5}$"))){
                return false;
            }
        }
        return true;
    }

}
