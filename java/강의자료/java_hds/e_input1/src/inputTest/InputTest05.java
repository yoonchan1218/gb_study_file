package inputTest;

import java.util.Scanner;

public class InputTest05 {
	public static void main(String[] args) {
//		두 정수를 입력받은 뒤 곱셈의 결과가 30보다 큰지 검사한다.
//		1. 30보다 클 때: "30보다 큽니다" 출력
//		2. 30보다 작을 때: "30보다 작습니다" 출력
//		3. 30과 같을 때는 없다고 가정한다.
		
		int number1 = 0;
		int number2 = 0;
		int result = 0;
		
		boolean condition = false;
		
		String message = "정수 2개를 입력해주세요.";
		String resultMessage1 = "30보다 큽니다."; 
		String resultMessage2 = "30보다 작습니다.";
		String resultMessage = null;
		
		Scanner sc = new Scanner(System.in);
		
		System.out.println(message);
		number1 = sc.nextInt();
		number2 = sc.nextInt();
		
		result = number1 * number2;
		
		condition = result > 30;
		
		if(condition) {
			resultMessage = resultMessage1;
			
		} else {
			resultMessage = resultMessage2;
			
		}
		
		System.out.println(resultMessage);
		
//		resultMessage = condition ? resultMessage1 : resultMessage2;
//		System.out.println(resultMessage);
		
	}
}




















