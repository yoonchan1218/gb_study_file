package exceptionTest;

public class Chatting {
	
	public void chat(String message) {
		if(message.contains("바보")) {
//			사용자가 비속어를 사용하면 게임을 튕기게 할 것인가?
//			System.out.println("비속어가 감지되어 프로그램을 종료합니다.");
//			throw new BadWordException("비속어 감지: Chatting.java (9)");
			
//			사용자가 비속어를 사용하면 안내 메세지가 나오게 할 것인가?
			try {
				throw new BadWordException();
			} catch (BadWordException e) {
				message = "사랑해";
			}
		}
		System.out.println(message);
	}
	
	
	public static void main(String[] args) {
		new Chatting().chat("바보니?");
	}
}
