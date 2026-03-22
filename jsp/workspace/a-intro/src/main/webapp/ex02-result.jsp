<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>EX02 - result</title>
</head>
<body>
	<%
		String number1 = request.getParameter("number1");
		String number2 = request.getParameter("number2");
		String result = request.getParameter("result");
	%>
	<h1><%=number1%> + <%=number2%> = <%=result%></h1>
</body>
</html>


















