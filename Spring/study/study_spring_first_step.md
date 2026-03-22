# 📚 Threetier V1~V6 종합 코드 리뷰 학습 자료

> 기준 코드: `C:\Users\pigch\Desktop\gb_0090_kyc\Spring\강의자료\spring_day10~12`
> 학습 목적: 3-Tier 아키텍처 기반 Spring Boot + MyBatis 백엔드 개발 흐름 이해

---

## 버전별 핵심 변화 요약

| 버전 | 핵심 기능 | 새로 추가된 개념 |
|------|----------|----------------|
| V1 | 페이징 (무한스크롤) | Criteria, PostWithPagingDTO, IIFE 패턴 |
| V2 | 더보기 버튼 | Search 객체 기초, TagService 분리 |
| V3 | 검색/필터 | `@Param`, 동적 SQL `<if>`, `<choose>`, `<foreach>` |
| V4 | CRUD 전체 | `Optional`, 커스텀 예외, `@ControllerAdvice` |
| V5 | 이메일/SMS | JavaMailSender, MimeMessageHelper, 쿠키 인증 |
| V6 | 댓글 REST + 인터셉터 | `@RequestBody`, `HandlerInterceptor`, REST CRUD |

---

## 1. 어노테이션 완전 해부

### 📌 클래스 레벨 어노테이션

```java
// ──── PostService.java ────
@Service                           // Spring이 이 클래스를 서비스 빈으로 등록
@RequiredArgsConstructor           // final 필드를 인자로 하는 생성자를 자동 생성 (Lombok)
@Transactional(rollbackFor = Exception.class)  // 모든 public 메서드에 트랜잭션 적용
                                               // Exception(체크드/언체크드 모두) 발생 시 롤백
@Slf4j                             // log 변수 자동 생성 (Lombok) → log.info(...) 사용 가능
public class PostService { ... }
```

```java
// ──── PostController.java ────
@Controller                        // 뷰(HTML)를 반환하는 MVC 컨트롤러
@RequestMapping("/post/**")        // 이 컨트롤러의 모든 메서드는 /post/ 로 시작
@RequiredArgsConstructor
@Slf4j
public class PostController { ... }

// ──── PostAPIController.java (v1) ────
@RestController                    // @Controller + @ResponseBody 합성
                                   // 반환값을 JSON으로 직렬화해서 응답 본문에 직접 씀
@RequestMapping("/api/posts/**")
public class PostAPIController { ... }
```

```java
// ──── PostDAO.java ────
@Repository                        // Spring이 이 클래스를 DAO 빈으로 등록
@RequiredArgsConstructor           // DB 오류를 DataAccessException으로 변환
public class PostDAO { ... }
```

```java
// ──── PostMapper.java ────
@Mapper                            // MyBatis가 이 인터페이스의 구현체를 자동 생성
                                   // application.yml의 mapper-locations와 연결됨
public interface PostMapper { ... }
```

```java
// ──── Period.java ────
@NoArgsConstructor(access = AccessLevel.PROTECTED)  // 외부에서 new Period() 호출 불가
@SuperBuilder                      // 자식 클래스에서 builder() 사용할 때 부모 필드도 포함
public abstract class Period { ... }
```

```java
// ──── PostVO.java ────
@Getter                            // 모든 필드에 getter 자동 생성 (setter 없음 → 불변)
@EqualsAndHashCode(of="id")        // id 필드만 기준으로 equals/hashCode 계산
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@SuperBuilder                      // builder().id(1).postTitle("제목").build() 방식 생성
public class PostVO extends Period { ... }
```

```java
// ──── PostDTO.java ────
@Getter @Setter                    // getter + setter 모두 생성 (폼 데이터 바인딩에 필요)
@ToString                          // 로그 출력용
@EqualsAndHashCode(of="id")
@NoArgsConstructor                 // Spring MVC가 파라미터 바인딩 시 기본 생성자 필요
public class PostDTO { ... }
```

### 📌 메서드 레벨 어노테이션

```java
// ──── MemberController.java ────

// GET /member/check-email?memberEmail=test@test.com
@GetMapping("check-email")
@ResponseBody                      // @Controller에서도 이 메서드만 JSON/text 반환
public boolean checkEmail(String memberEmail) { ... }

// GET /member/login → 쿠키에서 remember 값 자동 추출
@GetMapping("login")
public String goToLoginForm(
    @CookieValue(name="remember", required = false) boolean remember,        // 없으면 false
    @CookieValue(name="remember-member-email", required = false) String email
) { ... }

// GET /post/list/{page} → URL 경로 변수 바인딩
@GetMapping("list/{page}")
public String list(@PathVariable int page, Model model) { ... }
```

```java
// ──── ReplyController.java (v6) ────

// POST /api/replies/write  → JSON 요청 본문을 ReplyDTO로 역직렬화
@PostMapping("write")
public void write(@RequestBody ReplyDTO replyDTO) { ... }

// PUT /api/replies/{id}    → 전체 수정 (필드 수가 많을 때)
@PutMapping("{id}")
public void update(@RequestBody ReplyDTO replyDTO) { ... }

// DELETE /api/replies/{id} → 삭제
@DeleteMapping("{id}")
public void delete(@PathVariable Long id) { ... }
```

```java
// ──── MemberExceptionHandler.java ────

// com.app.threetier.controller.member 패키지 내 컨트롤러에서 발생한 예외만 처리
@ControllerAdvice(basePackages = "com.app.threetier.controller.member")
public class MemberExceptionHandler {

    // LoginFailException 발생 시 이 메서드 실행
    @ExceptionHandler(LoginFailException.class)
    protected RedirectView loginFail(...) { ... }
}
```

```java
// ──── WebMvcConfig.java (v6) ────
@Configuration                     // 이 클래스가 Spring 설정 클래스임을 선언
public class WebMvcConfig implements WebMvcConfigurer { ... }
```

---

## 2. Controller 완전 분석

### 🔹 @Controller vs @RestController 차이

```
@Controller                   @RestController
────────────────────────────────────────────────
return "post/list"            return postWithPagingDTO
→ 템플릿 파일 이름 반환         → 객체를 JSON으로 직렬화
→ Thymeleaf 렌더링             → fetch() 응답으로 전달
→ 브라우저가 HTML 수신          → 브라우저가 JSON 수신
```

### 🔹 Mapping 패턴 완전 정리

**패턴 1: 와일드카드 기반 (v1~v4 방식)**
```java
@RequestMapping("/post/**")   // /post/ 이후 모든 경로를 이 컨트롤러가 처리
@GetMapping("write")          // → /post/write
@PostMapping("write")         // → /post/write (POST)
@GetMapping("list/{page}")    // → /post/list/1, /post/list/2, ...
```

**패턴 2: REST API URL 설계 (v6 Reply)**
```java
@RequestMapping("/api/replies/**")
@PostMapping("write")       // POST   /api/replies/write
@GetMapping("list/{page}")  // GET    /api/replies/list/1?postId=5
@PutMapping("{id}")         // PUT    /api/replies/42
@DeleteMapping("{id}")      // DELETE /api/replies/42
```

> **PUT vs PATCH 설계 원칙 (v6 주석에서)**
> - 수정해야 하는 필드 수가 **많으면** → `PUT` (전체 교체 의미)
> - 수정해야 하는 필드 수가 **적으면** → `PATCH` (일부 수정 의미)

### 🔹 Controller가 하는 일 vs 하지 않는 일

```java
// ✅ 컨트롤러가 해야 하는 일
@PostMapping("write")
public RedirectView write(PostDTO postDTO,                // 1. 파라미터 수신
                          @RequestParam("file") ArrayList<MultipartFile> files) {
    postService.write(postDTO, files);                    // 2. 서비스 호출
    return new RedirectView("/post/list");                // 3. 결과 반환 (리다이렉트)
}

// ❌ 컨트롤러가 하면 안 되는 일
// - DB 조회 직접 수행
// - 파일 저장 로직 작성
// - 비즈니스 규칙 검사
// → 이 모든 것은 Service로 위임
```

### 🔹 RedirectView vs return "경로" vs return null

```java
return "post/list";                    // 뷰 이름 반환 → /templates/post/list.html 렌더링
return new RedirectView("/post/list"); // HTTP 302 리다이렉트 → 브라우저가 /post/list 재요청
return null;                           // v1 write에서 임시 처리 (미완성 코드)
```

### 🔹 Model과 th:inline="javascript" 데이터 전달

