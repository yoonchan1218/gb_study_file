<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>회원가입</title>
</head>
<body>
	<form action="join-ok.member" method="post">
		<input type="text" name="memberEmail" placeholder="이메일">
		<input type="password" name="memberPassword" placeholder="비밀번호">
		<input type="text" name="memberName" placeholder="이름">
		<button>회원가입</button>
	</form>
</body>
</html>