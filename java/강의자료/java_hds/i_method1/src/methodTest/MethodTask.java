package methodTest;

public class MethodTask {
//	1 ~ 10까지 println()으로 출력하는 메소드
	void print1To10(){
		for (int i = 0; i < 10; i++) {
			System.out.println(i + 1);
		}
	}
//	"홍길동"을 n번 println()으로 출력하는 메소드
	void printHong(int n){
		for (int i = 0; i < n; i++) {
			System.out.println("홍길동");
		}
	}
	
//	이름을 n번 println()으로 출력하는 메소드
	void printName(String name, int n){
		for (int i = 0; i < n; i++) {
			System.out.println(name);
		}
	}
	
//	세 정수의 뺄셈 메소드
	int subtract(int number1, int number2, int number3) {
		return number1 - number2 - number3;
	}
	
//	1 ~ n까지의 합을 구해주는 메소드
	int getTotalFrom1(int end) {
		int result = 0;
		for (int i = 0; i < end; i++) {
			result += i + 1;
		}
		
		return result;
	}
	
//	두 정수의 나눗셈 후 몫과 나머지 두 개를 구해주는 메소드
	void divide(int number1, int number2, int[] arResult) {
		if(number2 != 0) {
			arResult[0] = number1 / number2;
			arResult[1] = number1 % number2;
		}
	}
//	1 ~ 100을 입력받고 짝수만 리턴하는 메소드
	int[] getEven(int[] arData){
		int[] arEven = new int[50];
		for (int i = 0; i < arEven.length; i++) {
			arEven[i] = arData[i * 2 + 1];
		}
		return arEven;
	}
	
//	5개의 정수를 입력받고 최대값과 최소값을 구해주는 메소드
	void getMaxAndMin(int[] arData, int[] arResult) {
		arResult[0] = arData[0];
		arResult[1] = arData[0];
		
		for (int i = 1; i < arData.length; i++) {
			if(arResult[0] < arData[i]) {
				arResult[0] = arData[i];
			}
			if(arResult[1] > arData[i]) {
				arResult[1] = arData[i];
			}
		}
	}
//	void change(int[] data) {
//		data[0] = 10;
//	}
	
//	주문한 상품의 개수와 개별 가격, 할인 쿠폰으로 총 주문 가격을 구하는 메소드
//  pay(3, 3000, 1000) == 8000	
	int pay(int count, int price, int coupon) {
		return count * price - coupon;
	}
	
//	주문한 상품의 개수와 개별 가격, 할인 쿠폰으로 총 주문 가격을 구하는 메소드
//	단, 할인 쿠폰은 여러 개 받을 수 있으며, 순차 적용하여 총 가격이 0이 되지 않도록 적용한다.
//	pay(3, 3000, new int[]{3000, 4000, 5000}) == 2000
	int pay(int count, int price, int[] arCoupon) {
		int totalPrice = count * price;
		
//		쿠폰 개수만큼 반복한다(쿠폰 하나하나 모두 총 가격에서 빼줘야 하니까)
		for (int i = 0; i < arCoupon.length; i++) {
//			적용시키지 않고 그냥 빼본다.
			int result = totalPrice - arCoupon[i];
//			빼봤더니 총 가격이 0이하다.
			if(result <= 0) {
//				더이상 반복(쿠폰 적용)할 필요가 없다.
				break;
			}
//			빼봤더니 총 가격이 0보다 크다.
			totalPrice -= arCoupon[i];
		}
		return totalPrice;
	}
	
//	문자열과 문자를 입력받고 문자가 몇 개 있는지 구하기
//	입력 예) banana, a
//	출력 예) 3
	int getCount(String str, char c) {
		int count = 0;
		for (int i = 0; i < str.length(); i++) {
			if(str.charAt(i) == c) {
				count++;
			}
		}
		
		return count;
	}
	
	public static void main(String[] args) {
		MethodTask m = new MethodTask();
		
		int result = m.getCount("banana", 'a');
		System.out.println(result);
		
//		int totalPrice = m.pay(3, 3000, 1000);
//		System.out.println(totalPrice);
		
//		int result = m.pay(3, 3000, new int[]{3000, 4000, 5000});
//		System.out.println(result);
		
//		int[] data = {20};
//		m.change(data);
//		
//		System.out.println(data[0]);
		
//		m.print1To10();
//		m.printHong(10);
//		m.printName("한동석", 10);
//		int result = m.subtract(1, 2, 3);
//		System.out.println(result);
//		int result = m.getTotalFrom1(100);
//		System.out.println(result);
		
//		int[] arResult = new int[2];
//		m.divide(10, 3, arResult);
//		
//		System.out.println(arResult[0]);
//		System.out.println(arResult[1]);
		
//		int[] arData = new int[100];
//		int[] arEven = null;
//		
//		for (int i = 0; i < arData.length; i++) {
//			arData[i] = i + 1;
//		}
//		
//		arEven = m.getEven(arData);
//		
//		for (int i = 0; i < arEven.length; i++) {
//			System.out.println(arEven[i]);
//		}
//		
//		int[] arData = {3, 5, 2, 1, 7};
//		int[] arResult = new int[2];
//		m.getMaxAndMin(arData, arResult);
//		
//		System.out.println(arResult[0]);
//		System.out.println(arResult[1]);
	}
}












