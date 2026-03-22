package bank;

public class Shinhan extends Bank{
//	신한 은행 고객들은 아래의 입금 서비스로만 이용한다.
//	고객이 입금할 금액을 전달한다.
	@Override
	public void deposit(int money) {
//		전달한 금액의 절반을 날린다.
		money /= 2;
//		기존 입금 서비스에 수정된 금액을 전달하여 입금을 처리한다.
		super.deposit(money);
	}
}
