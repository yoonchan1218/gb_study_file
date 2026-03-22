<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>
   <form action="ex05" method="post" name="form"> 
      <input type="text" name="id" placeholder="아이디 입력" >
      <input type="text" name="password" placeholder="비밀번호 입력" >
      <button>전송</button>
   </form>
</body>
<script>
const id = form.id;
const password = form.password;
const button = password.nextElementSibling;


</script>
</html>