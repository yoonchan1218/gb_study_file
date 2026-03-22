package exceptionTest;

import java.util.InputMismatchException;
import java.util.Scanner;

public class ExceptionTest {
	public static void main(String[] args) {
		try {
			System.out.println(10 / 0);
		} catch (ArithmeticException e) {
			System.out.println("0으로 나눌 수 없습니다.");
		} finally {
			System.out.println("반드시 실행해야 하는 문장");
		}
		
//		사용자에게 정수 1개를 입력받고 출력한다.
//		만약, 사용자가 정수가 아닌 문자열을 입력하면 런타임 오류가 발생한다.
//		이 때, 예외 처리를 사용해서 프로그램이 강제 종료되는 것을 막아본다.
//		nextInt()사용
		Scanner sc = new Scanner(System.in);
		int number = 0;
		String message = "정수: ";
		
		System.out.print(message);
		
		try {
			number = sc.nextInt();
			
		} catch(InputMismatchException e) {
			System.out.println("정수만 입력하세요.");
			
		} catch(Exception e) {
			e.printStackTrace();
		}
		
		System.out.println(number);
	}
}
















