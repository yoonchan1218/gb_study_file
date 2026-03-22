package arrayTest;

public class ArTest {
	public static void main(String[] args) {
//		int[] arData = {2, 4, 5, 6, 8};
//		
////		System.out.println(arData);
////		System.out.println(arData[0]);
////		System.out.println(arData.length);
//		
//		for (int i = 0; i < arData.length; i++) {
//			arData[i] = 1;
//		}
//		
//		for(int i=0; i<arData.length; i++) {
//			System.out.println(arData[i]);
//		}
		
//		5칸 배열 선언 후, 5, 4, 3, 2, 1 넣고 출력
//		int[] arData = {5, 4, 3, 2, 1};
		
//		arData[0] = 5
//		arData[1] = 4
//		arData[2] = 3
//		arData[3] = 2
//		arData[4] = 1
		
//		5번 반복
//		첫 번째 반복: i = 0
//		두 번째 반복: i = 1
//		세 번째 반복: i = 2
//		네 번째 반복: i = 3
//		다섯 번째 반복: i = 4
		
//		다섯 번 반복
//		for (int i = 0; i < arData.length; i++) {
//			System.out.println(arData[i]);
//		}
		
//		int 자료형을 5칸 Heap 메모리(동적 메모리)에 할당한다.
//		각 방은 모두 초기값(0)으로 초기화 되어있다.
		int[] arData = new int[5];
		
//		arData 길이만큼 반복한다(5번 반복)
		for (int i = 0; i < arData.length; i++) {
//			각 방에 순서대로 5, 4, 3, 2, 1을 넣어준다.
			arData[i] = 5 - i;
		}
		
//		arData 길이만큼 반복한다(5번 반복)
		for (int i = 0; i < arData.length; i++) {
//			각 방에 있는 값을 순서대로 가져와서 콘솔에 출력한다.
			System.out.println(arData[i]);
		}
		
	}
}