```java
// 컨트롤러에서 Model에 담으면
@GetMapping("list")
public String list(Model model) {
    model.addAttribute("tags", tagService.selectAll()); // "tags" 이름으로 HTML에 전달
    return "post/list";
}
```

```html
<!-- 타임리프로 서버 데이터를 JS 변수로 전달 -->
<script th:inline="javascript">
    <!--/*
    const posts = [[${postsWithPaging.posts}]];   // <!--/* ... */--> 안에 있으면
    const criteria = [[${postsWithPaging.criteria}]];  // Thymeleaf가 렌더링하고 주석이 됨
    */-->
</script>
<!-- detail.html에서 postId를 JS에 전달하는 실제 사용 예 -->
<script th:inline="javascript">
    const postId = [[${post.id}]];   // 서버의 post.id를 JS 변수 postId에 할당
</script>
```

### 🔹 쿠키와 세션 처리 (MemberController)

```java
@PostMapping("login")
public RedirectView login(MemberDTO memberDTO, HttpServletResponse response) {
    // 1. 세션에 로그인 정보 저장 (서버 메모리에 저장, 브라우저 종료 시 삭제)
    session.setAttribute("member", memberService.login(memberDTO));

    // 2. "이메일 저장" 쿠키 생성
    Cookie rememberCookie = new Cookie("remember", String.valueOf(memberDTO.isRemember()));
    rememberCookie.setPath("/");                 // 모든 경로에서 쿠키 전송

    if (memberDTO.isRemember()) {
        rememberCookie.setMaxAge(60 * 60 * 24 * 30); // 30일 유지
    } else {
        rememberCookie.setMaxAge(0);             // 즉시 삭제 (0 = 만료)
    }
    response.addCookie(rememberCookie);          // 응답 헤더에 Set-Cookie 추가
    return new RedirectView("/post/list/1");
}

// 쿠키 읽기 - 로그인 폼에서 이메일 자동 입력
@GetMapping("login")
public String goToLoginForm(
    @CookieValue(name="remember", required = false) boolean remember,
    @CookieValue(name="remember-member-email", required = false) String rememberMemberEmail,
    Model model) {
    model.addAttribute("remember", remember);
    model.addAttribute("rememberMemberEmail", rememberMemberEmail);
    return "member/login";
}
```

---

## 3. Service 완전 분석

### 🔹 Service에 들어오는 코드의 종류와 이유

```java
@Service
@RequiredArgsConstructor
@Transactional(rollbackFor = Exception.class)
@Slf4j
public class PostService {
    // ★ 여러 DAO를 조합 - 서비스가 여러 DAO를 오케스트레이션
    private final PostDAO postDAO;
    private final TagDAO tagDAO;
    private final FileDAO fileDAO;
    private final PostFileDAO postFileDAO;
```

**Service에 들어와야 하는 코드:**

```java
// 1. 비즈니스 로직 (다수 엔티티 조합)
public void write(PostDTO postDTO, ArrayList<MultipartFile> multipartFiles) {
    postDAO.save(postDTO);           // ① 게시글 저장

    postDTO.getTags().forEach(tagDTO -> {
        tagDTO.setPostId(postDTO.getId());  // ② 방금 저장된 postId를 태그에 세팅
        tagDAO.save(tagDTO.toVO());          // ③ 태그 저장
    });

    multipartFiles.forEach(multipartFile -> {  // ④ 파일 처리
        fileDAO.save(fileDTO);
        postFileDAO.save(postFileDTO.toPostFileVO());
        multipartFile.transferTo(new File(path, fileName)); // ⑤ 실제 파일 저장
    });
    // → 이 전체가 하나의 @Transactional 트랜잭션 = 하나라도 실패하면 전체 롤백
}

// 2. 조회 후 가공 (DateUtils, 연관 데이터 조립)
public PostWithPagingDTO list(int page, Search search) {
    Criteria criteria = new Criteria(page, postDAO.findTotal(search));  // 페이징 계산
    List<PostDTO> posts = postDAO.findAll(criteria, search);

    // hasMore 판정: DB에서 rowCount+1개 조회 → +1개가 있으면 더 있음
    criteria.setHasMore(posts.size() > criteria.getRowCount());
    if (criteria.isHasMore()) {
        posts.remove(posts.size() - 1);  // 마지막 +1 제거
    }

    posts.forEach(postDTO -> {
        // 상대 시간 변환 ("5분 전", "3시간 전")
        postDTO.setCreatedDatetime(DateUtils.toRelativeTime(postDTO.getCreatedDatetime()));
        // 연관 태그 조회 및 변환
        postDTO.setTags(tagDAO.findAllByPostId(postDTO.getId())
                .stream().map(this::toTagDTO).collect(Collectors.toList()));
        // 연관 파일 조회
        postDTO.setPostFiles(postFileDAO.findAllByPostId(postDTO.getId()));
    });
    return postWithPagingDTO;
}

// 3. 예외 처리 (Optional + orElseThrow)
public PostDTO detail(Long id) {
    Optional<PostDTO> foundPost = postDAO.findById(id);
    PostDTO postDTO = foundPost.orElseThrow(PostNotFoundException::new);
    // Optional이 비어있으면 PostNotFoundException 발생 → @ControllerAdvice가 캐치
    ...
}

// 4. 삭제 순서 보장 (FK 제약 조건 고려)
public void delete(Long id) {
    tagDAO.deleteByPostId(id);           // ① 태그 먼저 삭제 (FK)
    postFileDAO.findAllByPostId(id).forEach(postFileDTO -> {
        File file = new File("C:/file/" + postFileDTO.getFilePath(), postFileDTO.getFileName());
        if (file.exists()) file.delete(); // ② 실제 파일 삭제
        postFileDAO.delete(fileId);        // ③ 연결테이블 삭제
        fileDAO.delete(fileId);            // ④ 파일 메타 삭제
    });
    postDAO.delete(id);                  // ⑤ 게시글 마지막에 삭제
}
```

**Service에 들어오면 안 되는 코드:**
- HTTP 요청/응답 처리 (`HttpServletRequest`, `HttpServletResponse`) → Controller
- 뷰 이름 반환 → Controller
- SQL 직접 작성 → Mapper XML

---

## 4. DAO (Repository) 완전 분석

### 🔹 DAO의 역할과 패턴

```java
@Repository
@RequiredArgsConstructor
@Slf4j
public class PostDAO {
    private final PostMapper postMapper;  // Mapper 인터페이스 주입

    // DAO 메서드명 = Java 관용어 (findAll, save, findById...)
    // Mapper 메서드명 = SQL 관용어 (selectAll, insert, selectById...)

    public void save(PostDTO postDTO) {
        postMapper.insert(postDTO);       // DAO → Mapper → XML 쿼리
    }

    public List<PostDTO> findAll(Criteria criteria, Search search) {
        return postMapper.selectAll(criteria, search);
    }

    public int findTotal(Search search) {
        return postMapper.selectTotal(search);
    }

    // v4: Optional 사용 - null 안전한 반환
    public Optional<PostDTO> findById(Long id) {
        return postMapper.selectById(id);
    }

    // v4: VO를 받아서 수정 (VO는 불변 → builder로 만들어서 전달)
    public void setPost(PostVO postVO) {
        postMapper.update(postVO);
    }

    public void delete(Long id) {
        postMapper.delete(id);
    }
}
```

### 🔹 DAO가 하는 단 하나의 일

```
DAO = Mapper 인터페이스를 감싸는 래퍼
이유: Service 코드가 MyBatis에 직접 의존하지 않도록 분리
나중에 JPA로 교체할 때 DAO 구현만 교체하면 Service 코드 변경 없음
```

---

## 5. Mapper 인터페이스 완전 분석

### 🔹 @Mapper와 @Param

```java
@Mapper
public interface PostMapper {
    // 단일 파라미터: @Param 불필요
    public void insert(PostDTO postDTO);
    public Optional<PostDTO> selectById(Long id);
    public void update(PostVO postVO);
    public void delete(Long id);

    // ★ 복수 파라미터: 반드시 @Param으로 이름 지정
    // XML에서 #{criteria.offset}, #{search.keyword} 로 접근
    public List<PostDTO> selectAll(
        @Param("criteria") Criteria criteria,
        @Param("search") Search search
    );

    public int selectTotal(
        @Param("search") Search search
    );
}
```

