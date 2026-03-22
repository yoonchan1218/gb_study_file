package exceptionTest;

import java.util.Scanner;

public class ExceptionTask {
	public static void main(String[] args) {
//		정수 입력받기
//		5칸 배열을 만들어서 해당 인덱스에 입력받은 정수를 담는다.
//		5개까지만 담을 수 있으며, 6번째 정수가 담기면 오류가 발생한다.
//		단, q를 입력하면 입력을 중단시킨다.
//		if문은 딱 한 번만 사용한다(q 입력 시 나가기)
		Scanner sc = new Scanner(System.in);
		int[] arData = new int[5];
		String message = "번째 정수: ";
		int count = 0;
		String temp = null;
		
		
		while(true) {
			System.out.print(++count + message);
			temp = sc.next();
			
			if(temp.equals("q")) {
				break;
			}
			
			try {
				arData[count - 1] = Integer.parseInt(temp);
				
			} catch(NumberFormatException e) {
				System.out.println("정수만 입력하세요!");
				count--;
				
			} catch(ArrayIndexOutOfBoundsException e) {
				System.out.println("더이상 입력하실 수 없습니다.");
				break;
				
			} catch (Exception e) {
				System.out.println("다시 시도해주세요.");
				count--;
			}
		}
		
		for (int i = 0; i < arData.length; i++) {
			System.out.println(arData[i]);
		}
	}
}















