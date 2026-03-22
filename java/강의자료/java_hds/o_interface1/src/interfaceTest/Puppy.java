package interfaceTest;

public class Puppy implements Animal{

	@Override
	public void showHands() {
		System.out.println("멍멍! 손을 준다.");
	}

	@Override
	public void sitDown() {
		System.out.println("멍멍! 앉는다.");
	}

	@Override
	public void poop() {
		System.out.println("멍멍! 지정된 곳에서 배변한다.");
	}

	@Override
	public void waitNow() {
		System.out.println("멍멍! 기다린다.");
	}

}







