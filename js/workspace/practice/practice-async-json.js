// const commentService = (() => {
//     const getList = async (postId, callback) => {
//         const response = await fetch(
//             "https://jsonplaceholder.typicode.com/comments"
//         );
//         const comments = await response.json();
//         if (callback) {
//             return callback(postId, comments);
//         }
//     };

//     return { getList };
// })();

// const printCommentInfo = (postId, comments) => {
//     comments
//         .filter((comment) => comment.postId === postId)
//         .forEach((comment) =>
//             console.log(`이름: ${comment.name}`, `이메일: ${comment.email}`)
//         );
// };

// // postId가 1인 댓글의 name과 email 출력
// commentService.getList(1, printCommentInfo);
// ============================================================================
// const userService = (() => {
//     const getList = async (city, callback) => {
//         const response = await fetch(
//             "https://jsonplaceholder.typicode.com/users"
//         );
//         const users = await response.json();

//         if (callback) {
//             return callback(city, users);
//         }
//     };

//     return { getList };
// })();

// const printUsersByCity = (city, users) => {
//     users
//         .filter((user) => user.address.city === city)
//         .forEach((user) =>
//             console.log(
//                 `이름: ${user.name}`,
//                 `이메일: ${user.email}`,
//                 `폰: ${user.phone}`
//             )
//         );
// };

// // "Gwenborough" 도시에 사는 사용자 정보 출력
// userService.getList("Gwenborough", printUsersByCity);
// ============================================================================
// const todoService = (() => {
//     const getList = async (userId, callback) => {
//         try {
//             const response = await fetch(
//                 "https://jsonplaceholder.typicode.com/todos"
//             );
//             const todos = await response.json();
//             if (callback) {
//                 return callback(userId, todos);
//             }
//         } catch (err) {
//             console.log(err);
//         }
//     };

//     return { getList };
// })();

// const printTodoStats = (userId, todos) => {
//     const userTodos = todos.filter((todo) => todo.userId === userId);
//     const completedTodos = userTodos.filter((todo) => todo.completed);
//     const incompleteTodos = userTodos.filter((todo) => !todo.completed);

//     console.log(`=== 사용자 ${userId}의 할 일 통계 ===`);
//     console.log(`완료: ${completedTodos.length}개`);
//     console.log(`미완료: ${incompleteTodos.length}개`);
//     console.log();

//     console.log("[완료된 할 일 목록]");
//     completedTodos.forEach((todo) => console.log(`- ${todo.title}`));
// };

// todoService.getList(1, printTodoStats);
// ============================================================================
// const photoService = (() => {
//     const getList = async (albumId, keyword, callback) => {
//         try {
//             const response = await fetch(
//                 "https://jsonplaceholder.typicode.com/photos"
//             );

//             const photos = await response.json();
//             if (callback) {
//                 return callback(albumId, keyword, photos);
//             }
//         } catch (err) {
//             console.log(err);
//         }
//     };

//     return { getList };
// })();

// const printPhotosByKeyword = (albumId, keyword, photos) => {
//     photos
//         .filter((photo) => photo.albumId === albumId)
//         .filter((photo) => photo.title.includes(keyword))
//         .forEach((photo) =>
//             console.log(
//                 `아이디: ${photo.albumId}`,
//                 `제목: ${photo.title}`,
//                 `url: ${photo.url}`
//             )
//         );
// };

// // albumId가 1이고, 제목에 "repudiandae"가 포함된 사진 정보 출력
// photoService.getList(1, "repudiandae", printPhotosByKeyword);

// 다음과 같이 사용 가능
// const printPhotosByKeyword = (albumId, keyword, photos) => {
//     photos
//         .filter((photo) =>
//             photo.albumId === albumId &&
//             photo.title.includes(keyword)
//         )
//         .forEach((photo) =>
//             console.log(
//                 `아이디: ${photo.id}`,
//                 `제목: ${photo.title}`,
//                 `URL: ${photo.url}`
//             )
//         );
// };
// 클루드의 개선점 담은 코드
// const photoService = (() => {
//     const getList = async (albumId, keyword, callback) => {
//         try {
//             const response = await fetch(
//                 "https://jsonplaceholder.typicode.com/photos"
//             );
//             const photos = await response.json();

//             if (callback) {
//                 return callback(albumId, keyword, photos);
//             }
//         } catch (err) {
//             console.error("사진 조회 실패:", err);
//         }
//     };

//     return { getList };
// })();

// const printPhotosByKeyword = (albumId, keyword, photos) => {
//     // 필터링
//     const filteredPhotos = photos
//         .filter((photo) => photo.albumId === albumId)
//         .filter((photo) => photo.title.includes(keyword));

//     // 결과 없을 때
//     if (filteredPhotos.length === 0) {
//         console.log(`\n앨범 ${albumId}에서 "${keyword}"를 포함한 사진이 없습니다.`);
//         return;
//     }

//     // 결과 출력
//     console.log(`\n=== 앨범 ${albumId}, "${keyword}" 검색 결과 (${filteredPhotos.length}개) ===\n`);

//     filteredPhotos.forEach((photo, index) => {
//         console.log(`${index + 1}. [ID: ${photo.id}]`);
//         console.log(`   제목: ${photo.title}`);
//         console.log(`   URL: ${photo.url}\n`);
//     });
// };

// // albumId가 1이고, 제목에 "repudiandae"가 포함된 사진 정보 출력
// photoService.getList(1, "repudiandae", printPhotosByKeyword);
// // ============================================================================
// const postService = (() => {
//     const getPostsWithCommentCount = async (userId, callback) => {
//         try {
//             // 1. 게시글 가져오기
//             const postsResponse = await fetch(
//                 "https://jsonplaceholder.typicode.com/posts"
//             );
//             const posts = await postsResponse.json();

//             // 2. 댓글 가져오기
//             const commentsResponse = await fetch(
//                 "https://jsonplaceholder.typicode.com/comments"
//             );
//             const comments = await commentsResponse.json();

//             if (callback) {
//                 callback(userId, posts, comments);
//             }
//         } catch (err) {
//             console.log(err);
//         }
//     };

//     return { getPostsWithCommentCount };
// })();

// const printPostsWithComments = (userId, posts, comments) => {
//     console.log(`=== 사용자 ${userId}의 게시글(댓글 개수 포함) ===`);
//     const postFilter = posts.filter((post) => post.userId === userId);
//     postFilter.forEach((post) => {
//         const commentCount = comments.filter(
//             (comment) => comment.postId === post.id
//         ).length;
//         console.log(
//             `[게시글 ${post.id}] ${post.title} (댓글 ${commentCount}개)`
//         );
//     });
//     // [게시글 1] sunt aut facere... (댓글 5개)
//     // [게시글 2] qui est esse (댓글 5개)
//     // ...
// };

// // userId가 1인 사용자의 게시글과 각 게시글의 댓글 개수 출력
// postService.getPostsWithCommentCount(1, printPostsWithComments);
// // ============================================================================
// // 1. 두 API 모두 가져오기
// const posts = await fetch(...).then(r => r.json());
// const comments = await fetch(...).then(r => r.json());

// // 2. 둘 다 callback에 전달
// callback(userId, posts, comments);

// // 3. forEach 안에서 filter로 개수 세기
// userPosts.forEach((post) => {
//     const count = comments.filter(c => c.postId === post.id).length;
// });
