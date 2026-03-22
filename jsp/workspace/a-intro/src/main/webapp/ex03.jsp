<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>EX03</title>
</head>
<body>
	<form action="ex03" method="post" name="fruitForm">
		<input type="text" name="fruitName" placeholder="과일 이름">
		<input type="text" name="fruitPrice" placeholder="과일 가격">
		<input type="button" value="전송">
	</form>
</body>
<script>
	const button = document.querySelector("input[type=button]");
	const fruitName = fruitForm.fruitName;
	const fruitPrice = fruitForm.fruitPrice;
	const tempBorder = fruitName.style.border;
	const checks = [false, false];
	
	fruitName.addEventListener("blur", (e) => {
		if(!e.target.value){
			e.target.style.border = "1px solid red";
			checks[0] = false;
			return;
		}
		
		e.target.style.border = tempBorder;
		checks[0] = true;
		
	});
	
	fruitPrice.addEventListener("blur", (e) => {
		if(!e.target.value){
			e.target.style.border = "1px solid red";
			checks[1] = false;
			return;
		}
		
		e.target.style.border = tempBorder;
		checks[1] = true;
		
	});
	
	button.addEventListener("click", (e) => {
		if(checks[0] && checks[1]){
			fruitForm.submit();
		}
	});
	
	
</script>
</html>

















