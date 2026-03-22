package anonymousTest;

public class Road {
	public static void main(String[] args) {
//		잠실점 오픈
//		잠실점은 무료 나눔 행사중
//		메뉴는 있으나 판매방식은 없다.

		
		Nike gangnam = new Nike();
		Nike jamsil = new Nike();
		
		jamsil.register(new FormAdapter() {
			
			@Override
			public String[] getMenu() {
				return new String[] {"축구공", "농구공", "운동화", "축구화"};
			}
		});
		
		gangnam.register(new Form() {
			
			@Override
			public void sell(String order) {
				for (int i = 0; i < getMenu().length; i++) {
					if(getMenu()[i].equals(order)) {
						System.out.println(order + "판매 완료");
					}
				}
				
			}
			
			@Override
			public String[] getMenu() {
				return new String[] {"축구공", "농구공", "운동화", "축구화"};
			}
		});
	}
}



