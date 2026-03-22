// const promise = new Promise((resolve, reject) => {
//     let check = true;

//     if (check) {
//         resolve("resolve");
//     } else {
//         reject("reject");
//     }
// });

// // 동기코드
// let data = null;
// // 여기부터 비동기 코드
// promise
//     .then((result) => {
//         data = result;
//         console.log(result);
//         return 10;       첫번째 리턴값은 다음 then의 콜백으로 들어온다
//     })
//     .then((data) => {
//         console.log(data);
//     })
//     .catch((err) => {
//         console.log(err);
//     });
// // 동기코드와 비동기 코드의 혼합으로 출력을 하게 되면 null이나옴(동기코드가 먼저 진행된 후 비동기 코드가 진행되었다!)
// console.log(data);

// =======================================================================================
// 서버에서 게시글 목록 요청하기
// 받은 게시글 중 id가 짝수인 게시글의 아이디와 제목 출력하기
// const getPostList = async () => {
//     try {
//         const response = await fetch(
//             "https://jsonplaceholder.typicode.com/posts"
//         );

//         const posts = await response.json();

//         posts
//             .filter((post) => post.id % 2 === 0) // 짝수만

//             .forEach((post) => console.log(post.id, post.title));
//     } catch (err) {
//         console.log(err);
//     }
// };
// getPostList();
// =======================================================================================
// 전달받은 댓글들 중, postId가 3인 댓글 내용 출력
// const getCommetList = async () => {
//     try {
//         const respose = await fetch(
//             "https://jsonplaceholder.typicode.com/comments"
//         );
//         const comments = await respose.json();
//         comments
//             .filter((comment) => comment.postId === 3)
//             .forEach((comment) => console.log(comment));
//     } catch (err) {
//         console.log(err);
//     }
// };
// getCommetList();
// =======================================================================================
// 전달받은 회원들 중, zipcode만 출력
// const getUserList = async () => {
//     try {
//         const response = await fetch(
//             "https://jsonplaceholder.typicode.com/users"
//         );

//         const users = await response.json();
//         users.forEach((user) => {
//             console.log(user.address.zipcode);
//         });
// user안에 address 객체가 또 존재함
//     } catch (err) {
//         console.log(err);
//     }
// };
// getUserList();
// =======================================================================================
// 게시글 정보를 전달받은 후,
// 게시글 조회를 모듈화하여 사용한다.
// 게시글 조회시, 회원의 번호를 전달받아서 그 작성자의 게시글만 가져온다.
// // 전체 정보를 출력한다.
// const getPostService = (() => {
//     const getList = async (userId, callback, page = 1) => {
//         try {
//             const response = await fetch(
//                 "https://jsonplaceholder.typicode.com/posts"
//             );
//             const posts = await response.json();

//             if (callback) {
//                 return callback(userId, posts);
//             }
//         } catch (err) {
//             console.log(err);
//         }
//     };

//     return { getList: getList };
// })();

// const readByUserId = (userId, posts) => {
//     posts
//         .filter((post) => post.id === userid)
//         .forEach((post) => console.log(post));
// };
// getPostService.getList(1, readByUserId);
// =======================================================================================
// ### getPostService.getList(1, readByUserId)의 의미:

// 1. **1**: userId 값 → "userId가 1인 게시글을 찾아줘"
// 2. **readByUserId**: callback 함수 → "데이터를 받으면 이 함수로 처리해줘"

// ### 실행 흐름:
// ```
// ① getList 함수 호출 (1, readByUserId)
// ② 서버에서 posts 데이터 가져오기
// ③ callback(1, posts) 실행
//    = readByUserId(1, posts) 실행
// ④ userId가 1인 게시글만 필터링해서 출력
// =======================================================================================

// 앨범 정보를 전달받은 후,
// 회원 번호가 5인 정보를 모두 가져온다.
// 그 중 userId와 title만 출력한다.
// const getAlbumService = (() => {
//     const getAlbumList = async (userId, callback, page = 1) => {
//         try {
//             const response = await fetch(
//                 "https://jsonplaceholder.typicode.com/albums"
//             );
//             const albums = await response.json();
//             if (callback) {
//                 return callback(userId, albums);
//             }
//         } catch (err) {
//             console.log(err);
//         }
//     };
//     return { getAlbumList: getAlbumList };
// })();

// const printAlbumIdTitle = (userId, albums) => {
//     albums
//         .filter((album) => album.userId === userId)
//         .forEach((album) => console.log(album.userId, album.title));
// };
// album.userId는 json 데이터에 있는 속성명과 일치해야함
// getAlbumService.getAlbumList(5, printAlbumIdTitle);
// ======================================================================================
// 디버깅 팁
// const printAlbumIdTitle = (userId, albums) => {
//     // 1단계: 전체 데이터 확인
//     console.log("받은 데이터:", albums[0]);
//     // 출력: { userId: 1, id: 1, title: "..." }

//     // 2단계: 필터 결과 확인
//     const filtered = albums.filter((album) => album.userId === userId);
//     console.log("필터 결과 개수:", filtered.length);  // 0개 → 문제 발견!

//     // 3단계: 속성명 확인
//     console.log("첫 번째 앨범의 키:", Object.keys(albums[0]));
//     // 출력: ["userId", "id", "title"] → userId가 맞네!

//     filtered.forEach((album) => console.log(album.userId, album.title));
// };
// ===========================================================================================
// 마지막 문제 클로드 버전
// 모듈화된 앨범 서비스
// const albumService = (() => {
//     // 전체 앨범 가져오기
//     const getList = async () => {
//         try {
//             const response = await fetch(
//                 "https://jsonplaceholder.typicode.com/albums"
//             );
//             return await response.json();
//         } catch (err) {
//             console.error("앨범 조회 실패:", err);
//             return [];
//         }
//     };

//     // 특정 사용자의 앨범만 가져오기
//     const getByUserId = async (userId) => {
//         try {
//             const albums = await getList();
//             return albums.filter(album => album.userId === userId);
//         } catch (err) {
//             console.error("사용자 앨범 조회 실패:", err);
//             return [];
//         }
//     };

//     return { getList, getByUserId };
// })();

// // 사용 예시 1: callback 방식
// albumService.getByUserId(5).then(albums => {
//     albums.forEach(album => {
//         console.log(album.userId, album.title);
//     });
// });

// // 사용 예시 2: async/await 방식 (더 깔끔!)
// async function showUserAlbums(userId) {
//     const albums = await albumService.getByUserId(userId);

//     console.log(`사용자 ${userId}의 앨범 (총 ${albums.length}개):`);
//     albums.forEach(album => {
//         console.log(`- [${album.id}] ${album.title}`);
//     });
// }

// showUserAlbums(5);