```java
// Reply Mapper - 복수 파라미터 패턴
public interface ReplyMapper {
    public List<ReplyDTO> selectAllByPostId(
        @Param("criteria") Criteria criteria,
        @Param("id") Long id              // id는 postId를 의미
    );
    public int selectCountAllByPostId(Long id); // 단일이면 @Param 불필요
}
```

**@Mapper 인터페이스와 XML의 1:1 연결 규칙:**
```
PostMapper.java  ←→  postMapper.xml
namespace="com.app.threetier.mapper.PostMapper"   ← 인터페이스 풀패스와 일치
id="insert"      ←→  public void insert(...)
id="selectAll"   ←→  public List<PostDTO> selectAll(...)
```

---

## 6. DTO / VO 완전 분석

### 🔹 VO와 DTO의 역할 구분

```
VO (Value Object) = DB 테이블의 구조를 반영
└── 불변 (setter 없음, @Getter만)
└── 생성자: @NoArgsConstructor(PROTECTED) + @SuperBuilder
└── DB → Java로 읽은 "원본 데이터"

DTO (Data Transfer Object) = 계층 간 데이터 전달용
└── 가변 (@Getter @Setter)
└── @NoArgsConstructor (Spring MVC 파라미터 바인딩을 위해 필요)
└── 화면 ↔ Service ↔ DB 사이를 이동하는 "운반 객체"
└── 화면에 필요한 추가 필드 포함 (memberName, tags, postFiles 등)
```

### 🔹 실제 코드로 보는 VO vs DTO 차이

```java
// ──── PostVO.java (불변, DB 구조 반영) ────
@Getter                        // setter 없음 → 생성 후 변경 불가
@NoArgsConstructor(access = AccessLevel.PROTECTED)  // new PostVO() 직접 호출 불가
@SuperBuilder                  // PostVO.builder().id(1).postTitle("제목").build()
public class PostVO extends Period {
    private Long id;
    private String postTitle;
    private String postContent;
    private int postReadCount;
    private Status postStatus;
    private Long memberId;
    // ★ memberName은 없음 - DB tbl_post 테이블에는 member_id만 있음
}

// ──── PostDTO.java (가변, 화면 요구사항 반영) ────
@Getter @Setter                // setter 있음 → Spring MVC가 폼 데이터 바인딩 가능
@NoArgsConstructor             // 기본 생성자 필요
public class PostDTO {
    private Long id;
    private String postTitle;
    private String postContent;
    private int postReadCount;
    private Status postStatus;
    private Long memberId;
    private String memberName;    // ★ JOIN 결과 - tbl_member에서 가져옴
    private String createdDatetime;
    private String updatedDatetime;

    // ★ 화면 표시용 연관 데이터 - DB 테이블에 없는 필드
    private List<TagDTO> tags = new ArrayList<>();
    private List<PostFileDTO> postFiles = new ArrayList<>();

    // VO로 변환 - DB에 저장할 때 사용
    public PostVO toVO() {
        return PostVO.builder()
                .id(id).postTitle(postTitle)...build();
    }
}
```

### 🔹 DTO를 언제 사용하는가

```
상황 1: 폼 데이터 수신 (Controller 파라미터)
  @PostMapping("write")
  public RedirectView write(PostDTO postDTO, ...)
  → Spring MVC가 form의 name 속성을 DTO 필드에 바인딩

상황 2: REST API 응답 (JSON 직렬화)
  @GetMapping("list/{page}")
  public PostWithPagingDTO list(...)
  → DTO를 Jackson이 JSON으로 변환 → fetch() 응답

상황 3: REST API 요청 수신 (@RequestBody)
  @PostMapping("write")
  public void write(@RequestBody ReplyDTO replyDTO)
  → JSON 본문을 Jackson이 DTO로 역직렬화

상황 4: DB 조회 결과 매핑
  List<PostDTO> selectAll(...)
  → MyBatis가 ResultSet을 DTO 필드에 camelCase 변환하여 매핑
```

### 🔹 PostWithPagingDTO - 페이징 응답 래퍼

```java
// API 응답을 하나의 객체로 묶어서 반환
public class PostWithPagingDTO {
    private List<PostDTO> posts;       // 게시글 목록
    private Criteria criteria;         // 페이징 정보
}

// ReplyWithPagingDTO도 동일한 패턴
public class ReplyWithPagingDTO {
    private List<ReplyDTO> replies;
    private Criteria criteria;
}
```

### 🔹 toVO() / toDTO() 변환 메서드의 의미

```java
// TagDTO.java
public TagVO toVO() {           // DTO → VO: DB에 저장할 때
    return TagVO.builder()
            .id(id).postId(postId).tagName(tagName).build();
}

// ReplyDTO.java
public ReplyVO toVO() {         // DTO → VO: DB에 저장할 때
    return ReplyVO.builder()
            .id(id).replyContent(replyContent)
            .memberId(memberId).postId(postId)...build();
}

// MemberService.java - 수동 변환
public MemberDTO toDTO(MemberVO memberVO) {   // VO → DTO: 서비스에서 반환할 때
    MemberDTO memberDTO = new MemberDTO();
    memberDTO.setId(memberVO.getId());
    memberDTO.setMemberEmail(memberVO.getMemberEmail());
    ...
    return memberDTO;
}
```

---

## 7. MyBatis XML 쿼리 완전 분석

### 🔹 XML 기본 구조

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<!-- namespace: 연결할 Mapper 인터페이스의 풀패스 (패키지.클래스명) -->
<mapper namespace="com.app.threetier.mapper.PostMapper">
    ...
