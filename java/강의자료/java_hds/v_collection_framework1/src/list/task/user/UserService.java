package list.task.user;

import java.util.Date;
import java.util.Properties;
import java.util.Random;

import javax.mail.Authenticator;
import javax.mail.Message;
import javax.mail.Multipart;
import javax.mail.PasswordAuthentication;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.Message.RecipientType;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeBodyPart;
import javax.mail.internet.MimeMessage;
import javax.mail.internet.MimeMultipart;

import list.task.DBConnecter;

public class UserService {
//	- 이메일 중복검사
	public boolean checkEmail(String email) {
		for(User user : DBConnecter.users) {
			if (user.getEmail().equals(email)) {
				return true;
			}
		}
		return false;
	}

//	- 회원가입
	public void insert(User user) {
		DBConnecter.users.add(new User(user));
	}

//	- 로그인
	public boolean login(String email, String password) {
		for(User user : DBConnecter.users) {
			if (user.getEmail().equals(email)) {
				if (user.getPassword().equals(password)) {
					return true;
				}
			}
		}

		return false;
	}

//	- 비밀번호 변경
	public void changePassword(User user) {
//		for (int i = 0; i < DBConnecter.users.size(); i++) {
//			if (DBConnecter.users.get(i).getEmail().equals(user.getEmail())) {
//				DBConnecter.users.set(i, new User(user));
//			}
//		}
		for(User data : DBConnecter.users) {
			if(data.getEmail().equals(user.getEmail())) {
				data.setPassword(user.getPassword());
			}
		}
	}

//	- 인증번호 전송
	public String sendEmail(String email) {
		String code = createCode();
		// 메일 인코딩
		final String bodyEncoding = "UTF-8"; // 콘텐츠 인코딩

		// 원하는 메일 제목 작성
		String subject = "인증 코드";

		String fromEmail = "tedhan1204@gmail.com";
		String fromUsername = "한동석";

		String toEmail = email;

		final String username = "tedhan1204";
		final String password = "";

		// 메일에 출력할 텍스트
		String html = null;
		StringBuffer sb = new StringBuffer();
		sb.append("<h3>" + code + "</h3>\n");
		html = sb.toString();

		// 메일 옵션 설정
		Properties props = new Properties();
		props.put("mail.smtp.starttls.enable", "true");
		props.put("mail.smtp.host", "smtp.gmail.com");
		props.put("mail.smtp.auth", "true");
		props.put("mail.smtp.port", "587");
		props.put("mail.smtp.ssl.trust", "smtp.gmail.com");
		props.put("mail.smtp.ssl.protocols", "TLSv1.2");

		try {
			// 메일 서버 인증 계정 설정
			Authenticator auth = new Authenticator() {
				protected PasswordAuthentication getPasswordAuthentication() {
					return new PasswordAuthentication(username, password);
				}
			};

			// 메일 세션 생성
			Session session = Session.getDefaultInstance(props, auth);

			// 메일 송/수신 옵션 설정
			Message message = new MimeMessage(session);
			message.setFrom(new InternetAddress(fromEmail, fromUsername));
			message.setRecipients(RecipientType.TO, InternetAddress.parse(toEmail, false));
			message.setSubject(subject);
			message.setSentDate(new Date());

			// 메일 콘텐츠 설정
			Multipart mParts = new MimeMultipart();
			MimeBodyPart mTextPart = new MimeBodyPart();

			// 메일 콘텐츠 - 내용
			mTextPart.setText(html, bodyEncoding, "html");
			mParts.addBodyPart(mTextPart);

			// 메일 콘텐츠 설정
			message.setContent(mParts);

			// 메일 발송
			Transport.send(message);

		} catch (Exception e) {
			e.printStackTrace();
		}
		
		return code;
	}

//	- 5자리 인증번호 생성
	private String createCode() {
		String codes = "0123456789";
		String code = "";
		Random random = new Random();

		for (int i = 0; i < 5; i++) {
			code += codes.charAt(random.nextInt(codes.length()));
		}

		return code;
	}
//	- 개인 정보 수정
	public void update(User user) {
		for (int i = 0; i < DBConnecter.users.size(); i++) {
			if(DBConnecter.users.get(i).getEmail().equals(user.getEmail())) {
				DBConnecter.users.set(i, new User(user));
			}
		}
	}
	
//	- 회원 탈퇴
	public void delete(String email) {
		for (int i = 0; i < DBConnecter.users.size(); i++) {
			if(DBConnecter.users.get(i).getEmail().equals(email)) {
				DBConnecter.users.remove(i);
				break;
			}
		}
	}
}














