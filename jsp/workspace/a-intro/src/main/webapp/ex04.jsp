<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>EX04</title>
</head>
<body>
	<form action="ex04" method="post" name="stateForm">
		<select name="state">
			<option value="">선택</option>
			<option value="서울">서울</option>
			<option value="경기도">경기도</option>
		</select>
		<button type="button">전송</button>
	</form>
</body>
<script>
	const state = stateForm.state;
	const button = document.querySelector("button[type=button]");
	
	button.addEventListener("click", (e) => {
		if(state.value) {
			stateForm.submit();
		}
	});
	
	
</script>
</html>

















