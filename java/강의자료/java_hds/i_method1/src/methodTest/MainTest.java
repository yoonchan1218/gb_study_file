package methodTest;

public class MainTest {
//	main 메소드
//	개발자가 직접 사용하지 않고, 컴파일러가 대신 사용해준다.
	public static void main(String[] args) {
		if(args != null && args.length != 0) {
			for (int i = 0; i < args.length; i++) {
				System.out.println(args[i]);
			}
		}else {
			System.out.println("옵션 없음");
		}
	}
	
}
