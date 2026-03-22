package abstractTest;

public abstract class Electronics {
	
//	강제
	public abstract void on();
	
//	선택
	public void printProduct() {
		System.out.println("전자 제품");
	}
	
//	불가
	public final void sos() {
		System.out.println("긴급 전화 119 연락");
	}
}
