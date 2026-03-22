package classTest;

class A {
//	전역 변수(global variable)
//	프로그램 종료 시 메모리 해제
//	자동 초기화
	int data;
	
	void printData() {
//		지역 변수(local variable)
//		해당 영역이 끝날 때(닫는 중괄호 }를 만날 때)
//		직접 초기화
		int data = 10;
		
		System.out.println(data);
		System.out.println(this.data);
		System.out.println(this);
	}
}

public class ClassTest01 {
	public static void main(String[] args) {
		A a1 = new A();
		A a2 = new A();
		
		System.out.println(a1);
		a1.data = 100;
		a1.printData();
		
		System.out.println(a2);
		a2.data = 20;
		a2.printData();
		
	}
}












