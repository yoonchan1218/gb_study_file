package exceptionTest;

// Exception 상속: 컴파일러가 체크(컴파일 오류), try ~ catch문을 강제한다. 즉, 강제 종료 시키면 안된다!
// RuntimeException 상속: 컴파일러가 체크하지 않음. 강제 종료 시켜야한다.
public class BadWordException extends RuntimeException/*Exception*/{
	public BadWordException() {;}
	
	public BadWordException(String message) {
		super(message);
	}
}
