package exceptionTest;

public class Game {
//	캐릭터 이름을 입력받고,
//	"멍청이", "바보", "똥개"가 포함된 이름에 예외를 발생시켜
//	사용자에게 경고 메세지를 출력해준다.
//	※ 강제 종료하지 않는다.
	
//	출력 종류 예시
//	종류1: 캐릭터명: 홍길동
//	종류2: 사용할 수 없는 닉네임입니다.
	public void checkNickname(String nickname) throws NicknameException {
		String[] arName = {"멍청이", "바보", "똥개"};
		
		for (int i = 0; i < arName.length; i++) {
			if(nickname.contains(arName[i])) {
				throw new NicknameException();
			}
		}
	}
	
	public static void main(String[] args) {
		Game game = new Game();
		String nickname = "나는똥개전사";
		try {
			game.checkNickname(nickname);
			System.out.println("캐릭터명: " + nickname);
		} catch (NicknameException e) {
			System.out.println("사용할 수 없는 닉네임입니다.");
		}
	}
	
	
}














