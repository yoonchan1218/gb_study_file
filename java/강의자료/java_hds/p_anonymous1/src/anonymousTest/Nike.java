package anonymousTest;

public class Nike {
	public void register(Form form) {
		for (int i = 0; i < form.getMenu().length; i++) {
			System.out.println(form.getMenu()[i]);
		}
		if(form instanceof FormAdapter) {
			System.out.println("무료 나눔 매장입니다.");
		}else {
			form.sell("축구공");
		}
	}
}
