# 📋 Step-by-Step 추가 학습 로드맵

> threetier_v1~v6 학습 후 연속적으로 공부하면 좋은 심화 주제들.
> 각 Step은 독립적이며 순서대로 따라가면 실무 수준에 도달한다.

---

## STEP 1. Spring DI / Bean 생명주기 심화

**왜 지금?** — @RequiredArgsConstructor가 왜 안전한 주입인지 원리로 이해해야 한다.

- 의존성 주입 3가지 비교 (생성자 / 필드 / 세터)
- 순환 참조 문제와 해결 방법
- @Component 계층 어노테이션의 역할 구분
- ApplicationContext와 BeanFactory의 차이
- Bean 스코프: singleton vs prototype vs request

---

## STEP 2. @Transactional 동작 원리 심화

**왜 지금?** — PostService의 @Transactional이 실제로 어떻게 작동하는지 알아야 버그를 막는다.

- Spring의 프록시(AOP) 기반 트랜잭션 동작 원리
- 셀프 호출(self-invocation) 문제: 같은 클래스 내 메서드 호출 시 트랜잭션 무시
- 트랜잭션 전파 레벨 (Propagation): REQUIRED, REQUIRES_NEW, NESTED
- readOnly = true 최적화: 읽기 전용 쿼리에 적용하는 이유
- 체크드 예외 vs 언체크드 예외 롤백 정책

---

## STEP 3. MyBatis ResultMap 심화

**왜 지금?** — 현재 코드에서 태그/파일 데이터를 N+1 쿼리로 가져온다. resultMap으로 해결하는 방법을 배워야 한다.

- `<resultMap>` id, type 속성 이해
- `<association>` : 1:1 관계 매핑 (PostDTO ↔ MemberDTO 임베드)
- `<collection>` : 1:N 관계 매핑 (PostDTO ↔ List<TagDTO> 한 번에)
- N+1 쿼리 문제란? resultMap으로 해결하는 방법
- `<discriminator>` : 타입별 다른 매핑 분기

---

## STEP 4. 전역 예외 처리 REST 버전 고도화

**왜 지금?** — 현재 @ControllerAdvice는 HTML 리다이렉트 방식. REST API용 에러 응답을 만들어야 한다.

- @RestControllerAdvice vs @ControllerAdvice 차이
- ResponseEntity<T>로 상태 코드 + 본문 함께 반환
- 공통 에러 응답 DTO 설계 (code, message, timestamp)
- HTTP 상태 코드 의미: 400, 401, 403, 404, 409, 500
- @ExceptionHandler에서 여러 예외 타입 동시 처리

---

## STEP 5. Bean Validation (@Valid / @Validated)

**왜 지금?** — 현재 코드에는 입력값 검증이 없다. 서비스 코드가 null, 빈 값에 취약하다.

- @NotNull, @NotBlank, @Size, @Email, @Min, @Max
- Controller에서 @Valid 적용 + BindingResult 처리
- @Validated: 그룹 검증 (등록 시 / 수정 시 다른 검증 규칙)
- 커스텀 어노테이션 검증기 작성 (@ConstraintValidator)
- REST API에서 MethodArgumentNotValidException 처리

---

## STEP 6. 파일 업로드 고도화 (Thumbnailator)

**왜 지금?** — 의존성에 Thumbnailator가 이미 있지만 현재 코드에서 미사용 상태다.

- Thumbnails.of().size().toFile()로 썸네일 생성
- 원본 파일 vs 썸네일 파일 동시 저장 패턴
- MIME 타입 검증 (화이트리스트 방식: image/jpeg, image/png만 허용)
- 파일 확장자 검증 + 실제 MIME 타입 검증 (헤더 스니핑)
- 파일 크기 제한과 업로드 실패 시 트랜잭션 롤백 처리

---

## STEP 7. 테스트 코드 작성

**왜 지금?** — 테스트 없이는 리팩토링이 불가능하고 버그 추적이 어렵다.

- @SpringBootTest: 전체 컨텍스트 로드 통합 테스트
- @MyBatisTest: MyBatis 레이어만 테스트 (DB 연결 필요)
- @WebMvcTest: Controller 레이어 단위 테스트 (MockMvc)
- MockMvc로 REST API 요청/응답 검증
- @Transactional on 테스트: 테스트 후 자동 롤백
- MemberMapperTests.java 패턴 확장 (현재 v1에 있음)

---

## STEP 8. 환경 프로파일 분리

**왜 지금?** — 현재 application.yml에 DB 비밀번호가 평문으로 노출된다.

- application.yml / application-dev.yml / application-prod.yml 분리
- @Profile("dev") / @Profile("prod") 빈 조건 등록
- Spring Boot의 프로파일 활성화: spring.profiles.active
- 환경 변수 / 시스템 속성으로 민감 정보 외부화
- @ConfigurationProperties로 설정 클래스 타입 바인딩

---

## STEP 9. Spring Security 기초 도입

**왜 지금?** — 현재는 세션 수동 관리 + 인터셉터로 인증 처리한다. Security로 표준화한다.

- SecurityFilterChain 설정 (requestMatchers, csrf, formLogin)
- UserDetails / UserDetailsService 구현
- PasswordEncoder (BCrypt) 적용
- 현재 세션 방식 → Security 기반으로 마이그레이션 과정
- remember-me 쿠키를 Security 표준 방식으로 전환

---

## STEP 10. REST API 고도화 + Swagger

**왜 지금?** — v6의 Reply REST API를 기반으로 프로 수준의 API 설계를 완성한다.

- ResponseEntity<T>로 응답 통일: status + body + headers
- HATEOAS 기초: 응답에 관련 링크 포함
- API 버저닝 전략: /api/v1/, /api/v2/
- Springdoc OpenAPI (Swagger UI) 설정
- @Operation, @Parameter, @ApiResponse 문서화 어노테이션
- Pageable 객체로 Spring Data 페이지네이션 패턴

---

## 학습 순서 요약

```
현재 코드 이해 (v1~v6)
    ↓
STEP 1: DI/Bean 원리 (기반)
    ↓
STEP 2: @Transactional 원리 (기반)
    ↓
STEP 3: MyBatis 심화 (N+1 해결)
    ↓
STEP 4: REST 예외 처리 (API 완성도)
    ↓
STEP 5: 입력 검증 (안정성)
    ↓
STEP 6: 파일 처리 고도화 (실무)
    ↓
STEP 7: 테스트 작성 (품질)
    ↓
STEP 8: 환경 설정 분리 (운영)
    ↓
STEP 9: Spring Security (보안)
    ↓
STEP 10: API 고도화 (심화)
```
