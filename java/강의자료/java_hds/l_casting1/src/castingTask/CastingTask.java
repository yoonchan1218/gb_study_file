package castingTask;

public class CastingTask {
//	아래의 getService 메소드로 1개의 영상을 전달받은 뒤
//	Animation과 Film일 경우에만 각 서비스를 사용한다.
//	반드시 up casting과 down casting을 활용한다.
//	Film, Animation, Drama 중 어떤 영상이 들어올지 알 수 없다.
	public void getService(Video video) {
		if(video instanceof Animation) {
			Animation animation = (Animation) video;
			animation.printSubtitle();
			
		}else if(video instanceof Film) {
			Film film = (Film) video;
			film.shake();
			
		}else {
			System.out.println("지원되지 않는 서비스입니다.");
		}
	}
	
	public static void main(String[] args) {
		
		CastingTask castingTask = new CastingTask();
		
		Video[] arVideo = {
			new Film(),
			new Animation(),
			new Drama()
		};
		
		for (int i = 0; i < arVideo.length; i++) {
			castingTask.getService(arVideo[i]);
		}
	}
}














