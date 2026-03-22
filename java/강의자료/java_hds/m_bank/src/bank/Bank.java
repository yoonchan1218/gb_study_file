package bank;

public class Bank {
	private String name;
	private String account;
	private String phone;
	private String password;
	private int money;

	public Bank() {
		;
	}

	public Bank(String name, String account, String phone, String password, int money) {
		super();
		this.name = name;
		this.account = account;
		this.phone = phone;
		this.password = password;
		this.money = money;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getAccount() {
		return account;
	}

	public void setAccount(String account) {
		this.account = account;
	}

	public String getPhone() {
		return phone;
	}

	public void setPhone(String phone) {
		this.phone = phone;
	}

	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}

	public int getMoney() {
		return money;
	}

	public void setMoney(int money) {
		this.money = money;
	}

//	계좌번호 중복검사
//	모든 고객의 정보를 가져오기 위해 arrBank를 전달받는다.
//	가입한 고객의 계좌번호만 가져오면 되기 때문에,
//	이를 위해서는 은행별로 가입한 고객 수를 알아야 한다.
//	arCount는 은행별 고객 수를 담고 있는 배열이다.
//	전달받은 계좌번호(account)가 이미 존재하는 계좌번호인지 검사한다.
	public final static Bank checkAccount(Bank[][] arrBank, int[] arCount, String account) {
//		전달받은 계좌번호 주인이 있다면 bank에 담아준다.
//		checkAccount 메소드의 활용범위를 넓히기 위해서
//		true, false가 아닌 찾은 객체를 리턴한다.
		Bank bank = null;

//		은행 수만큼 반복한다(3번)
		for (int i = 0; i < arrBank.length; i++) {
//			안에 있는 for문 밖에서도 j를 사용해야하기 때문에
//			이 영역에 선언한다.
			int j = 0;

//			i번 은행의 고객 수만큼 반복한다.
			for (j = 0; j < arCount[i]; j++) {
//				가입된 모든 고객의 계좌번호를 조회해서 전달받은 계좌번호와 같은지 검사
				if (arrBank[i][j].getAccount().equals(account)) {
//					전달받은 계좌번호 주인을 bank에 담아준다.
					bank = arrBank[i][j];
//					어차피 계좌번호는 중복이 없기 때문에,
//					계좌번호를 찾았다면, 더이상 반복은 의미가 없다.
//					따라서 break로 반복문을 탈출한다.
					break;
				}
			}

//			만약 위의 for문에서 j가 arCount[i]까지 증가하지 못했다면,
//			break를 만났다는 뜻이다. 즉, 안에 있는 for문이 break로 종료되었다면,
//			밖에 있는 for문도 종료시키라는 뜻이다.
			if (j != arCount[i]) {
				break;
			}
		}

//		계좌번호를 찾았다면, 그 계좌번호의 주인(객체)이 리턴되고,
//		계좌번호를 찾지 못했다면, null이 리턴된다.
		return bank;
	}

//	핸드폰 번호 중복검사
	public final static Bank checkPhone(Bank[][] arrBank, int[] arCount, String phone) {
		Bank bank = null;

		for (int i = 0; i < arrBank.length; i++) {
			int j = 0;

			for (j = 0; j < arCount[i]; j++) {
				if (arrBank[i][j].getPhone().equals(phone)) {
					bank = arrBank[i][j];
					break;
				}
			}

			if (j != arCount[i]) {
				break;
			}
		}

		return bank;
	}

//	로그인
//	계좌번호와 비밀번호를 전달받는다.
	public final static Bank login(Bank[][] arrBank, int[] arCount, String account, String password) {
		
//		계좌번호가 존재한다면, 계좌번호 주인(객체)이 user에 담기고,
//		계좌번호가 없다면, null이 user에 담긴다.
		Bank user = checkAccount(arrBank, arCount, account);
		
//		만약 계좌번호가 있다면(주인을 찾았다면)
		if(user != null) {
//			그 주인의 비밀번호를 가져와서 전달받은 비밀번호와 같은지 검사한다.
			if(user.password.equals(password)) {
//				로그인 성공한 고객 정보(객체)를 리턴한다.
				return user;
			}
		}
//		로그인 실패 시, null을 리턴한다.
		return null;
	}

//	입금
	public void deposit(int money) {
		this.money += money;
	}

//	출금
	public void withdraw(int money) {
		this.money -= money;
	}

//	잔액 조회
	public int showBalance() {
		return money;
	}

}
