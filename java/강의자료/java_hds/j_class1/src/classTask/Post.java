package classTask;

public class Post {
	long id;
	String title;
	String content;
	
	Reply[] arReply;
	int replyCount;
	
	public Post() {;}

	public Post(long id, String title, String content, Reply[] arReply) {
		this.id = id;
		this.title = title;
		this.content = content;
		this.arReply = arReply;
		
		this.replyCount = arReply.length;
	}
}
