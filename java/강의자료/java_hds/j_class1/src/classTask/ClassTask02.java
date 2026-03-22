package classTask;

// 회원의 정보를 저장할 클래스 선언
// 아이디, 비밀번호
// 저장소에 있는 아이디는 항상 "test"이고 비밀번호는 항상 "1234"이다.

// 아이디 중복검사
// 전달받은 아이디가 이미 있는 아이디인지 boolean으로 리턴한다.

// 로그인
// 로그인 성공 혹은 실패에 대한 결과를 boolean으로 리턴한다.
class Member {
	String id;
	String password;
	
	public Member() {;}

	public Member(String id, String password) {
		this.id = id;
		this.password = password;
	}
	
	static boolean checkId(String id) {
		return id.equals("test");
	}
	
	static boolean login(String id, String password) {
		return id.equals("test") && password.equals("1234");
	}
	
}

public class ClassTask02 {
	public static void main(String[] args) {
		String id = "test";
		String password = "1234";
		
		boolean isDup = Member.checkId(id);
		System.out.println(isDup);
		
		boolean isMember = Member.login(id, password);
		System.out.println(isMember);
	}
}






