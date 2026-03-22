package arrayTest;


public class ArTask {
	public static void main(String[] args) {
//		몇 칸 필요한지가 핵심!!
		
//		1 ~ 10까지 배열에 담고 출력
//		int[] arData = new int[10];
//		
//		for (int i = 0; i < arData.length; i++) {
//			arData[i] = i + 1;
//		}
//		
//		for (int i = 0; i < arData.length; i++) {
//			System.out.println(arData[i]);
//		}
		
		
//		10 ~ 1까지 중 짝수만 배열에 담고 출력
//		int[] arData = new int[5];
//		
//		for (int i = 0; i < arData.length; i++) {
//			arData[i] = (5 - i) * 2;
//		}
//		
//		for (int i = 0; i < arData.length; i++) {
//			System.out.println(arData[i]);
//		}
		
		
//		1 ~ 100까지 배열에 담은 후 홀수만 출력
//		int[] arData = new int[100];
//		
//		for (int i = 0; i < arData.length; i++) {
//			arData[i] = i + 1;
//		}
//		
//		for (int i = 0; i < arData.length; i++) {
//			if(i % 2 == 0) {
//				System.out.println(arData[i]);
//			}
//		}
		
		
//		1 ~ 100까지 배열에 담은 후 짝수의 합 출력
//		int[] arData = new int[100];
//		int total = 0;
//		
//		
//		for (int i = 0; i < arData.length; i++) {
//			arData[i] = i + 1;
//		}
//		
//		for (int i = 0; i < arData.length; i++) {
//			if(i % 2 == 1) {
//				total += arData[i];
//			}
//		}
//		
//		System.out.println(total);
		
		
//		001.png ~ 010.png를 배열에 담고 출력
//		String[] arData = new String[10];
//		
//		for (int i = 0; i < arData.length; i++) {
//			arData[i] = i + 1 + ".png";
//		}
//		
//		for (int i = 0; i < arData.length; i++) {
//			switch(arData[i].length()) {
//			case 5:
//				arData[i] = "00" + arData[i];
//				break;
//				
//			case 6:
//				arData[i] = "0" + arData[i];
//				break;
//			}
//		}
//		
//		for (int i = 0; i < arData.length; i++) {
//			System.out.println(arData[i]);
//		}
		
//		5개의 정수를 입력받고 배열에 담은 후 최대값과 최소값 출력
//		단, 같은 수는 없다고 가정한다.
//		int[] arData = new int[5];
//		int max = 0, min = 0;
//		Scanner sc = new Scanner(System.in);
//		String message = "번째 정수: ";
//		
//		for (int i = 0; i < arData.length; i++) {
//			System.out.print(i + 1 + message);
//			arData[i] = sc.nextInt();
//		}
//		
//		max = arData[0];
//		min = arData[0];
//		
//		for (int i = 1; i < arData.length; i++) {
//			if(max < arData[i]) {
//				max = arData[i];
//			}
//			if(min > arData[i]) {
//				min = arData[i];
//			}
//		}
//		
//		System.out.println("최대값 " + max);
//		System.out.println("최소값 " + min);
		
//		사용자에게 칸 수를 입력받고, 그 칸 수만큼 정수를 다시 입력받는다.
//		입력한 정수들의 평균값을 구한다.
//		Scanner sc = new Scanner(System.in);
//		int total = 0;
//		double average = 0.0;
//		int length = 0;
//		int[] arData = null;
//		String message = "몇 개의 정수를 입력하시나요?";
//		String inputMessage = "번째 정수: ";
//		
//		System.out.println(message);
//		length = sc.nextInt();
//		
//		arData = new int[length];
//		
//		for (int i = 0; i < arData.length; i++) {
//			System.out.print(i + 1 + inputMessage);
//			arData[i] = sc.nextInt();
//		}
//		
//		for (int i = 0; i < arData.length; i++) {
//			total += arData[i];
//		}
//		
//		average = total / (double)arData.length;
//		
//		System.out.println(average);
		
//		당신은 3칸 방이 있는 건물의 주인이다.
//		각 방에는 세입자가 살고 있다.
//		방마다 월세를 받아서 총 월세와 평균 월세를 구해주는 프로그램을 만들고자 한다.
//		Scanner sc = new Scanner(System.in);
//		int[] arIncome = new int[3];
//		String message = "호 월세[단위, 만원]: ";
//		int total = 0;
//		double average = 0.0;
//		
//		for (int i = 0; i < arIncome.length; i++) {
//			System.out.print(i + 1 + message);
//			arIncome[i] = sc.nextInt();
//			total += arIncome[i];
//		}
//		
//		average = (double)total / arIncome.length;
//		
//		System.out.println("총 월세: " + total);
//		System.out.println("평균 월세: " + average);
	}
}
















