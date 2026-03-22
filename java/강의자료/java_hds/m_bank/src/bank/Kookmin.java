package bank;

public class Kookmin extends Bank {
	@Override
	public void withdraw(int money) {
//		출금할 금액에서 수수료를 포함시킨다.
		money *= 1.5;
//		출금할 금액에서 수수료가 포함된 금액을 출금 처리한다.
		super.withdraw(money);
	}
}
