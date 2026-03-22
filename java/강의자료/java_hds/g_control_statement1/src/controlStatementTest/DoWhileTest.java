package controlStatementTest;

import java.util.Scanner;

public class DoWhileTest {
	public static void main(String[] args) {
		String message = "1. 통신 요금 조회\n2. 번호 변경\n3. 통신사 변경\n0. 상담사 연결";
		
		Scanner sc = new Scanner(System.in);
		int choice = 0;
		
		do {
			System.out.println(message);
			choice = sc.nextInt();
		} while(choice != 0);
	}
}