</mapper>
```

### 🔹 INSERT - 게시글 저장

```xml
<!-- id="insert" : PostMapper.insert() 메서드와 연결 -->
<!-- useGeneratedKeys="true" : DB가 자동 생성한 PK를 받아옴 (AUTO_INCREMENT) -->
<!-- keyProperty="id" : 자동 생성된 PK를 PostDTO.id 필드에 세팅 -->
<insert id="insert" useGeneratedKeys="true" keyProperty="id">
    insert into tbl_post (post_title, post_content, member_id)
    values(#{postTitle}, #{postContent}, #{memberId})
</insert>
```

**useGeneratedKeys 동작 원리:**
```
INSERT 실행 후 DB가 생성한 id를
→ PostDTO의 id 필드에 자동으로 채워줌
→ Service에서 postDTO.getId() 로 바로 사용 가능

Service 코드:
postDAO.save(postDTO);                    // INSERT 실행
postDTO.getId()                           // → DB가 생성한 id 반환 (useGeneratedKeys 덕분)
tagDTO.setPostId(postDTO.getId());        // 방금 생성된 id로 태그 연결
```

### 🔹 SELECT 목록 - 페이징 쿼리

```xml
<!-- v1: 단순 페이징 -->
<select id="selectAll">
    select
        m.member_name,
        p.id, p.post_title, p.post_content,
        p.post_read_count, p.post_status,
        p.member_id, p.created_datetime, p.updated_datetime
    from tbl_member m join tbl_post p
    on m.id = p.member_id
    order by id desc
    limit #{count} offset #{offset}
    <!--
        count = rowCount + 1 = 11 (10개 + hasMore 판정용 1개)
        offset = (page - 1) * rowCount
        page=1 → offset=0, count=11 → 1~11번 행
        page=2 → offset=10, count=11 → 11~21번 행
    -->
</select>

<!-- v3: 파라미터가 2개 → Criteria와 Search에 이름으로 접근 -->
<select id="selectAll">
    ...
    limit #{criteria.count} offset #{criteria.offset}
</select>
```

### 🔹 동적 SQL - v4 필터 쿼리 (핵심)

```xml
<!-- 재사용 가능한 SQL 조각 정의 -->
<sql id="search">

    <!-- ① keyword가 있을 때만 조건 추가 -->
    <if test="search.keyword != null and search.keyword != ''.toString()">

        <!-- choose-when-otherwise = Java의 if-else if-else -->
        <choose>
            <when test="search.type == '제목'.toString()">
                post_title like concat('%', #{search.keyword}, '%')
            </when>
            <when test="search.type == '내용'.toString()">
                post_content like concat('%', #{search.keyword}, '%')
            </when>
            <otherwise>
                (
                    post_title like concat('%', #{search.keyword}, '%')
                    or
                    post_content like concat('%', #{search.keyword}, '%')
                )
            </otherwise>
        </choose>
    </if>

    <!-- ② tagNames 배열이 있을 때 태그 필터 -->
    <if test="search.tagNames != null">
        and
        t.post_id in
        (
            select post_id
            from tbl_tag
            where
                tag_name in
                <trim prefix="(" suffix=")">
                    <foreach item="tagName" collection="search.tagNames" separator=",">
                        #{tagName}
                    </foreach>
                </trim>
            group by post_id
            having count(post_id) = #{search.tagNamesSize}
        )
    </if>
</sql>

<!-- sql 조각 사용: <where> 태그가 내부 조건 유무에 따라 WHERE 자동 추가 -->
<select id="selectAll">
    select distinct ...
    from tbl_member m join tbl_post p on m.id = p.member_id
    left outer join tbl_tag t on p.id = t.post_id
    <where>
        <include refid="search"></include>
    </where>
    order by id desc
    limit #{criteria.count} offset #{criteria.offset}
</select>
```

### 🔹 SELECT 단건 + UPDATE + DELETE

```xml
<!-- 단건 조회 -->
<select id="selectById">
    select distinct m.member_name, p.id, p.post_title, ...
    from tbl_member m join tbl_post p on m.id = p.member_id
    where p.id = #{id}
</select>

<!-- 수정 -->
<update id="update">
    update tbl_post
    set
        post_title = #{postTitle},
        post_content = #{postContent},
        updated_datetime = current_timestamp
    where id = #{id}
</update>

<!-- 삭제 -->
<delete id="delete">
    delete from tbl_post where id = #{id}
</delete>
```

### 🔹 replyMapper.xml 전체 분석 (v6)

```xml
<mapper namespace="com.app.threetier.mapper.ReplyMapper">

    <insert id="insert">
        insert into tbl_reply (reply_content, member_id, post_id)
        values (#{replyContent}, #{memberId}, #{postId})
    </insert>

    <select id="selectAllByPostId">
        select m.member_name, r.id, r.reply_content, r.member_id,
               r.post_id, r.created_datetime, r.updated_datetime
        from tbl_member m join tbl_reply r on m.id = r.member_id
        where post_id = #{id}
        order by r.id desc
        limit #{criteria.rowCount} offset #{criteria.offset}
        <!--
            ★ postMapper와 차이:
            postMapper: limit #{criteria.count}  (rowCount+1, hasMore 판정용)
            replyMapper: limit #{criteria.rowCount}  (정확히 rowCount개만)
        -->
    </select>

    <select id="selectCountAllByPostId">
        select count(*) from tbl_reply where post_id = #{id}
    </select>

    <update id="update">
        update tbl_reply
        set reply_content = #{replyContent}, updated_datetime = current_timestamp
        where id = #{id}
    </update>

    <delete id="delete">
        delete from tbl_reply where id = #{id}
    </delete>

    <delete id="deleteAllByPostId">
        delete from tbl_reply where post_id = #{id}
    </delete>
</mapper>
```

---

## 8. JavaScript 완전 분석 (service / layout / event)

### 🔹 IIFE 패턴 - 3파일 분리의 핵심

```javascript
// IIFE = Immediately Invoked Function Expression (즉시 실행 함수)
const postService = (() => {    // ← 화살표 함수 선언
    // 내부 변수/함수는 외부에서 접근 불가 (클로저)
    const getList = async (page, callback) => { ... }

    return { getList: getList };  // 공개할 함수만 반환
}) ();                           // ← 즉시 실행 ()

// 다른 파일에서 postService.getList() 로 호출 가능
// postService 내부 구현은 캡슐화되어 숨겨짐
```

### 🔹 service.js - API 호출 담당 (비동기)

**v1 service.js (단순 버전):**
```javascript
const postService = (() => {
    const getList = async (page, callback) => {
        page = page || 1;

        const response = await fetch(`/api/posts/list/${page}`)
        const postWithPaging = await response.json();

        if (callback) {
            return callback(postWithPaging);
        }
    }
    return { getList: getList };
}) ();
```

**v6 service.js (검색 파라미터 추가):**
```javascript
const postService = (() => {
    const getList = async (page, {type, keyword, tagNames}, callback) => {
        page = page || 1;

        let queryString = `?type=${type}`;
        queryString += `&keyword=${keyword}`;
        if (tagNames) {
            tagNames.forEach((tagName) => {
                queryString += `&tagNames=${tagName}`;
            });
        }

        const response = await fetch(`/api/posts/list/${page}${queryString}`)
        const postWithPaging = await response.json();
        if (callback) {
            return callback(postWithPaging);
        }
    }
    return { getList: getList };
}) ();
```

**reply service.js (POST/PUT/DELETE 포함):**
```javascript
const replyService = (() => {

    // POST 요청: JSON 본문 전송
    const write = async (reply) => {
        await fetch("/api/replies/write", {
            method: "POST",
            body: JSON.stringify(reply),
            headers: { "Content-Type": "application/json" }
        });
    }

    const getList = async (page, postId, callback) => {
        const response = await fetch(`/api/replies/list/${page}?postId=${postId}`);
        const replies = await response.json();
        if (callback) callback(replies);
    }

    const update = async (reply) => {
        await fetch(`/api/replies/${reply.id}`, {
            method: "PUT",
            body: JSON.stringify(reply),
            headers: { "Content-Type": "application/json" }
        })
    }

    const remove = async (id) => {
        await fetch(`/api/replies/${id}`, { method: "DELETE" });
    }

    return { write, getList, update, remove };
})();
```

**member service.js (이메일 중복 확인):**
```javascript
const memberService = (() => {
    const checkEmail = async (memberEmail, callback) => {
        const response = await fetch(`/member/check-email?memberEmail=${memberEmail}`)
        const isAvailable = await response.text() === "true"
        if (callback) callback(isAvailable);
    }
    return { checkEmail: checkEmail };
})()
```

### 🔹 layout.js - DOM 조작 담당 (동기)

```javascript
const postLayout = (() => {
    const showList = (postWithPaging) => {
        const tbody = document.querySelector("#post-list tbody");
        const posts = postWithPaging.posts;
        const criteria = postWithPaging.criteria;

        let text = ``;
        posts.forEach((post) => {
            text += `<tr><td>${post.id}</td><td>${post.postTitle}</td><td>`
            post.tags.forEach((tag) => { text += `${tag.tagName}, ` });
            text = text.substring(0, text.length - 2);  // 마지막 ", " 제거
            text += `</td><td>${post.memberName}</td>...`

            if (post.postFiles.length === 0) {
                text += `<img src="/image/no-image.png" width="100px">`
            } else {
                text += `<img src="/api/files/display?filePath=...&fileName=...">`
            }
            text += `</td>`;
        });

        tbody.innerHTML += text;  // += : 기존 내용에 추가 (무한스크롤)
        return criteria;
    }
    return { showList: showList };
})();
```

**reply layout.js (기본 페이징 포함):**
```javascript
const replyLayout = (() => {
    const showList = ({replies, criteria}) => {    // 구조 분해 할당
        let text = ``;
        replies.forEach((reply) => {
            text += `
                <div class="reply reply-wrap${reply.id}">
                    <span class="span${reply.id}">${reply.replyContent}</span>/
                    <a href="${reply.id}" id="update-ready">수정/</a>
                    <a style="display: none;" href="${reply.id}" id="update-ok">수정완료/</a>
                    <a href="${reply.id}" id="delete-ok">삭제</a>
                </div>
            `;
            // href="${reply.id}" = reply.id를 링크처럼 활용 (실제 링크 아님)
            // event.js에서 e.target.getAttribute("href")로 id 추출
        });

        // 기본 페이징 HTML 생성
        if (criteria.startPage > 1) {
            text += `<a class="paging" href="${criteria.startPage - 1}">[이전]</a>`;
        }
        for (let i = criteria.startPage; i <= criteria.endPage; i++) {
            text += criteria.page === i
                ? `${i}`
                : `<a class="paging" href="${i}">${i}</a>`;
        }
        if (criteria.endPage !== criteria.realEnd) {
            text += `<a class="paging" href="${criteria.endPage + 1}">[다음]</a>`;
        }

        replyContainer.innerHTML = text;  // = 교체 (페이지 변경 시 전체 갱신)
    }
    return { showList };
})();
```

### 🔹 event.js - 이벤트 연결 담당 (동기 + 비동기 혼합)

**v1 event.js (무한 스크롤):**
```javascript
let page = 1;
let checkScroll = true;
let criteria = { hasMore: true }

// ① 초기 데이터 로드
postService.getList(page, postLayout.showList)

// ② 무한 스크롤
window.addEventListener("scroll", async (e) => {
    if (!checkScroll || !criteria.hasMore) { return; }

    const scrollCurrentPosition = window.scrollY;
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight;

    if (scrollCurrentPosition + windowHeight >= documentHeight - 1) {
        checkScroll = false;
        criteria = await postService.getList(++page, postLayout.showList);
    }

    setTimeout(() => { checkScroll = true; }, 500)
});
```

**v6 event.js (검색 + 태그 필터 + 무한스크롤):**
```javascript
NodeList.prototype.filter = Array.prototype.filter;  // NodeList에 filter 메서드 추가

// 태그 버튼 클릭 → 체크박스 토글
buttons.forEach((button, i) => {
    button.addEventListener("click", (e) => { checkboxes[i].click(); });
});

// 체크박스 변경 → 검색 실행
checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("click", async (e) => {
        page = 1;
        criteria = await postService.getList(page, {
            type: type.value, keyword: keyword.value,
            tagNames: checkboxes.filter((cb) => cb.checked).map((cb) => cb.value)
        }, postLayout.showList)
    });
});
```

**reply event.js (이벤트 위임 + 인라인 DOM 수정):**
```javascript
// 이벤트 위임: 컨테이너 하나에서 내부 클릭 모두 처리
// (동적으로 추가된 요소도 이벤트 받을 수 있음)
replyContainer.addEventListener("click", async (e) => {
    e.preventDefault();
    const replyId = e.target.getAttribute("href");

    if (e.target.classList.contains("paging")) {
        page = e.target.getAttribute("href");
        await replyService.getList(page, postId, replyLayout.showList);

    } else if (e.target.id === "update-ready") {
        // "수정" 클릭 → textarea 동적 생성
        const span = document.querySelector(`span.span${replyId}`);
        const textarea = document.createElement("textarea");
        textarea.value = span.textContent;
        replyWrap.prepend(textarea);
        span.remove();
        e.target.style.display = "none";
        e.target.nextElementSibling.style.display = "inline-block";

    } else if (e.target.id === "update-ok") {
        const replyContentTextArea = document.querySelector(`textarea.reply-content${replyId}`);
        await replyService.update({ id: replyId, replyContent: replyContentTextArea.value });
        await replyService.getList(page, postId, replyLayout.showList);

    } else if (e.target.id === "delete-ok") {
        const rowCount = document.querySelectorAll(".reply").length;
        await replyService.remove(replyId);
        rowCount === 1 && (page--);  // 마지막 댓글 삭제 시 이전 페이지로
        await replyService.getList(page, postId, replyLayout.showList);
    }
});
```

**update event.js - 폼 동적 조작 (동기):**
```javascript
// 태그 Enter로 추가, 클릭으로 삭제
tagInput.addEventListener("keyup", (e) => {
    if (e.key === "Enter") {
        tagListDIV.innerHTML += `<span class="tag">${e.target.value}</span>`
        arTag.push(e.target.value);
        e.target.value = "";
    }
});

// 폼 제출 시 동적 input 생성하여 추가
sendButton.addEventListener("click", (e) => {
    arTag.forEach((tag, i) => {
        const input = document.createElement("input");
        input.setAttribute("name", `tags[${i}].tagName`)  // PostDTO.tags[0].tagName
        input.value = tag;
        form.appendChild(input);
    });
    form.submit();
});
```

### 🔹 동기 vs 비동기 코드 흐름 정리

```
동기 코드 (순서대로 실행):
1. DOM 요소 참조 (document.querySelector...)
2. 이벤트 리스너 등록 (addEventListener)
3. 이벤트 핸들러 내부에서 DOM 조작 (innerHTML, createElement...)

비동기 코드 (async/await):
1. async 함수 선언 → 내부에서 await 사용 가능
2. await fetch(...) → HTTP 요청 전송, 응답 올 때까지 이 줄에서 대기
3. await response.json() → JSON 파싱, 완료될 때까지 대기
4. 다음 줄 실행 (콜백 호출, DOM 업데이트)

콜백 패턴:
postService.getList(page, postLayout.showList)
                          ^^^^^^^^^^^^^^^^^^
→ 서비스가 데이터 준비되면 이 함수 호출
→ 함수를 값으로 전달하는 고차 함수 패턴
```

---

## 9. Thymeleaf HTML 완전 분석

### 🔹 기본 속성

```html
<!-- 변수 출력 -->
<h1 th:text="${post.postTitle}">기본값</h1>

<!-- th:object로 객체 지정 후 *{} 단축 사용 -->
<div th:object="${post}">
    <h1 th:text="*{postTitle}"></h1>
    <h3 th:text="*{postContent}"></h3>
</div>

<!-- 속성 값 설정 -->
<input type="text" name="postTitle" th:value="*{postTitle}">

<!-- URL 빌더: 파라미터 자동 인코딩 -->
<img th:src="@{/api/files/display(filePath=${postFile.filePath}, fileName=${postFile.fileName})}">

<!-- 링크 URL 생성 -->
<a th:href="@{/post/update(id=${post.id})}">수정</a>
<!-- → /post/update?id=5 -->
```

### 🔹 반복 (th:each)

```html
<!-- 1:N 관계 반복 -->
<span class="tag" th:id="${tag.id}"
      th:each="tag: *{tags}"
      th:text="${tag.tagName}">
</span>

<!-- th:block: 렌더링 시 이 태그 자체는 사라짐 -->
<th:block th:each="postFile: *{postFiles}">
    <img width="100px" th:id="${postFile.id}"
         th:src="@{/api/files/display(...)}">
</th:block>

<!-- list.html: 서버에서 받은 태그 목록으로 체크박스 생성 -->
<th:block th:each="tag: ${tags}">
    <input type="checkbox" name="tagNames" th:value="${tag}">
    <button class="tag-button" th:text="${tag}"></button>
</th:block>
```

### 🔹 조건부 (th:if / th:unless)

```html
<!-- header.html: 로그인 상태에 따른 분기 -->
<th:block th:if="${session.member != null}">
    <h3 th:text="|${session.member.memberName}님 환영합니다.|"></h3>
    <!--              |...| = 리터럴 치환 (문자열 연결) -->
    <nav>
        <a th:if="${session.member.provider.value == 'kakao'}"
           href="https://kauth.kakao.com/...">로그아웃</a>
        <a th:unless="${session.member.provider.value == 'kakao'}"
           href="/member/logout">로그아웃</a>
    </nav>
</th:block>

<th:block th:unless="${session.member != null}">
    <h3>로그인 후 이용해주세요.</h3>
</th:block>

<!-- detail.html: 로그인 + 작성자 본인만 수정/삭제 표시 -->
<th:block th:if="${session.member != null}">
    <div th:if="${session.member.id == post.memberId}">
        <a th:href="@{/post/update(id=${post.id})}">수정</a>
        <a th:href="@{/post/delete(id=${post.id})}">삭제</a>
    </div>
</th:block>
```

### 🔹 프래그먼트 (th:replace)

```html
<!-- common/header.html 정의 -->
<header>  <!-- header 프래그먼트 -->
    ...
</header>

<!-- 다른 페이지에서 사용 -->
<header th:replace="~{/common/header.html::header}"></header>
<!--
    th:replace: 이 태그 전체를 프래그먼트로 교체
    ~{파일경로::프래그먼트명} 형식
-->
```

### 🔹 th:inline="javascript" - 서버 데이터를 JS로 전달

```html
<!-- detail.html: postId를 JS 변수로 전달 -->
<script th:inline="javascript">
    const postId = [[${post.id}]];
    <!-- post.id가 Long(숫자)이면 → const postId = 5; (따옴표 없음) -->
</script>

<!-- login.html: 로그인 실패 메시지 전달 -->
<script>const login = "[[${login}]]";</script>

<!-- list.html: 주석 처리 (현재 REST 방식으로 대체됨) -->
<script th:inline="javascript">
    <!--/*
    const posts = [[${postsWithPaging.posts}]];
    const criteria = [[${postsWithPaging.criteria}]];
    */-->
</script>
```

### 🔹 폼 바인딩 (update.html)

```html
<form action="/post/update" method="post" name="update-form"
      enctype="multipart/form-data"
      th:object="${post}">

    <input type="hidden" name="id" th:value="*{id}">
    <input type="text" name="postTitle" th:value="*{postTitle}">
    <textarea name="postContent" th:text="*{postContent}"></textarea>

    <span class="tag" th:id="${tag.id}"
          th:each="tag: *{tags}"
          th:text="${tag.tagName}">
    </span>
</form>
```

### 🔹 login.html - 쿠키 값으로 입력 필드 자동 채우기

```html
<input type="text" name="memberEmail" th:value="${rememberMemberEmail}">
<input type="checkbox" name="remember" value="true" th:checked="${remember}">
<!--
    th:checked="true"  → checked 속성 추가 → 체크됨
    th:checked="false" → checked 속성 없음 → 미체크
-->
```

---

## 10. 버전별 핵심 차이 정리

### V1 → V3: 필터 추가 시 변화

```
변경된 곳:
PostAPIController: list(page) → list(page, Search search)
PostService:       list(page) → list(page, Search search)
PostDAO:           findAll(criteria) → findAll(criteria, search)
PostMapper:        @Param 추가, Search 파라미터 추가
postMapper.xml:    <sql id="search">, <where>, <choose>, <foreach> 추가
service.js:        URL에 쿼리스트링 조립 로직 추가
event.js:          검색 버튼 이벤트, 태그 체크박스 이벤트 추가
list.html:         검색 UI, 태그 체크박스 추가
```

### V3 → V4: CRUD 완성

```
추가된 것:
PostController:      goToUpdateForm, update, detail, delete 메서드 추가
PostService:         detail(), update(), delete() 메서드 추가
PostDAO:             findById(), setPost(), delete() 메서드 추가
PostMapper:          selectById, update, delete 메서드 추가
postMapper.xml:      selectById, update, delete 쿼리 추가
PostExceptionHandler: PostNotFoundException, FileNotFoundException 처리
update.html, detail.html: 새 페이지 추가
post/update/event.js: 태그/파일 동적 추가/삭제 로직
```

### V4 → V6: REST API + 인터셉터 + 댓글

```
추가된 것:
WebMvcConfig:        인터셉터 등록
TestInterceptor:     preHandle/postHandle 구현
ReplyController:     @RequestBody 기반 REST CRUD
ReplyService, ReplyDAO, ReplyMapper, replyMapper.xml: 댓글 레이어 전체
ReplyDTO, ReplyVO, ReplyWithPagingDTO: 댓글 도메인
reply/service.js, layout.js, event.js: 댓글 프론트엔드
detail.html:         댓글 섹션 추가
MailService, MailController: 이메일 인증
```

---

## 11. Criteria 페이징 계산 원리

```java
public Criteria(int page, int total) {
    rowCount = 10;          // 한 페이지에 표시할 행 수
    pageCount = 10;         // 페이지 번호 그룹 크기 (1~10, 11~20, ...)
    count = rowCount + 1;   // DB에서 11개 조회 → 11번째 있으면 hasMore=true

    this.page = Math.max(1, page);
    offset = (page - 1) * rowCount;    // page=1→0, page=2→10

    endPage = (int)(Math.ceil(page / (double)pageCount) * pageCount);
    startPage = endPage - pageCount + 1;
    realEnd = (int)(Math.ceil(total / (double)rowCount));
    endPage = Math.min(endPage, realEnd);
    endPage = Math.max(1, endPage);
}
```

**hasMore 판정 흐름:**
```
DB 쿼리: LIMIT 11 OFFSET 0
결과 11개 → hasMore = true  → 표시는 10개, 스크롤 시 다음 페이지 로드
결과 8개  → hasMore = false → 그대로 표시, 스크롤해도 로드 안 함
```

---

## 12. 인터셉터 (v6)

```java
public class TestInterceptor implements HandlerInterceptor {

    // 컨트롤러 실행 전 (return false: 요청 차단)
    @Override
    public boolean preHandle(HttpServletRequest request,
                              HttpServletResponse response,
                              Object handler) throws Exception {
        request.setAttribute("test", "안녕");
        return true;  // true: 진행, false: 차단
    }

    // 컨트롤러 실행 후, 뷰 렌더링 전
    @Override
    public void postHandle(HttpServletRequest request,
                            HttpServletResponse response,
                            Object handler,
                            ModelAndView modelAndView) throws Exception { }
}

// WebMvcConfig에서 등록
@Configuration
public class WebMvcConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new TestInterceptor())
                .addPathPatterns("/test/**")
                .excludePathPatterns("/test/a");  // 특정 경로 제외
    }
}
```

---

## 13. 이메일 인증 흐름 (v5/v6)

```
[전체 흐름]
1. POST /mail/send → MailService.sendMail()
   ① 랜덤 코드 생성 (10자리 영문)
   ② 쿠키 "code" 에 저장 (3분 만료)
   ③ HTML 이메일 발송 (링크: /mail/confirm?code=xxxx)
2. 사용자 링크 클릭 → GET /mail/confirm?code=xxxx
3. MailController.confirm()
   ① cookieCode == null → 만료 → /mail/fail
   ② cookieCode.equals(code) → 인증 성공 → 쿠키 삭제 → /mail/success
   ③ 불일치 → /mail/fail

[MimeMessageHelper 사용법]
MimeMessageHelper helper = new MimeMessageHelper(mimeMessage, true, "UTF-8");
// true = multipart (첨부파일 허용)
helper.setText(htmlBody, true);    // HTML 렌더링
helper.addInline("icon", file);    // <img src="cid:icon"> 로 본문 내 이미지 삽입
helper.addAttachment("file.txt", file);  // 첨부 파일
```

---

## ======================================================
## STEP 1 심화. Spring DI / Bean 생명주기 원리
## ======================================================

> **왜 여기서 공부하나?**
> `@RequiredArgsConstructor`가 왜 생성자 주입인지, 왜 필드 주입(`@Autowired` 직접)보다 나은지를
> 원리로 이해해야 코드 리뷰나 버그 분석 시 정확한 판단을 내릴 수 있다.

### 🔹 의존성 주입 3가지 비교

```java
// ──── 방법 1: 필드 주입 (권장 X) ────
@Service
public class PostService {
    @Autowired
    private PostDAO postDAO;   // Spring이 리플렉션으로 직접 주입
    // 단점: final 불가 → 불변 보장 안 됨
    //       테스트 시 mock 주입 불편
    //       순환 참조 런타임까지 발견 못 함
}

// ──── 방법 2: 세터 주입 (선택적 의존성에만 사용) ────
@Service
public class PostService {
    private PostDAO postDAO;

    @Autowired(required = false)  // required=false: 빈이 없어도 에러 안 남
    public void setPostDAO(PostDAO postDAO) {
        this.postDAO = postDAO;
    }
    // 단점: final 불가, 객체 생성 후 언제든 교체 가능 → 불안정
}

// ──── 방법 3: 생성자 주입 (권장 ✅) ────
@Service
public class PostService {
    private final PostDAO postDAO;  // final → 한 번 주입 후 변경 불가 (불변)

    // @RequiredArgsConstructor가 이 생성자를 자동 생성
    public PostService(PostDAO postDAO) {
        this.postDAO = postDAO;
    }
    // 장점: 순환 참조를 애플리케이션 시작 시 즉시 감지
    //       테스트 시 new PostService(mockDAO) 로 쉽게 주입
    //       final 필드 보장
}
```

### 🔹 순환 참조 문제

```java
// ❌ 순환 참조 예시
@Service
public class AService {
    private final BService bService;  // A가 B를 필요로 하고
}

@Service
public class BService {
    private final AService aService;  // B도 A를 필요로 하면
}
// 생성자 주입: 애플리케이션 시작 시 BeanCurrentlyInCreationException 발생
// 필드 주입:  시작은 되지만 실행 중 StackOverflowError 발생 가능

// ✅ 해결: 서비스 분리, 이벤트 기반으로 의존 방향 제거
```

### 🔹 Bean 스코프

```java
// Singleton (기본): 애플리케이션 전체에서 하나만 생성
@Service  // @Service는 기본적으로 singleton
public class PostService { }

// Prototype: 요청마다 새 인스턴스 생성
@Component
@Scope("prototype")
public class SomeComponent { }

// Request: HTTP 요청마다 새 인스턴스 (웹 환경)
@Component
@Scope(value = WebApplicationContext.SCOPE_REQUEST, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class RequestScopedBean { }

// 실제 코드에서:
// HttpSession session은 세션 스코프 빈 → Controller에서 final로 주입받아 사용
```

### 🔹 @Component 계층 어노테이션의 실제 역할 차이

```
@Component     → 일반적인 Spring 빈 (분류 없음)
@Controller    → @Component + 웹 요청 처리 역할 명시 + 예외 핸들러 대상
@Service       → @Component + 비즈니스 로직 레이어 명시 (기능 차이는 거의 없음)
@Repository    → @Component + DataAccessException 자동 변환 기능 추가
                 (SQLException → DataAccessException으로 추상화)
@Mapper        → MyBatis 전용, 구현체를 MyBatis가 생성
```

---

## STEP 2 심화. @Transactional 동작 원리

> **왜 여기서 공부하나?**
> 코드에서 `@Transactional(rollbackFor = Exception.class)`가 클래스 전체에 붙어 있는데,
> 어떤 상황에서 롤백이 되고 안 되는지를 정확히 알아야 데이터 정합성을 보장할 수 있다.

### 🔹 Spring 트랜잭션 = AOP 프록시

```
실제 동작 순서:
1. Spring이 PostService 대신 PostService의 프록시 객체 생성
2. 프록시가 트랜잭션 시작 → Connection.setAutoCommit(false)
3. 원본 PostService 메서드 실행
4-a. 정상 종료 → commit()
4-b. 예외 발생 → rollback()

코드로 보면:
// 실제 코드
postService.write(postDTO, files);
// 내부에서 일어나는 일 (개념적)
try {
    transactionManager.begin();
    originalPostService.write(postDTO, files);  // 실제 코드 실행
    transactionManager.commit();
} catch (Exception e) {
    transactionManager.rollback();
    throw e;
}
```

### 🔹 셀프 호출 문제 (중요 버그 원인)

```java
@Service
@Transactional(rollbackFor = Exception.class)
public class PostService {

    public void methodA() {
        methodB();  // ❌ 셀프 호출 → methodB의 @Transactional 무시됨!
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void methodB() {
        // 이 메서드는 새 트랜잭션에서 실행되길 원하지만...
        // methodA()가 직접 호출하면 프록시를 거치지 않아 트랜잭션 무시
    }
}

// ✅ 해결: methodB를 별도 서비스로 분리
@Service
public class PostHelperService {
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void methodB() { ... }  // 별도 빈 → 프록시 경유 → 트랜잭션 적용
}
```

### 🔹 readOnly = true 최적화

```java
// 조회 전용 메서드는 readOnly 추가
@Transactional(readOnly = true)
public PostWithPagingDTO list(int page, Search search) {
    // 장점 1: JPA Dirty Checking 비활성화 (MyBatis는 영향 적지만 습관 중요)
    // 장점 2: DB 레플리카(Slave)로 자동 라우팅 가능
    // 장점 3: 코드 의도 명확히 표현
    return ...;
}

// 쓰기 메서드는 기본 (rollbackFor Exception)
@Transactional(rollbackFor = Exception.class)
public void write(...) { ... }
```

### 🔹 트랜잭션 전파 레벨 요약

```
REQUIRED (기본):
  → 기존 트랜잭션 있으면 참여, 없으면 새로 시작
  → 현재 코드(PostService)의 기본 동작

REQUIRES_NEW:
  → 항상 새 트랜잭션 시작 (기존 트랜잭션 잠시 중단)
  → 로그 저장처럼 "부모 실패해도 독립 커밋" 이 필요할 때

NESTED:
  → 기존 트랜잭션 안에 중첩 트랜잭션 (savepoint 방식)
  → 중첩 실패해도 외부 트랜잭션은 롤백 안 됨
```

---

## STEP 3 심화. MyBatis ResultMap (N+1 문제 해결)

> **왜 여기서 공부하나?**
> 현재 PostService.list()에서 게시글 10개를 가져온 뒤,
> 각 게시글마다 태그 조회(10번), 파일 조회(10번) = 총 21번의 쿼리가 실행된다.
> resultMap의 `<collection>`으로 한 번에 해결할 수 있다.

### 🔹 N+1 문제 현재 코드에서 확인

```java
// PostService.java - N+1 발생 코드
posts.forEach(postDTO -> {
    // ★ posts가 10개면 아래 두 줄이 각각 10번씩 실행 = 총 20번 추가 쿼리
    postDTO.setTags(tagDAO.findAllByPostId(postDTO.getId()));     // 10번
    postDTO.setPostFiles(postFileDAO.findAllByPostId(postDTO.getId())); // 10번
});
// 전체: 목록 쿼리 1 + 태그 10 + 파일 10 = 21번
```

### 🔹 ResultMap 기본 구조

```xml
<!-- postMapper.xml에 resultMap 추가 -->
<resultMap id="postResultMap" type="PostDTO">
    <!-- 기본 컬럼 매핑 -->
    <id property="id" column="id"/>
    <result property="postTitle" column="post_title"/>
    <result property="postContent" column="post_content"/>
    <result property="memberName" column="member_name"/>
    <result property="createdDatetime" column="created_datetime"/>

    <!-- 1:N 매핑: tags 컬렉션 -->
    <collection property="tags" ofType="TagDTO">
        <id property="id" column="tag_id"/>
        <result property="tagName" column="tag_name"/>
        <result property="postId" column="tag_post_id"/>
    </collection>
</resultMap>

<!-- resultMap 사용 -->
<select id="selectAllWithTags" resultMap="postResultMap">
    select
        p.id, p.post_title, p.post_content,
        m.member_name, p.created_datetime,
        t.id as tag_id, t.tag_name, t.post_id as tag_post_id
    from tbl_post p
    join tbl_member m on m.id = p.member_id
    left outer join tbl_tag t on t.post_id = p.id
    order by p.id desc
    limit #{criteria.count} offset #{criteria.offset}
    <!--
        MyBatis가 같은 p.id에 대한 여러 행을 자동으로 하나의 PostDTO로 합침
        여러 태그가 있으면 tags List에 자동 추가
        → 쿼리 1번으로 모든 데이터 가져오기
    -->
</select>
```

### 🔹 association (1:1 매핑)

```xml
<!-- PostDTO 안에 MemberDTO 임베드 -->
<resultMap id="postWithMemberMap" type="PostDTO">
    <id property="id" column="post_id"/>
    <result property="postTitle" column="post_title"/>

    <!-- 1:1 매핑: 작성자 정보 -->
    <association property="member" javaType="MemberDTO">
        <id property="id" column="member_id"/>
        <result property="memberName" column="member_name"/>
        <result property="memberEmail" column="member_email"/>
    </association>
</resultMap>
```

---

## STEP 4 심화. REST API 전역 예외 처리 고도화

> **왜 여기서 공부하나?**
> 현재 v4의 PostExceptionHandler는 HTML 리다이렉트만 처리한다.
> v6의 REST API(`/api/replies/`)에서 예외 발생 시 JSON 에러 응답이 필요하다.

### 🔹 @RestControllerAdvice + ResponseEntity

```java
// 공통 에러 응답 DTO
public class ErrorResponse {
    private int status;
    private String message;
    private String timestamp;

    public static ErrorResponse of(int status, String message) {
        ErrorResponse error = new ErrorResponse();
        error.status = status;
        error.message = message;
        error.timestamp = LocalDateTime.now().toString();
        return error;
    }
}

// REST API 전용 예외 핸들러
@RestControllerAdvice(basePackages = "com.app.threetier.controller.reply")
public class ReplyExceptionHandler {

    // 404: 리소스 없음
    @ExceptionHandler(PostNotFoundException.class)
    public ResponseEntity<ErrorResponse> postNotFound(PostNotFoundException e) {
        return ResponseEntity
                .status(HttpStatus.NOT_FOUND)          // 404
                .body(ErrorResponse.of(404, "게시글을 찾을 수 없습니다."));
    }

    // 400: 잘못된 요청
    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<ErrorResponse> badRequest(IllegalArgumentException e) {
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)        // 400
                .body(ErrorResponse.of(400, e.getMessage()));
    }

    // 500: 서버 내부 오류
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> internalError(Exception e) {
        return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)  // 500
                .body(ErrorResponse.of(500, "서버 오류가 발생했습니다."));
    }
}
```

### 🔹 현재 코드 vs 고도화 비교

```java
// 현재 v4 방식 (HTML 리다이렉트)
@ExceptionHandler(PostNotFoundException.class)
protected RedirectView postNotFound(...) {
    return new RedirectView("/post/list");  // 브라우저 리다이렉트
}

// REST API 방식 (JSON 응답)
@ExceptionHandler(PostNotFoundException.class)
public ResponseEntity<ErrorResponse> postNotFound(...) {
    return ResponseEntity.status(404).body(ErrorResponse.of(404, "없음"));
    // fetch()에서: if (!response.ok) { const error = await response.json(); }
}
```

---

## STEP 5 심화. Bean Validation (@Valid)

> **왜 여기서 공부하나?**
> 현재 코드는 postTitle이 null이어도, replyContent가 빈 값이어도 저장이 된다.
> 서비스 레이어에서 if 체크 코드를 줄이고 선언적으로 검증하는 방법을 배운다.

### 🔹 어노테이션 적용

```java
// ReplyDTO에 검증 어노테이션 추가
public class ReplyDTO {
    private Long id;

    @NotBlank(message = "댓글 내용을 입력해주세요.")
    @Size(max = 500, message = "댓글은 500자 이내로 입력해주세요.")
    private String replyContent;

    @NotNull(message = "회원 정보가 없습니다.")
    private Long memberId;

    @NotNull(message = "게시글 정보가 없습니다.")
    private Long postId;
}
```

```java
// ReplyController에서 @Valid 적용
@PostMapping("write")
public ResponseEntity<Void> write(@RequestBody @Valid ReplyDTO replyDTO,
                                   BindingResult bindingResult) {
    if (bindingResult.hasErrors()) {
        // 첫 번째 오류 메시지 반환
        String errorMessage = bindingResult.getAllErrors().get(0).getDefaultMessage();
        return ResponseEntity.badRequest().build();
    }
    replyService.write(replyDTO);
    return ResponseEntity.ok().build();
}

// 또는 @Valid + @RestControllerAdvice로 자동 처리
@ExceptionHandler(MethodArgumentNotValidException.class)
public ResponseEntity<ErrorResponse> validationError(MethodArgumentNotValidException e) {
    String message = e.getBindingResult().getAllErrors().get(0).getDefaultMessage();
    return ResponseEntity.badRequest().body(ErrorResponse.of(400, message));
}
```

### 🔹 주요 검증 어노테이션

```java
@NotNull      // null 불가 (빈 문자열 "", 공백 " " 허용)
@NotEmpty     // null, "" 불가 (공백 " " 허용)
@NotBlank     // null, "", " " 모두 불가 (String에만 사용)
@Size(min=1, max=100)  // 문자열/컬렉션 크기 제한
@Min(0) @Max(100)      // 숫자 범위 제한
@Email        // 이메일 형식 검증
@Pattern(regexp="...")  // 정규식 검증
@Positive     // 양수만
@Future       // 미래 날짜만 (LocalDate, LocalDateTime)
```

---

## STEP 6 심화. 파일 업로드 고도화 (Thumbnailator)

> **왜 여기서 공부하나?**
> `build.gradle`에 `net.coobird:thumbnailator:0.4.8` 의존성이 있지만
> 현재 코드에서 사용하지 않는다. 이미지 최적화는 실무에서 필수다.

### 🔹 썸네일 생성 패턴

```java
// PostService.write() 내부에서 파일 저장 시 추가
import net.coobird.thumbnailator.Thumbnails;

multipartFiles.forEach(multipartFile -> {
    if (multipartFile.getOriginalFilename().isEmpty()) return;

    // MIME 타입 검증 (화이트리스트)
    String contentType = multipartFile.getContentType();
    if (!List.of("image/jpeg", "image/png", "image/webp").contains(contentType)) {
        throw new IllegalArgumentException("이미지 파일만 업로드 가능합니다.");
    }

    String fileName = UUID.randomUUID() + "_" + multipartFile.getOriginalFilename();
    File originalFile = new File(path, fileName);
    multipartFile.transferTo(originalFile);

    // ★ 원본 파일로 썸네일 생성
    if (contentType.contains("image")) {
        File thumbnailFile = new File(path, "thumb_" + fileName);
        Thumbnails.of(originalFile)
                .size(300, 300)         // 300x300으로 리사이즈
                .keepAspectRatio(true)  // 비율 유지
                .outputQuality(0.8)     // 품질 80%
                .toFile(thumbnailFile);
    }
});
```

---

## STEP 7 심화. 테스트 코드 작성

> **왜 여기서 공부하나?**
> `MemberMapperTests.java`가 v1에 있다. 이 패턴을 확장해 Service, Controller 테스트를 배운다.
> 테스트 없으면 리팩토링 시 기존 기능 깨짐을 모르고 배포하게 된다.

### 🔹 @MyBatisTest - Mapper 레이어 테스트

```java
@MyBatisTest                     // MyBatis 컴포넌트만 로드 (가볍고 빠름)
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
// NONE: 실제 DB 사용 (H2 인메모리 대신)
@Transactional                   // 각 테스트 후 자동 롤백
class PostMapperTests {
    @Autowired
    private PostMapper postMapper;

    @Test
    void insert_test() {
        PostDTO postDTO = new PostDTO();
        postDTO.setPostTitle("테스트 제목");
        postDTO.setPostContent("테스트 내용");
        postDTO.setMemberId(1L);

        postMapper.insert(postDTO);

        assertThat(postDTO.getId()).isNotNull();  // useGeneratedKeys 확인
    }

    @Test
    void selectAll_test() {
        Criteria criteria = new Criteria(1, 100);
        Search search = new Search();

        List<PostDTO> posts = postMapper.selectAll(criteria, search);

        assertThat(posts).isNotEmpty();
        assertThat(posts.size()).isLessThanOrEqualTo(11);
    }
}
```

### 🔹 @WebMvcTest - Controller 레이어 테스트

```java
@WebMvcTest(PostAPIController.class)  // PostAPIController만 로드
class PostAPIControllerTests {
    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private PostService postService;  // 실제 Service 대신 Mock 주입

    @Test
    void list_test() throws Exception {
        // given: mock 반환값 설정
        PostWithPagingDTO mockResult = new PostWithPagingDTO();
        mockResult.setPosts(new ArrayList<>());
        given(postService.list(anyInt(), any())).willReturn(mockResult);

        // when & then: 요청 후 응답 검증
        mockMvc.perform(get("/api/posts/list/1")
                .param("type", "전체")
                .param("keyword", ""))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.posts").isArray());
    }
}
```

---

## STEP 8 심화. 환경 프로파일 분리

> **왜 여기서 공부하나?**
> 현재 `application.yml`에 DB 비밀번호가 평문으로 들어있다.
> 개발/운영 환경 분리는 실무 필수 지식이다.

### 🔹 프로파일 분리 구조

```
resources/
├── application.yml          # 공통 설정 (프로파일 선택)
├── application-dev.yml      # 개발 환경 (로컬 DB)
└── application-prod.yml     # 운영 환경 (RDS 등)
```

```yaml
# application.yml (공통)
spring:
  profiles:
    active: dev          # 기본값: dev 프로파일 사용
  servlet:
    multipart:
      max-file-size: 5MB

server:
  port: 10000
```

```yaml
# application-dev.yml (개발)
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/spring
    username: spring
    password: 1234
  mail:
    username: dev@gmail.com

logging:
  level:
    com.app.threetier: DEBUG   # 개발 시 상세 로그
```

```yaml
# application-prod.yml (운영)
spring:
  datasource:
    url: ${DB_URL}             # 환경 변수에서 읽기
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
  mail:
    username: ${MAIL_USERNAME}

logging:
  level:
    com.app.threetier: WARN    # 운영 시 경고 이상만 로그
```

```bash
# 운영 서버 실행 시 프로파일 지정
java -jar app.jar --spring.profiles.active=prod
# 또는 환경 변수로
SPRING_PROFILES_ACTIVE=prod java -jar app.jar
```

---

## 학습 경로 요약

```
V1~V6 코드 이해 ← 지금 여기
    ↓
STEP 1: DI/Bean 원리 (왜 생성자 주입인가)
STEP 2: @Transactional 원리 (프록시, 전파 레벨)
STEP 3: MyBatis ResultMap (N+1 쿼리 해결)
STEP 4: REST 예외 처리 (JSON 에러 응답)
STEP 5: Bean Validation (선언적 검증)
STEP 6: 파일 처리 고도화 (Thumbnailator)
STEP 7: 테스트 코드 (Mapper/Controller)
STEP 8: 환경 프로파일 분리 (dev/prod)
    ↓
    다음 단계는 step_by_step_study.md의 STEP 9, 10 참고
    (Spring Security, REST API 고도화)
```

---

*마지막 업데이트: 2026-03-02*
*참고 파일: `step_by_step_study.md` (전체 로드맵)*
