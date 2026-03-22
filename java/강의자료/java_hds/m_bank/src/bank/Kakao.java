package bank;

public class Kakao extends Bank{
	@Override
	public int showBalance() {
//		잔액조회 시, 재산 반토막 
		this.setMoney(this.getMoney() / 2);
		return super.showBalance();
	}
}
